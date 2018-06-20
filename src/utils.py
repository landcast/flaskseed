import socket
import os
import signal


def setup_pid_file(app):
    """
    check pid file configured by PID_FILE in app config,
    if exists, get old process id from file and kill it, then write the new
    process id into it.
    if not exist, write the new process id directly into it.
    :return:
    """
    pid = os.getpid()
    pid_file_path = app.config['PID_FILE'] + ".pid"
    if os.path.exists(pid_file_path):
        with open(pid_file_path, 'r+') as pidfile:
            old_pid = pidfile.read()
            # kill the process
            try:
                if not os.getppid() == int(old_pid):
                    os.kill(int(old_pid), signal.SIGKILL)
                    app.logger.debug(
                        'kill ' + old_pid + ', started ' + str(pid))
                else:
                    app.logger.debug(
                        'flaskseed.pid refer to current process parent id,'
                        ' ignore kill action')
            except ProcessLookupError as e:
                # app.logger.debug(old_pid + ' process already killed', e)
                pass
            # move file teller to start
            pidfile.seek(0, 0)
            pidfile.write(str(pid))
    else:
        with open(pid_file_path, 'a+') as pidfile:
            pidfile.write(str(pid))


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