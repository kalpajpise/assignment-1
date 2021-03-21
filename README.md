# ABG - Assignment


## About 
***
Build 2 python apps - Django based, where query-server will hold data IFSC data in-memory. We need to
invoke the APIs from the REST Client (postman or CURL). 
***

## Technologies and Tools

- TextEditor - PyCharm
- Python - 3.9.2
- Pip - 20.1.1
- Django
- Django Rest Framework
- Development OS - Window 10 and Linux

## Requirements

- If Operating System is Linux - Install redis server and run on port 6739 and database = 0 (Default)
```cmd
# Install Redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/

# To start redis-server
redis-server

# To start a client session
redis-cli -h 127.0.0.1 -p 6379
```
Reference: https://redis.io/topics/quickstart
  
## Initial Setup

Clone the repository and initialize the virtual environment
```cmd
git clone https://github.com/kalpajpise/assignment-1.git

cd assignment-1
```
For Linux Operating System
```cmd
python3 -m venv venv

source venv\Scripts\activate # to activate the Virtual Environment

redis-server (default port 6379, host - 127.0.0.1) # Initialize the redis server

python3 run.py # Automated scripts install requirements 
```
Run Client Server on port 80 <br>
Run  Query Server on port 8000<br>

For Window Operating System
```cmd
python -m venv venv

venv\Scripts\activate # to activate the Virtual Environment

python run.py # Automated scripts install requirements 
```
