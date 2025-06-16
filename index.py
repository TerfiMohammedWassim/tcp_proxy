import sys 
import socket
import threading


hex_filter = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src,length=16,show=True):
    if isinstance(src,bytes):
        src = src.decode()
    result = list()
    for i in range(0,len(src),length):
        word = str(src[i:i+length])
        hexa = ' '.join([f'{ord(c):02x}' for c in word])
        printable = ''.join([c if c in hex_filter else '.' for c in word])
        hexa_width = length * 3
        result.append(f'{i:04x}  {hexa:<{hexa_width}}  {printable}')
    
    if show:
        for line in result:
            print(line)
    else:
        return '\n'.join(result)

def recieve_from(connection):
    buffer = b''
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        if str(e) != 'timed out':
            print(f'Error receiving data: {e}')
    finally:
        connection.settimeout(None)
        return buffer
    
    
def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

def proxy_handler(client_socket,remote_host,remote_port):
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    
    while True:
        client_buffer = recieve_from(client_socket)
        if not client_buffer:
            break
        
        client_buffer = request_handler(client_buffer)
        
        remote_socket.send(client_buffer)
        
        remote_buffer = recieve_from(remote_socket)
        
        if not remote_buffer:
            break
        
        remote_buffer = response_handler(remote_buffer)
        
        
        client_socket.send(remote_buffer)
    
    client_socket.close()
    remote_socket.close()
    
def start_proxy(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(5)
    print(f'[*] Listening on {local_host}:{local_port}')
    
    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accepted connection from {addr}')
        
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()
        print(f'[*] Active connections: {threading.activeCount() - 1}')
        
def main():
    if len(sys.argv) != 5:
        print("Usage: python index.py <local_host> <local_port> <remote_host> <remote_port>")
        sys.exit(1)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    start_proxy(local_host, local_port, remote_host, remote_port)
    
if __name__ == "__main__":
    main()
