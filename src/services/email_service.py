#!/usr/bin/env python

from flask import current_app
from flask_mail import Mail, Message
from threading import Thread
from collections import namedtuple


mail = Mail()


def create_email_attachment(filename):
    with open(filename, 'rb') as fd:
        Att = namedtuple('att', ['data', 'content_type', 'filename',
                                 'disposition'])
        att = Att(data=fd.read(), content_type='application/octet-stream',
                  filename=filename,
                  disposition='attachment; filename="' + filename + '"')
        return att


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject=None, body=None, attachments=None, cc=None, bcc=None,
               sender=None):
    if not sender:
        sender = current_app.config['MAIL_DEFAULT_SENDER']
    msg = Message(subject, recipients=to, cc=cc,
                  bcc=bcc, sender=sender)
    msg.html = body
    if attachments:
        for att in attachments:
            msg.attach(filename=att.filename, content_type=att.content_type,
                       data=att.data, disposition=att.disposition)

    thr = Thread(target=send_async_email,
                 args=[current_app._get_current_object(), msg])
    thr.start()
