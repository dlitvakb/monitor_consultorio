import requests
import smtplib
import json
import os


CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'config.json'
)


def read_config():
    with open(CONFIG_FILE_PATH, 'r') as f:
        return json.load(f)


def write_config(new_config):
    with open(CONFIG_FILE_PATH, 'w') as f:
        f.write(json.dumps(new_config, indent=4))


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

    try:
        response = requests.post(
            '{0}'.format(config['server_url']),
            data={'token': config['last_token']}
        )

        if response.status_code != 200:
            send_mail(
                config['error_email']['from_email'],
                config['error_email']['from_password'],
                config['error_email']['to_emails'],
                'Error recibido del dispositivo',
                'El dispositivo envio el siguiente error: {0}'.format(
                    response.text
                )
            )
        else:
            config['last_token'] = response.json()['next_token']
            write_config(config)
    except requests.ConnectionError:
        try:
            response = requests.get('https://google.com')

            if response:
                send_mail(
                    config['error_email']['from_email'],
                    config['error_email']['from_password'],
                    config['error_email']['to_emails'],
                    '[IMPORTANTE] No es posible conectarse con el servidor',
                    'El dispositivo cuenta con internet, pero no puede conectarse al servidor.'
                )
        except:
            pass
