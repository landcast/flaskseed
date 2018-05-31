#!/usr/bin/env python
from ustutor import create_app
import ustutor.config as config


app = create_app(config)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
