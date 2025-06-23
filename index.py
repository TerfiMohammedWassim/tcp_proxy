import sys 
import socket
import threading


hex_filter = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src,length=16,show = True):
    if isinstance(src,bytes):
        src = src.decode()
    result = list()
    for i in range(0,len(src),length):
        word = str(src[i:i+length])
        hexa = ' '.join([f'{ord(c):02x}' for c in word])
        printable = ''.join([c if c in hex_filter else '.' for c in word])
        result.append(f'{i:04x}  {hexa:<{length*3}}  {printable}')
    if show: 
        print('\n'.join(result))
    return '\n'.join(result)


def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except socket.timeout:
        pass
    except Exception as e:
        print(f"Error receiving data: {e}")
    return buffer


def request_handler(buffer):
    # Modify requests here
    return buffer


def response_handler(buffer):
    # Modify responses here
    return buffer


def proxy_handler(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        remote_socket.connect((remote_host, remote_port))
        
        while True:
            # Receive data from client
            local_buffer = receive_from(client_socket)
            if len(local_buffer):
                print(f"[<==] Received {len(local_buffer)} bytes from localhost.")
                hexdump(local_buffer)
                
                # Send to remote server
                local_buffer = request_handler(local_buffer)
                remote_socket.send(local_buffer)
                print(f"[==>] Sent to remote.")
            
            # Receive response from remote server
            remote_buffer = receive_from(remote_socket)
            if len(remote_buffer):
                print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
                hexdump(remote_buffer)
                
                # Send to client
                remote_buffer = response_handler(remote_buffer)
                client_socket.send(remote_buffer)
                print(f"[==>] Sent to localhost.")
            
            # If no data from either side, break
            if not len(local_buffer) and not len(remote_buffer):
                break
                
    except Exception as e:
        print(f"[!!] Exception: {e}")
    finally:
        client_socket.close()
        remote_socket.close()


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
        print(f"[*] Listening on {local_host}:{local_port}")
        server.listen(5)
        
        while True:
            client_socket, addr = server.accept()
            print(f"[==>] Received incoming connection from {addr[0]}:{addr[1]}")
            
            proxy_thread = threading.Thread(
                target=proxy_handler,
                args=(client_socket, remote_host, remote_port)
            )
            proxy_thread.start()
            
    except Exception as e:
        print(f'[!!] Problem on bind: {e}')
        print(f"[!!] Failed to listen on {local_host}:{local_port}")
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
        
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = "True" in sys.argv[5]
    
    print(f"[*] Starting proxy {local_host}:{local_port} -> {remote_host}:{remote_port}")
    print(f"[*] Receive first: {receive_first}")
    
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()