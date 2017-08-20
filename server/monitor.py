import os
import json
import smtplib
import dateutil.parser
from datetime import datetime, timedelta


CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'config.json'
)


def read_config():
    with open(CONFIG_FILE_PATH, 'r') as f:
        return json.load(f)


def send_mail(user, password, to_mails, subject, body):
    message = 'From: {0}\nTo: {1}\nSubject: {2}\n\n{3}'.format(
        user,
        ", ".join(to_mails),
        subject,
        body
    )
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(user, to_mails, message)
        server.close()
        print('Email sent: {0}'.format(subject))
    except Exception as e:
        print('Failed to send Email')
        print(e)


if __name__ == '__main__':
    config = read_config()
    last_called_date = dateutil.parser.parse(config['last_called_at'])

    if datetime.utcnow() - last_called_date > timedelta(minutes=10):
        send_mail(
            config['error_email']['from_email'],
            config['error_email']['from_password'],
            config['error_email']['to_emails'],
            '[IMPORTANTE] Dispositivo sin contacto',
            'No se ha recivido contacto del dispositivo hace mas de 10 minutos.'
        )
