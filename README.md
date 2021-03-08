# virtual-dma
Create customised virtual orderbooks, test trades and algos in a fully manipulable live environment

### Dependencies
* Python 3.9 or higher
* [socket](https://docs.python.org/3/library/socket.html) for Python

### Usage

VirtualDMA's OrderBook implementation runs as a server instance on your machine. Simply connect to the opened port and send FIX messages as if it were a standard FIX hub.

An example of a login and the resulting ack, on port 4206:

```
T2-MBP% telnet localhost 4206
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
8=FIX 4.4^9=122^35=A^49=BuySide^56=SellSide^34=1^52=20190605-11:51:27.848^1128=9^98=0^108=30^141=Y^553=BuySideUser^554=BuyPassword^1137=9^10=079^
8=FIX 4.4^9=122^35=A^49=SellSide^56=BuySide^34=1^52=20190605-11:51:28.162^1128=9^98=0^108=30^141=Y^553=BuySideUser^1137=9^10=079^
```