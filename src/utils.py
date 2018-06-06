import socket


def free_port_no(host):
    """
    Get a free port no from system, by bind(host, 0)
    :param host: host name
    :return: found free port no
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def test_url(path, host='localhost', port=5000):
    return 'http://' + host + ':' + str(port) + path