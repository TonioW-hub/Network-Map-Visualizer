import socket

ports = [22, 80, 443, 3389, 8080]
for i in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    result = s.connect_ex(("192.168.1.254", i))
    s.close()
    if result == 0:
        print(f"Port {i} ouvert")
        break