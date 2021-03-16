import asyncio
import socket
from fix_mapping import *

# FIX formatting params
SOH = '^'
STX = '='

TCP_IP_PORT = ('127.0.0.1', 4206)
BUFFER_SIZE = 256
MAX_CONNECTIONS = 1

pending_msgs = []
received = []
logged_in = {}

async def receive():
    s = ''
    try:
        s = conn.recv(BUFFER_SIZE).decode().strip()
    except UnicodeDecodeError:
        pass
    if s:
        pending_msgs.append(s)
        received.append(s)
        print("RECEIVED: "+s)

def send(s):
    conn.send(str.encode(str(s)))

async def execute_fix(s):
    s_dict = fixmsg_to_dict(s)
    response = exec(MSG_TYPES[s_dict[MSG_TYPE]]+'('+str(s_dict)+')')
    if not response.get(BODY_LENGTH): # autofill body length
        body_length = 0
        incl = False
        for k,v in response.items():
            if k == CHECKSUM:
                incl = False
            if incl:
                body_length += len(SOH)+len(STX)+len(k)+len(v)
            if k == BODY_LENGTH:
                incl = True
        response[BODY_LENGTH] = body_length
    send(dict_to_fixmsg(s)+"\n")

def logon(fix_dict):
    logged_in[fix_dict[SENDER]] = fix_dict[USERNAME]
    print(f"LOGGED ON: {fix_dict[USERNAME]}")
    return cc(fix_dict)

def logout(fix_dict):
    logged_in.pop(fix_dict[SENDER])
    print(f"LOGGED OUT: {fix_dict[SENDER]}")
    r_dict = cc(fix_dict)
    r_dict.pop(PASSWORD)
    return r_dict

def order(fix_dict):
    print(f"NEW ORDER ({fix_dict[CL_ORD_ID]}): {SUBTYPE_MAP[SIDE][fix_dict[SIDE]]} {fix_dict[QTY]}x of {fix_dict[SECURITY_ID]} @ {fix_dict[CURRENCY]}{fix_dict[{PRICE}]}, {SUBTYPE_MAP[TIME_IN_FORCE][fix_dict[TIME_IN_FORCE]]}")
    return cc(fix_dict)

async def main():
    while True:
        await receive()
        if len(pending_msgs)>0:
            await execute_fix(pending_msgs.pop(0))

def cc(fix_dict, receiver=None):
    cc_dict = fix_dict.copy()
    cc_dict[SENDER] = fix_dict[RECEIVER]
    if receiver:
        cc_dict[RECEIVER] = receiver
    else:
        cc_dict[RECEIVER] = fix_dict[SENDER]
    return cc_dict

def dict_to_fixmsg(fix_dict):
    fix_str = ''
    for k,v in fix_dict.items():
        fix_str += str(k)+STX+str(v)+SOH
    return fix_str[:-len(SOH)]

def fixmsg_to_dict(fix_str):
    if fix_str[-len(SOH):]==SOH:
        fix_str = fix_str[:-len(SOH)]
    return dict(s.split(STX) for s in fix_str.split(SOH))


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(TCP_IP_PORT)
    server.listen(MAX_CONNECTIONS)
    conn, addr = server.accept()

    print('Server IP:', addr[0])
    print('Server Port:', addr[1])

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()