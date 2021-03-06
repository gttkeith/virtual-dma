import asyncio
import socket

SOH = '^'
STX = '='

TCP_IP_PORT = ('127.0.0.1', 4213)
BUFFER_SIZE = 256
MAX_CONNECTIONS = 1

pending_msgs = []

async def receive():
    s = ''
    try:
        s = conn.recv(BUFFER_SIZE).decode().strip()
    except UnicodeDecodeError:
        pass
    if s:
        pending_msgs.append(s)
        print("RECEIVED: "+s)

def send(s):
    conn.send(str.encode(str(s)))

async def simple_reply(s):
    s = str(s)
    send("You said: "+s+"\n")
    print("Replied:", s)

async def main():
    while True:
        await receive()
        if len(pending_msgs)>0:
            await simple_reply(pending_msgs.pop(0))

def dict_to_fixmsg(fix_dict):
    fix_str = ''
    for k,v in fix_dict.items():
        fix_str += str(k)+STX+str(v)+SOH
    return fix_str[:-len(SOH)]

def fixmsg_to_dict(fix_str):
    if fix_str[-len(SOH):]==SOH:
        fix_str = fix_str[:-len(SOH)]
    return dict(s.split(STX) for s in fix_str.split(SOH))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(TCP_IP_PORT)
server.listen(MAX_CONNECTIONS)
conn, addr = server.accept()

print('Server IP:', addr[0])
print('Server Port:', addr[1])

asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()