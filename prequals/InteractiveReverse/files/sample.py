
import pwn
import base64

SERVER_ADDRESS = ?
SERVER_PORT = ?

with open("prog.bin", "rb") as f:
    program = f.read()

r = pwn.remote(SERVER_ADDRESS, SERVER_PORT)

r.sendline("-----PROGRAM START-----")
r.sendline(base64.b64encode(program))
r.sendline("-----PROGRAM END-----")

r.interactive()
