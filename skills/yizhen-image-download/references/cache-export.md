# 已验证的缓存路线与适配边界

2026-11 在医真云电子胶片的 Vue 2 / Cornerstone 查看器验证过此路线。下列属性是发现线索，必须对当前页面验证，不保证其他医院、版本相同。代码片段供已授权浏览器能力调用，不是可直接粘贴到 shell 的脚本。

## 1. 找到正确 iframe 和缓存对象

通过当前 tab 的 CDP capability 阅读操作文档，使用 `Page.getResourceTree` / DOM 确认影像 iframe。旧版常为 `#iframeId`，内部挂载节点 `#app`。高层 frame locator 可以只读检查 DOM；需要页面对象时，可用 `DOM.getDocument({depth:-1,pierce:true})` 找真实挂载节点，再 `DOM.resolveNode`，通过 `Runtime.callFunctionOn` 读取 `this.__vue__`。不要用 isolated world 猜主世界的全局变量。

已验证版本的 `$Images` 位于挂载节点的 `this.__vue__.$Images`；这是候选路径，先确认当前实例/源码真实暴露该属性。`window.cornerstone` 和 `window.dicomParser` 同样先做存在性与接口检查，不能由源码里的函数名字推断全局存在。

已验证数据：

```js
const s = this.__vue__.$store.state['2D'];
// s.studyList: 各序列 images[].frames[] 的实际 image ID
// s.studyData[id]: periodId, imageId, frameId, dicomInfo,
//                  isLoaded, isLoadedToLocal, imageTypeKey
// window.cornerstone.getEnabledElements(): 当前显示的图像
```

默认只输出数量、尺寸、序列描述等必要字段；不要输出整个 store、Base64 或带认证参数 URL。优先枚举一次、精确读取，避免反复打印全部源码和医疗字段。

查看页面已加载的 app JS（`Page.getResourceContent`，URL 来自资源树），搜索 `getImageBlobUrlByImageUrl`、`afterGetImage`、`saveImageBlobUrl`、`parseDicom`、`downloadImagesByPeriod`。关键证据是服务数据 `buffer` 被 `dicomParser.parseDicom` 解析后保存为 Blob，图像对象本身却未暴露 `.data`。

优先使用页面已暴露的缓存读取对象。已验证版本中 `$Images` 的模块闭包变量 `ee` 是加载器，具有 `getImageBlobUrlByImageUrl(id)`。如果仅闭包可达：

1. `Runtime.callFunctionOn` 返回当前 `$Images.getImagesByPeriodId` 函数对象（不按值返回）。
2. `Runtime.getProperties` 读取该函数 `internalProperties` 的 `[[Scopes]]`，再枚举闭包描述；不要假定是第几个 scope。
3. 只检查当前源码已确认包含缓存变量的模块闭包，定位 `ee` 的对象句柄，再核对其读取方法。变量名和闭包结构变化时依据当前源码重新定位；找不到就停止这条路线，不读 Global scope 或扫描无关敏感状态。
4. 调用读取方法获得当前图像的 Blob URL。只读这个已观察到的 Blob，不构造远端请求或启用隐藏权限。

如果部分切片尚未缓存，当前代码确实存在 `$Images.downloadImagesByPeriod(index)` 时，可按目标序列调用正常加载方法，随后有界检查加载状态。未完成时记录缺失，不能无限等待或宣称完整。不要通过设置权限对象开启功能。

## 2. 保存并检查 DICOM

下面示例前提是当前 iframe 主世界已确认存在 `window.dicomParser.parseDicom`。若仅模块内存在，使用已确认的解析器句柄；否则先将 Blob 原字节保存到任务临时目录，用已有可信本地 DICOM 解析器验证，通过后才以 `.dcm` 纳入成品。没有可用解析器时报告未验证，不把未知二进制当成有效 DICOM。

以下函数通过 `Runtime.callFunctionOn` 绑定到已确认的加载器对象，传入来自当前目录的 id；设置 `awaitPromise:true`、`returnByValue:true`。它只读取本页 Blob：

```js
async function readDicom(id) {
  const url = this.getImageBlobUrlByImageUrl(id);
  if (!url || !url.startsWith('blob:')) throw new Error('No cached Blob');
  const response = await fetch(url);
  if (!response.ok) throw new Error('Blob unavailable');
  const blob = await response.blob();
  const bytes = new Uint8Array(await blob.arrayBuffer());
  const ds = window.dicomParser.parseDicom(bytes);
  if (!ds.elements.x7fe00010) throw new Error('No supported pixel element');
  const base64 = await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
  return {
    base64, byteLength: bytes.length,
    rows: ds.uint16('x00280010'), columns: ds.uint16('x00280011'),
    bitsAllocated: ds.uint16('x00280100'),
    transferSyntax: ds.string('x00020010'),
    numberOfFrames: ds.string('x00280008') || '1',
    warnings: ds.warnings || []
  };
}
```

Node REPL 使用 `fs.writeFile(path, Buffer.from(result.base64, 'base64'))` 保存，不将 Base64 打印到对话。返回异常、缺失像素、告警时先调查，不能把错误文本保存为 `.dcm`。保留源字节，不重新编码。文件过大时分批或用受支持的本地下载能力，不把图像发给外部转换服务。

历史样本传输语法 `1.2.840.10008.1.2.4.51` 为 JPEG Extended（有损编码语法）；不能由 `BitsAllocated=16` 推断无损。当前文件可能不同，按真实标签判断。不保证服务器未压缩、脱敏或重写标签。

## 3. 从原尺寸像素导出 PNG

缓存图像可经 `window.cornerstone.loadAndCacheImage(id)` 读取，优先复用该版本验证过的渲染器。取 `width/height`、`getPixelData()` 和该图像实际窗宽窗位，创建不挂到 DOM 的离屏 canvas；尺寸必须等于图像尺寸，不能使用显示 canvas 的缩放后尺寸。不要固定取第一个 enabled element 来批量导出不同切片。

本次成功的简化转换仅适用于单通道、线性 VOI、无额外 LUT 的灰度影像：

```js
// 对每个像素 p，先使用该图像的 slope/intercept，缺失时为 1/0。
const x = p * slope + intercept;
// DICOM LINEAR，windowWidth >= 1；width=1 是阈值，不能除以零。
const y = width === 1 ? (x <= center - 0.5 ? 0 : 255)
  : Math.max(0, Math.min(255, ((x - (center - 0.5)) / (width - 1) + 0.5) * 255));
// 按实际 MONOCHROME1/查看器 invert 语义仅反相一次；填 RGB=y，alpha=255。
```

注意代码中的 `width` 是窗宽，不是图像宽度。先验证数值有限且窗宽合法。颜色、多帧、非线性 VOI、Modality/VOI LUT、Presentation LUT 或不明反相语义，使用匹配的已验证 DICOM 渲染器，不能套用这个公式。未覆盖时保留 DICOM 并明确 PNG 缺失，不声称成功。

每帧独立保存 PNG；DICOM 按实际 SOP 实例去重，保留多帧完整文件。相同 SOPInstanceUID 且字节哈希一致时可合并；UID 相同而哈希不同，保留各版本并记为待核对冲突，不静默覆盖。缺少可靠 UID 时不得仅按帧数或数组位置推断重复。用真实 frame ID 与图像号核对映射。导出 PNG 后应校验并抽查画面；图像不正常时不要仅凭非零文件大小验收。
