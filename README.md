# Mission Control Dashboard

Mission Control Dashboard for our TVs at the office.

## Running

To run or update your local environment you can run:

    $ docker-compose build
    $ docker-compose up

It will rebuild you image, since Docker has a cache mechanism it will take
less than building the image for the first time.


## Commands

To run any command on the app container you can do:

    $ docker exec -it missioncontroldashboard_web_1 ./manage.py shell_plus
    $ docker exec -it missioncontroldashboard_web_1 bash

## Deployment

On your production server do:

    $ virtualenv -p python3 mission_control_dashboard_app
    $ cd mission_control_dashboard_app
    # clone the repository
    $ source bin/activate
    $ pip install -r mission-control-dashboard/requirements.txt

Create the file ```app/local_settings.py``` with:

    $ vim app/local_settings.py

```
SECRET_KEY = 'this-is-so-secret'

DEBUG = False

ALLOWED_HOSTS = ['dashboard.mycompany.com']

RAVEN_CONFIG = {
    'dsn': 'your-sentry-dsn',
}

ZENDESK_URL = 'https://{mycompany}.zendesk.com/api/v2/views/{view-id}/count.json'
ZENDESK_EMAIL = '{email}/token'
ZENDESK_API = '{apikey}'

SENTRY_URL = 'http://sentry.com/api/0/organizations/{mycompany}/stats/'
SENTRY_KEY = '{apikey}'
```

Then run the management commands:

    $ ./manage.py migrate
    $ ./manage.py collectstatic --noinput

As root (or sudo) create the service:

    $ vim /etc/init/gunicorn_mission_control.conf

```
description "Gunicorn Mission Control Dashboard"

start on (filesystem)
stop on runlevel [016]

respawn
setuid deploy
setgid www-data
chdir /opt/deploy/mission_control_dashboard_app/mission-control-dashboard/

exec /opt/deploy/mission_control_dashboard_app/bin/gunicorn --bind 0.0.0.0:6000 -w 3 app.wsgi
```

Start the service:
    $ service gunicorn_mission_control start

Create your nginx site file as:

```
server {
    listen       80;
    server_name  dashboard.mycompany.com;
    charset      utf-8;

    client_max_body_size       10m;
    client_body_buffer_size    128k;

    location /static/ {
        alias /opt/deploy/mission_control_dashboard_app/mission-control-dashboard/static/;
    }

    location / {
        proxy_pass         http://127.0.0.1:6000;
        proxy_redirect     off;

        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    }

}
```

And dance!
