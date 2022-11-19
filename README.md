# Ip-based-Udp-Proxy
Udp proxy that doesnt use hostname. Just an ip and a port. 

# How to use.
1. Know the ip and port of the server you are trying to connect to
2. Make that ip point to your loopback interface with `netsh int ip add address "Loopback" <ip>`
3. Obtain your local ip on your network interface/non loopback interface using ifconfig/ipconfig
4. Open proxy.py, and change the parameters to your local_ip, remote_ip and the port
