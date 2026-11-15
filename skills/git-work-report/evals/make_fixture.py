from pathlib import Path
import subprocess, os, sys
p=Path(sys.argv[1]); p.mkdir(parents=True,exist_ok=True)
def git(*args,env=None):
    return subprocess.run(['git','-C',str(p),*args],env=env,check=True,capture_output=True,text=True).stdout
git('init'); git('config','user.name','Demo'); git('config','user.email','me@example.invalid')
rows=[('2026-11-14T23:59:59+08:00','me@example.invalid','fix: 前一天修改'),('2026-11-15T10:00:00+08:00','me@example.invalid','feat: 增加游客模式'),('2026-11-15T11:00:00+08:00','other@example.invalid','feat: 管理后台统计'),('2026-11-15T12:00:00+08:00','me@example.invalid','feat: 强制登录并移除游客模式'),('2026-11-15T13:00:00+08:00','me@example.invalid','test: 补充登录返回验收\n\n后端仍运行旧认证逻辑，待重启后联调。'),('2026-11-16T00:00:00+08:00','me@example.invalid','feat: 次日支付功能')]
for i,(date,email,msg) in enumerate(rows):
    (p/'changes.txt').write_text(msg+'\n')
    git('add','changes.txt')
    env=os.environ.copy(); env.update(GIT_AUTHOR_NAME='Demo',GIT_AUTHOR_EMAIL=email,GIT_AUTHOR_DATE=date,GIT_COMMITTER_DATE=date)
    git('commit','-m',msg,env=env)
print(p)
