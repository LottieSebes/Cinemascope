# cinemascope

1. install requirements

    $ sudo aptitude install build-essential python-dev python-smbus virtualenv

2. enable SPI feature on raspberry pi

    $ sudo raspi-config

3. create virtual environment

    $ virtualenv venv

4. activate virtual environment

    $ source venv/bin/activate

5. install dependencies

    $ pip install -r requirements.txt
