# Phoenix 完整迁移备份

## 2026-11-14 豆浆人格增量更新

`updates/` 中保存最新人格的 AES-256-GCM 加密补丁，沿用原 Phoenix 恢复密钥。更新包含自然拌嘴、情绪表达、回复长短和关心边界的调整。密钥和人格明文均不上传。

先按下文恢复完整备份，再在复制到新电脑前执行：

```powershell
python updates/restore_persona.py --key-file PHOENIX-RECOVERY-KEY.txt --dsh-home E:\Phoenix-restored\restored\dsh-home
```

也可将 `--dsh-home` 指向实际 `.dsh` 目录。恢复前会保留原人格副本；若同名备份已存在会停止，避免覆盖。此补丁只更新人格，不更新聊天历史或插件代码。


本仓库是公开仓库，所有私人数据均采用 AES-256-GCM 加密，保存在 Release 附件。**必须另外保管 PHOENIX-RECOVERY-KEY.txt，密钥不会上传到 GitHub；丢失后无法恢复。**

备份范围：整个 E:\qqbot 工作区、整个用户 .dsh（含已安装插件及依赖、插件数据、记忆、人格、图片、附件、会话消息历史、账号配置）、整个 DeepSeek Harness 安装目录、桌面 Electron 用户数据。包含隐藏文件和子目录。不是整个操作系统或 QQ 客户端安装目录的镜像。

## 换电脑恢复（Windows）

1. 下载仓库，安装 Python 3.12 或更新版本，运行 `python -m pip install cryptography requests`。
2. 从旧电脑单独复制 `PHOENIX-RECOVERY-KEY.txt` 到仓库目录，避免把密钥提交到 GitHub。
3. 运行 `python restore.py --key-file PHOENIX-RECOVERY-KEY.txt --output E:\Phoenix-restored`。工具自动下载所有 Release 分卷，验证 SHA256、解密、验证 ZIP 并解压。
4. 完全退出目标电脑的 DSH 后，将 `dsh-home` 内容复制到新用户的 `%USERPROFILE%\.dsh`，将 `workspace` 内容放到 `E:\qqbot`，将 `application` 内容放到 `E:\app\deepseek`。若盘符不同，需要调整插件配置中保存的绝对路径。
5. 将 `desktop-data` 复制到 `%APPDATA%\@deepseek-ai\dsh-desktop`。先保留新电脑原数据的备份，再合并迁移数据。
6. 运行恢复出的 `DeepSeek Harness.exe`。跨电脑受 Windows 账户加密保护的登录状态或 QQ 登录可能需要重新登录。SnowLuma 依赖单独安装和登录 QQ，不能保证 QQ 会话跨设备继续有效。

这是运行中的逐文件快照，详细的无法读取文件和读取期间变化文件记录位于解压后的 `backup-report.json`。系统锁文件通常不需要恢复；如果业务文件发生变化，可能需要在应用空闲时补备。不会自动启动机器人或发送消息。

恢复工具默认读取 `backup-20261108-2309` Release。请同时保存仓库、Release 附件和密钥。普通 git clone 不会下载 Release 附件，恢复工具会自动下载。分卷下载和上传均经过 SHA256 校验。
