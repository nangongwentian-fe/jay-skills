# 在 macOS 和 Windows 里让 Codex 始终走 Clash 代理

这是一份给 Agent 读取和执行的教程。目标是让 Codex CLI 或 Codex.app 单独走 Clash 代理，避免为了 Codex 打开 TUN/全局代理后影响其它软件。

## 适用范围

| 系统 | 支持对象 | 推荐做法 |
|------|----------|----------|
| macOS | Codex CLI | 在 shell 配置里定义 `codex()` 函数，只影响终端里的 `codex` 命令 |
| macOS | Codex.app | 用 `launchctl setenv` 设置图形会话环境变量，并用 `LaunchAgent` 持久化 |
| Windows | Codex.app | 创建一个专用启动器 `.bat`，只给 Codex.app 进程注入代理环境变量 |
| Windows | Codex CLI | 本文暂不覆盖，优先建议在 WSL/Linux 环境里用 shell 函数方式处理 |

## Agent 执行前检查

Agent 帮用户处理前，必须先确认以下信息。

| 检查项 | macOS 命令 | Windows PowerShell 命令 | 目的 |
|--------|------------|--------------------------|------|
| 操作系统 | `uname -s` | `$PSVersionTable.OS` | 选择 macOS 或 Windows 方法 |
| Clash 是否存在 | `ls /Applications | grep -Ei 'clash|mihomo|verge'` | `Get-Process | Where-Object { $_.ProcessName -match 'clash|mihomo|verge' }` | 确认代理软件已安装或正在运行 |
| 常见端口是否可用 | `lsof -nP -iTCP -sTCP:LISTEN | grep -E '7890|7897|7899'` | `Test-NetConnection 127.0.0.1 -Port 7897` | 找到 Clash HTTP 代理端口 |
| Codex.app 是否存在 | `mdfind 'kMDItemCFBundleIdentifier == "*Codex*"'` 或 `ls /Applications | grep -i Codex` | `Get-AppxPackage -Name OpenAI.Codex` | 确认可启动的 Codex 桌面端 |
| Codex CLI 是否存在 | `command -v codex` | `where.exe codex` | 只在需要处理 CLI 时检查 |

端口不要硬猜。常见端口是 `7890`、`7897`、`7899`，但必须以用户电脑实际监听端口为准。

## 使用前告知用户

| 事项 | 需要告诉用户的话 |
|------|------------------|
| Clash 必须运行 | 平时使用 Codex 前，保持 Clash 打开即可 |
| 不需要 TUN | 本方案给 Codex 单独注入代理环境变量，通常不需要开启 TUN/虚拟网卡/全局代理 |
| 系统代理不是必须 | 为了让 Codex 走代理，不需要依赖系统代理；浏览器访问外网时，很多情况下只开系统代理就够了 |
| 端口变更 | Clash 端口改了以后，需要把教程里使用的端口同步改成新端口 |
| 影响范围 | macOS 的 `launchctl setenv` 会影响设置后启动的图形应用；Windows `.bat` 方案只影响通过这个启动器打开的 Codex.app |

## 判断流程

```mermaid
flowchart TD
    A["开始"] --> B{"用户系统是什么？"}
    B -->|macOS| C["检查 Clash 和端口"]
    B -->|Windows| D["检查 Clash、端口和 Codex Appx 包"]
    C --> E{"处理对象"}
    E -->|Codex CLI| F["写入 shell 函数"]
    E -->|Codex.app| G["设置 launchctl + LaunchAgent"]
    D --> H["创建 Codex 专用 bat 启动器"]
    F --> I["验证代理环境变量和启动结果"]
    G --> I
    H --> I
```

## macOS：让 Codex CLI 走 Clash

以下示例端口用 `7897`。执行前先替换成用户电脑真实端口。

1. 确认 shell 配置文件

   | Shell | 配置文件 |
   |-------|----------|
   | zsh | `~/.zshrc` |
   | bash | `~/.bashrc` 或 `~/.bash_profile` |

2. 写入 `codex()` 函数

   ```bash
   # Codex Clash proxy
   codex() {
     HTTP_PROXY=http://127.0.0.1:7897 \
     HTTPS_PROXY=http://127.0.0.1:7897 \
     ALL_PROXY=http://127.0.0.1:7897 \
     http_proxy=http://127.0.0.1:7897 \
     https_proxy=http://127.0.0.1:7897 \
     all_proxy=http://127.0.0.1:7897 \
     NO_PROXY=localhost,127.0.0.1,::1 \
     no_proxy=localhost,127.0.0.1,::1 \
     command codex "$@"
   }
   ```

3. 让当前终端生效

   ```bash
   source ~/.zshrc
   ```

4. 验证

   ```bash
   type codex
   ```

   预期看到类似：

   ```text
   codex is a shell function from ~/.zshrc
   ```

## macOS：让 Codex.app 走 Clash

Codex.app 是图形应用，不会读取 `~/.zshrc` 里的 `codex()` 函数。要让从 Dock、访达、启动台打开的 Codex.app 继承代理，需要设置图形会话环境变量。

### 临时生效

```bash
launchctl setenv HTTP_PROXY http://127.0.0.1:7897
launchctl setenv HTTPS_PROXY http://127.0.0.1:7897
launchctl setenv ALL_PROXY http://127.0.0.1:7897
launchctl setenv http_proxy http://127.0.0.1:7897
launchctl setenv https_proxy http://127.0.0.1:7897
launchctl setenv all_proxy http://127.0.0.1:7897
launchctl setenv NO_PROXY localhost,127.0.0.1,::1
launchctl setenv no_proxy localhost,127.0.0.1,::1

killall Codex 2>/dev/null || true
open -a Codex
```

验证：

```bash
launchctl getenv HTTP_PROXY
launchctl getenv HTTPS_PROXY
launchctl getenv ALL_PROXY
launchctl getenv NO_PROXY
```

### 登录后自动生效

1. 创建 `LaunchAgent`

   ```bash
   mkdir -p ~/Library/LaunchAgents
   nano ~/Library/LaunchAgents/com.local.codex-proxy-env.plist
   ```

2. 写入配置

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
   "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
     <dict>
       <key>Label</key>
       <string>com.local.codex-proxy-env</string>

       <key>ProgramArguments</key>
       <array>
         <string>/bin/zsh</string>
         <string>-lc</string>
         <string>launchctl setenv HTTP_PROXY http://127.0.0.1:7897; launchctl setenv HTTPS_PROXY http://127.0.0.1:7897; launchctl setenv ALL_PROXY http://127.0.0.1:7897; launchctl setenv http_proxy http://127.0.0.1:7897; launchctl setenv https_proxy http://127.0.0.1:7897; launchctl setenv all_proxy http://127.0.0.1:7897; launchctl setenv NO_PROXY localhost,127.0.0.1,::1; launchctl setenv no_proxy localhost,127.0.0.1,::1</string>
       </array>

       <key>RunAtLoad</key>
       <true/>
     </dict>
   </plist>
   ```

3. 设置权限并检查语法

   ```bash
   chmod 600 ~/Library/LaunchAgents/com.local.codex-proxy-env.plist
   plutil -lint ~/Library/LaunchAgents/com.local.codex-proxy-env.plist
   ```

4. 加载并立即运行

   ```bash
   launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.local.codex-proxy-env.plist >/dev/null 2>&1 || true
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.local.codex-proxy-env.plist
   launchctl kickstart -k gui/$(id -u)/com.local.codex-proxy-env
   ```

5. 验证

   ```bash
   launchctl print gui/$(id -u)/com.local.codex-proxy-env
   launchctl getenv HTTP_PROXY
   launchctl getenv HTTPS_PROXY
   launchctl getenv ALL_PROXY
   launchctl getenv NO_PROXY
   ```

   重点检查：

   | 字段 | 正常值 |
   |------|--------|
   | `type` | `LaunchAgent` |
   | `last exit code` | `0` |
   | `runs` | 大于等于 `1` |
   | `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` | `http://127.0.0.1:7897` |
   | `NO_PROXY` | `localhost,127.0.0.1,::1` |

## Windows：让 Codex.app 走 Clash

Windows 推荐用专用 `.bat` 启动器，不修改系统环境变量。这样只有通过该启动器打开的 Codex.app 会走 Clash。

### 创建启动器

把下面内容保存为桌面文件：

```text
C:\Users\<用户名>\Desktop\start-codex-with-clash.bat
```

内容如下。端口默认是 `7897`，也可以运行时传入端口，例如 `start-codex-with-clash.bat 7890`。

```bat
@echo off
setlocal

set "CLASH_HOST=127.0.0.1"
set "CLASH_PORT=7897"
set "CODEX_PACKAGE_NAME=OpenAI.Codex"
set "CODEX_DESKTOP="

if not "%~1"=="" set "CLASH_PORT=%~1"

for /f "delims=" %%I in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "$pkg=Get-AppxPackage -Name OpenAI.Codex -ErrorAction SilentlyContinue; if($pkg){ $exe=Join-Path $pkg.InstallLocation 'app\Codex.exe'; if(Test-Path -LiteralPath $exe){ Write-Output $exe } }"') do set "CODEX_DESKTOP=%%I"

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $client = New-Object Net.Sockets.TcpClient; $connect = $client.BeginConnect('%CLASH_HOST%', [int]'%CLASH_PORT%', $null, $null); if (-not $connect.AsyncWaitHandle.WaitOne(1000, $false)) { $client.Close(); exit 2 }; $client.EndConnect($connect); $client.Close(); exit 0 } catch { exit 1 }"
if errorlevel 1 (
  echo Clash proxy is not reachable at %CLASH_HOST%:%CLASH_PORT%.
  echo Start Clash first, or run: %~nx0 7890
  pause
  exit /b 1
)

if "%CODEX_DESKTOP%"=="" (
  echo Codex desktop app was not found through Get-AppxPackage %CODEX_PACKAGE_NAME%.
  echo.
  echo Run this in PowerShell to inspect the installed package:
  echo Get-AppxPackage -Name OpenAI.Codex ^| Select-Object Name,Version,InstallLocation
  pause
  exit /b 1
)

set "HTTP_PROXY=http://%CLASH_HOST%:%CLASH_PORT%"
set "HTTPS_PROXY=http://%CLASH_HOST%:%CLASH_PORT%"
set "ALL_PROXY=http://%CLASH_HOST%:%CLASH_PORT%"
set "NO_PROXY=localhost,127.0.0.1,::1"

start "" "%CODEX_DESKTOP%"
endlocal
```

### 验证

1. 打开 Clash，确认 HTTP 代理端口正在监听。

   ```powershell
   Test-NetConnection 127.0.0.1 -Port 7897
   ```

   `TcpTestSucceeded` 应为 `True`。

2. 双击 `start-codex-with-clash.bat` 打开 Codex.app。

3. 如果 Clash 端口不是 `7897`，用端口参数启动。

   ```powershell
   C:\Users\<用户名>\Desktop\start-codex-with-clash.bat 7890
   ```

4. 后续使用 Codex.app 时，固定从这个 `.bat` 启动器打开。

## 取消设置

| 系统 | 取消方式 |
|------|----------|
| macOS Codex CLI | 删除 shell 配置文件里的 `# Codex Clash proxy` 函数块，然后执行 `source ~/.zshrc` |
| macOS Codex.app | `launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.local.codex-proxy-env.plist` 后删除 plist |
| macOS 当前会话变量 | 执行 `launchctl unsetenv HTTP_PROXY` 等 unset 命令 |
| Windows Codex.app | 删除 `start-codex-with-clash.bat`，或改回从普通入口启动 Codex.app |

macOS 清理当前图形会话变量：

```bash
launchctl unsetenv HTTP_PROXY
launchctl unsetenv HTTPS_PROXY
launchctl unsetenv ALL_PROXY
launchctl unsetenv http_proxy
launchctl unsetenv https_proxy
launchctl unsetenv all_proxy
launchctl unsetenv NO_PROXY
launchctl unsetenv no_proxy
```

## 常见问题

| 问题 | 原因 | 处理 |
|------|------|------|
| 终端 `codex` 走代理，但 Codex.app 不走 | `~/.zshrc` 只影响终端 | macOS 用 `launchctl setenv` 或 `LaunchAgent` |
| 设置后 Codex.app 仍不走代理 | 应用已在设置前启动 | 完全退出后重新打开 |
| 重启后失效 | 只做了临时 `launchctl setenv` | macOS 增加 `LaunchAgent` |
| Clash 端口变了 | 配置仍写旧端口 | 把所有旧端口改成新端口 |
| Windows 双击启动器提示端口不可达 | Clash 未运行或端口不对 | 打开 Clash，或用 `start-codex-with-clash.bat <端口>` |
| 不想影响其它图形应用 | macOS `launchctl setenv` 会影响之后启动的图形应用 | 只配置 Codex CLI，或在使用完后清理 `launchctl` 环境变量 |
