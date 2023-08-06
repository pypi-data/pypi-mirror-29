[<img src="logo.png">](https://www.nodedefender.com/)
[NodeDefender](https://www.nodedefender.com) is an Open- Source program for controlling multiple Z-Wave devices connected to multiple gateways.
This programs is exclusivly designed to work with [CTS-iCPE](http://cts-icpe.com). 

## Requirements
NodeDefender is written in Python3 around the Flask framework.
Some of the packages will require compilation which requires python-dev installed on your host. Everything else should be possible to install with pip, either on your host or in virtualenv(recommended).

- Linux System(OSX may work, not tested)
- Git
- Python3
- Python3-dev
- Python-virtualenv

## Installation, Quick step.

1. Clone the repo on your machine
```
git clone https://github.com/CTSNE/NodeDefender.git
```
2. Install virtual- enviroment
```
virtualenv -p python3 py
```
3. Install dependencies
```
./py/bin/pip install -r requirements.txt
```
4. Go through setup- phase
```
./manage.py setup all
```
5. Create, migrate and upgrade Database
```
./manage.py db init
./manage.py db migrate
./manage.py db upgrade
```
6. Create first superuser
```
./manage.py user create
./manage.py role superuser
```
7. Run
```
./run.py
```
## Full documentation

