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
