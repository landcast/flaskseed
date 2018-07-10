import socket
import os
import signal

from tempfile import NamedTemporaryFile
import subprocess
from jinja2 import Environment
from jinja2 import FileSystemLoader


CHROME_PATH = None
if os.path.exists('/usr/bin/chrome-browser'):
    CHROME_PATH = 'chrome-browser'
elif os.path.exists('/usr/bin/chromium-browser'):
    CHROME_PATH = 'chromium-browser'
elif os.path.exists('/usr/bin/google-chrome'):
    CHROME_PATH = 'google-chrome'


def get_chrome_args():
    return [
        CHROME_PATH,
        '--no-sandbox',  # Avoids permission issues while dockerized.
        '--headless',
        '--disable-extensions',  # Reduces startup overhead.
        '--disable-gpu',  # Required by chrome's headless mode for now.
    ]


def generate_pdf_from_template(html_template, params, pdf_filename):
    env = Environment(loader=FileSystemLoader('./pdf_templates', 'utf-8'))
    template = env.get_template(html_template)
    html_str = template.render(**params)
    print(html_str)
    return generate_pdf(html_str, pdf_filename)


def generate_pdf(html_str, pdf_filename):
    f = NamedTemporaryFile(delete=False)
    f.write(html_str.encode('utf-8'))
    f.close()
    os.rename(f.name, f.name + '.html')
    chrome_args = get_chrome_args()
    chrome_args.append(
        '--print-to-pdf="{}"'.format(pdf_filename),
    )
    chrome_args.append(f.name)
    status_code, output = subprocess.getstatusoutput(" ".join(chrome_args))
    return status_code, output


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
    print(pid_file_path)
    if os.path.exists("./" + pid_file_path):
        try:
            pidfile = open(pid_file_path, 'r')
            old_pid = pidfile.read()
            print(old_pid, os.getppid())
            pidfile.close()
            # kill the process
            if not os.getppid() == int(old_pid):
                os.kill(int(old_pid), signal.SIGKILL)
                print('kill ' + old_pid + ', started ' + str(pid))
                os.remove(pid_file_path)
                with open(pid_file_path, 'w') as newpidfile:
                    newpidfile.write(str(pid))
            else:
                print('flaskseed.pid refer to current process parent id,'
                    ' ignore kill action')
        except ProcessLookupError as e:
            # app.logger.debug(old_pid + ' process already killed', e)
            pass
    else:
        print('not found pid file, start new server')
        with open(pid_file_path, 'w') as pidfile:
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