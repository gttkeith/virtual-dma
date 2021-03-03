import asyncio
import websockets

PORT = 21293
NAME = "OrderBook"

SOH = '^'
STX = '='

D_MAP = {
    '54': {
        '1': 'Buy',
        '2': 'Sell'
    },
    '59': {
        '0': 'Day',
        '1': 'GTC',
        '2': 'At Open',
        '3': 'IOC',
        '4': 'FOK',
        '5': 'GTX',
        '6': 'GTD',
        '7': 'At Close'
    }
}

sent = []
received = []
logged_in = []

# customisable FIX flow
def send(network, fix_dict):
    # autofill field 9
    if fix_dict['9'] == '-':
        f9 = 0
        incl = False
        for k,v in fix_dict.items():
            if k == '10':
                incl = False
            if incl:
                f9 += len(SOH)+len(STX)+len(k)+len(v)
            if k == '9':
                incl = True
        fix_dict['9'] = f9
    fix_str = dict_to_fixmsg(fix_dict)
    print(f"[{NAME}] SENDING: {fix_str}")
    sent.append(fix_dict)
    network[fix_dict['56']].receive(network, fix_str)

def receive(network, fix_str):
    print(f"[{NAME}] RECEIVED: {fix_str}")
    fix_dict = fixmsg_to_dict(fix_str)
    received.append(fix_dict)
    if fix_dict['35'] == 'A': # login
        if len(sent)==0 or sent[-1]['35'] != 'A':
            print(f"[{NAME}] CLIENT LOGIN: {fix_dict['553']}")
            logged_in.append(fix_dict['553'])
            print(f"[{NAME}] PREPARING ACK.")
            ack_dict = fix_dict.copy()
            ack_dict.update({'49':fix_dict['56'],'56':fix_dict['49']}) # swap send and receive
            send(network, ack_dict)
        else:
            print(f"[{NAME}] ACK RECEIVED. SESSION OPEN.")
    elif fix_dict['35'] == '5': # logout
        if len(sent)==0 or sent[-1]['35'] != '5':
            print(f"[{NAME}] CLIENT LOGOUT: {fix_dict['49']}")
            print(f"[{NAME}] PREPARING ACK.")
            ack_dict = fix_dict.copy()
            ack_dict.update({'49':fix_dict['56'],'56':fix_dict['49']}) # swap send and receive
            send(network, ack_dict)
        else:
            print(f"[{NAME}] ACK RECEIVED. SESSION CLOSED.")
            logged_in = [v for v in logged_in if v != fix_dict['49']]
    elif fix_dict['35'] == 'D':
        print(f"[{NAME}] NEW ORDER ({fix_dict['11']}): {D_MAP['54'][fix_dict['54']]} {fix_dict['53']}x of {fix_dict['48']} @ {fix_dict['15']}{fix_dict['44']}, {D_MAP['59'][fix_dict['59']]}")
        # (perform risk checks and) send accepted execution report
        print(f"[{NAME}] ORDER ACCEPTED AND WORKING. PREPARING EXECUTION REPORT.")
        return_dict = fix_dict.copy()
        return_dict['35'] = '8' # execution report
        return_dict['39'] = '2' # no executions yet
        return_dict['150'] = '0' # new
        return_dict.update({'49':fix_dict['56'],'56':fix_dict['49']}) # swap send and receive
        send(network, return_dict)
    elif fix_dict['35'] == '8':
        if fix_dict['150'] == '0' and fix_dict['39'] == '2':
            print(f"[{NAME}] EXECUTION REPORT RECEIVED. BUYSIDE IS AWARE THAT NEW ORDER IS ACTIVE.")

def dict_to_fixmsg(fix_dict):
    fix_str = ''
    for k,v in fix_dict.items():
        fix_str += str(k)+STX+str(v)+SOH
    return fix_str[:-len(SOH)]

def fixmsg_to_dict(fix_str):
    if fix_str[-len(SOH):]==SOH:
        fix_str = fix_str[:-len(SOH)]
    return dict(s.split(STX) for s in fix_str.split(SOH))

async def main(websocket, path):
    msg = await websocket.recv()
    result = receive(msg)
    await websocket.send(result)

start_server = websockets.serve(main, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()