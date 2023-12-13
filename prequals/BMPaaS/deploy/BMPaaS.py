import base64
import os


FLAG = base64.b85encode(open("flag.bmp", "rb").read()).decode()

CHARSET = base64._b85alphabet.decode()
N = len(CHARSET)


def generate_key(length):
    random_stream = os.urandom(length)
    return "".join(CHARSET[x % N] for x in random_stream)


def encrypt(plaintext, key):
    ciphertext = ""
    for i in range(len(plaintext)):
        ciphertext += CHARSET[(CHARSET.find(plaintext[i]) + CHARSET.find(key[i])) % N]
    return ciphertext


print("[+] Welcome to BMPaaS!")
print("[+] We offer a military-grade BMP encryption algorithm, powered by one of the safest OTP mechanisms in the world.")
print("[+] For now, uploading new BMP files is disabled. However, you can challenge our security by requesting an encrypted flag ;)\n")

print("[1] Request a new encrypted flag")
print("[2] Exit\n")

while True:

    choice = input("[?] Enter your choice: ")

    if choice == "1":
        key = generate_key(len(FLAG))
        print(encrypt(FLAG, key))

    elif choice == "2":
        exit()

    else:
        print("[x] Invalid choice.")
