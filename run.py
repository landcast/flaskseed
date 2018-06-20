#!/usr/bin/env python

# used to start the created app

from src import create_app
from config import settings
import optparse
from src.utils import setup_pid_file


def process_options(config, default_host="0.0.0.0",
                    default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """
    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " +
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-E", "--eshost",
                      help="Host of elastic IP which only used by front-end, "
                           "not for binding")
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " +
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    if options.eshost:
        config.ESHOST = options.eshost
        # print('config.ESHOST=', config.ESHOST)
    if options.host:
        config.HOST = options.host
    if options.eshost:
        config.PORT = options.port
    return options



# build options to setup config
options = process_options(settings)
# create app using config, keep create_app in global' reason is to support
# the "flask * *" command, such as "flask db init"
app = create_app(settings)


if __name__ == '__main__':
    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                          restrictions=[30])
        options.debug = True
    # run app
    setup_pid_file(app)
    app.run(
        host=options.host,
        port=int(options.port)
    )
