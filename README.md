# 🧰 TCP Proxy

A simple, customizable TCP proxy tool written in Python 🐍.  
It allows you to intercept, analyze, and modify network traffic between a client and a server. Useful for debugging, learning, and testing network protocols!

---

## 🚀 Features

- 🔄 Bidirectional TCP forwarding
- 📝 Hexdump of traffic for inspection
- 🧩 Easy request/response modification
- 🤖 Multi-threaded handling of multiple clients
- 🛠️ Simple command-line interface

---

## 🛠️ Usage

```bash
python index.py [localhost] [localport] [remotehost] [remoteport] [receive_first]
```

### Example

```bash
python index.py 127.0.0.1 9000 10.12.132.1 9000 True
```

- `localhost`: IP address to listen on (e.g., 127.0.0.1)
- `localport`: Port to listen on (e.g., 9000)
- `remotehost`: Remote server IP to forward traffic to
- `remoteport`: Remote server port
- `receive_first`: `True` if the proxy should receive data from the remote server first

---

## 🧐 How it Works

1. Listens for incoming TCP connections on the specified local address.
2. Forwards data between the client and the remote server.
3. Prints a hexdump of all data sent and received.
4. Allows you to modify data in transit by editing the `request_handler` and `response_handler` functions.

---

## 🏗️ Customization

Want to manipulate requests/responses?  
Edit the following functions in `index.py`:

```python
def request_handler(buffer):
    # Modify requests here
    return buffer

def response_handler(buffer):
    # Modify responses here
    return buffer
```

---

## ⚠️ Disclaimer

This tool is intended for educational and debugging purposes.  
Do not use it for malicious activities! 🚫

---

## 📄 License

MIT License

---

## 👨‍💻 Author

- [@TerfiMohammedWassim](https://github.com/TerfiMohammedWassim)
