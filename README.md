# ikuuu
ikuuu每日签到

# 使用教程

1. 打开青龙面板，脚本管理 -> 新建空文件夹（文件名 `ikuu`，父目录为空）-> 新建空文件（文件名 `main.py`，父目录 `ikuu`）。

2. 依赖管理 -> 添加 Python 依赖：`requests` `cryptography` `pyOpenSSL` `certifi`。

3. 定时任务 -> 添加任务（命令：`/ql/data/scripts/ikuu/main.py`，定时规则：`0 9 * * *`）。

4. 环境变量 -> 新建变量。

   - 如果使用 `main.py` 的登录签到方式，配置以下三个变量：
     - `EMAIL`：邮箱
     - `PASSWD`：密码
     - `SCKEY`：server酱密钥

   - 如果使用 `ikuuu_checkin_from_curl.py` 的直接签到方式，配置以下变量：
     - `IKUUU_RAW_REQUEST`

     变量内容直接填写点击签到后浏览器抓包 "https://ikuuu.win/user/checkin" 得到的 cookie 字符串，例下图：
<img width="550" height="319" alt="image" src="https://github.com/user-attachments/assets/d67cbdc6-2fd9-4841-91d3-e0de576f338a" />




5. 定时任务 -> 执行（查看日志是否成功）。

# 最新域名

如果登录失败，更新 `main.py` 的最新域名即可。

[iKuuuVPN最新域名](https://ikuuu.club/)
