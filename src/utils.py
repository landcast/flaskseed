import socket


def free_port_no(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def test_url(path, host='localhost', port=5000):
    return 'http://' + host + ':' + str(port) + path