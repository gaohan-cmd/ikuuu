# ikuuu
ikuuu每日签到
# 使用教程
  1、打开青龙面板，脚本管理-》新建空文件夹（文件名ikuu，父目录为空）-》新建空文件（文件名main.py，父目录ikuu)
  
  2、依赖管理-》添加python依赖（requests cryptography pyOpenSSL certifi）
  
  3、定时任务-》添加任务（命令：	/ql/data/scripts/ikuu/main.py 定时规则：0 9 * * *）
  
  4、环境变量-》新建变量（新建三个变量，名称为：EMAIL、PASSWD、SCKEY，对应分别为邮箱、密码、server酱密钥）
  
  5、定时任务-》执行（查看日志是否成功）
