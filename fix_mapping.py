ACCOUNT = '1'
BODY_LENGTH = '9'
CHECKSUM = '10'
CL_ORD_ID = '11'
CURRENCY = '15'
EXEC_INST = '18'
MSG_TYPE = '35'
ORD_TYPE = '40'
PRICE = '44'
SECURITY_ID = '48'
SENDER = '49'
QTY = '53'
SIDE = '54'
SYMBOL = '55'
RECEIVER = '56'
TIME_IN_FORCE = '59'
USERNAME = '553'
PASSWORD = '554'

MSG_TYPES = {
    '0': "heartbeat",
    '1': "test_request",
    '2': "resend_request",
    '3': "reject",
    '4': "sequence_reset",
    '5': "logout",
    '6': "indication_of_interest",
    '7': "advertisement",
    '8': "execution_report",
    '9': "order_cancel_reject",
    'A': "logon",
    'B': "news",
    'C': "email",
    'D': "order_single",
    'E': "order_list",
    'F': "order_cancel_request",
    'G': "order_cancel_replace_request",
    'H': "order_status_request",
    'J': "allocation",
    'K': "list_cancel_request",
    'L': "list_execute",
    'M': "list_status_request",
    'N': "list_status",
    'P': "allocation_ack",
    'Q': "dont_know_trade",
    'R': "quote_request",
    'S': "quote",
    'T': "settlement_instructions",
    'V': "market_data_request",
    'W': "market_data-snapshot_full_refresh",
    'X': "market_data_incremental_refresh",
    'Y': "market_data_request_reject",
    'Z': "quote_cancel",
    'a': "quote_status_request",
    'b': "quote_acknowledgement",
    'c': "security_definition_request",
    'd': "security_definition",
    'e': "security_status_request",
    'f': "security_status",
    'g': "trading_session_status_request",
    'h': "trading_session_status",
    'i': "mass_quote",
    'j': "business_message_reject",
    'k': "bid_request",
    'l': "bid_response",
    'm': "list_strike_price"
}

SUBTYPE_MAP = {
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