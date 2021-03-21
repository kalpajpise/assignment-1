import os
import shutil
import time
import requests
import subprocess
import platform

start_time = time.time()
TERMINAL_WIDTH = shutil.get_terminal_size((80, 20)).columns
BASE_URL_SERVER1 = 'http://127.0.0.1:8000/api/'
BASE_URL_SERVER2 = 'http://127.0.0.1:80/api/'

def main():


    print("Installing packages".center(TERMINAL_WIDTH, "-"))
    os.system("pip install -r requirements.txt")

    print("Setting up Query Server - Flask Server".center(TERMINAL_WIDTH,'-'))
    os.chdir('query-server')
    print("Deleting OLD DB file".center(TERMINAL_WIDTH, "-"))
    DB_FILE_PATH = os.path.join(os.getcwd(), "db.sqlite3")
    if os.path.exists(DB_FILE_PATH):
        os.remove(os.path.join(os.getcwd(), "db.sqlite3"))

    print("Removing Migrations".center(TERMINAL_WIDTH, "-"))
    if os.path.exists('flask/migrations'):
        shutil.rmtree('flask/migrations')

    print("Making User Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} makemigrations flask".format(os.path.join(os.getcwd(), "manage.py")))

    print("Migrating Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} migrate".format(os.path.join(os.getcwd(), "manage.py")))

    print("Setting up Client Server -- django server".center(TERMINAL_WIDTH, "-"))
    os.chdir('../')

    os.chdir('client-server')
    print("Deleting OLD DB file".center(TERMINAL_WIDTH, "-"))
    DB_FILE_PATH = os.path.join(os.getcwd(), "db.sqlite3")
    if os.path.exists(DB_FILE_PATH):
        os.remove(os.path.join(os.getcwd(), "db.sqlite3"))

    print("Removing Migrations".center(TERMINAL_WIDTH, "-"))
    if os.path.exists('app_django/migrations'):
        shutil.rmtree('app_django/migrations')

    print("Making User Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} makemigrations app_django".format(os.path.join(os.getcwd(), "manage.py")))

    print("Migrating Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} migrate".format(os.path.join(os.getcwd(), "manage.py")))

    print("Run CLient Server".center(TERMINAL_WIDTH,"-"))
    os.system("start python manage.py runserver 0.0.0.0:80")
    while True:
        try:
            response = requests.get(BASE_URL_SERVER2)
            break
        except:
            print("Reconnecting....")

    os.chdir("../query-server/")

    print("Run Query Server ".center(TERMINAL_WIDTH, "-"))
    os.system("start python manage.py runserver 0.0.0.0:8000")
    while True:
        try:
            response = requests.get(BASE_URL_SERVER1)
            break
        except:
            print("Reconnecting....")

    flavour = platform.system()
    if flavour == 'Windows':
        print("Starting Redis Server".center(TERMINAL_WIDTH, "-"))
        os.chdir('../Redis')
        os.system("start {}\\redis-server.exe".format(os.path.join(os.getcwd())))
    else:
        print("unsupported os type : {} | supported os - Windows,"
              " Hence kindly have a local redis server running on port 6379".format(flavour))

    # subprocess.call(["{}\\redis-server.exe".format(os.path.join(os.getcwd()))])
    print("ALl DONE".center(TERMINAL_WIDTH, "-"))


if __name__ == "__main__":
    main()
    print("--- Completed in {} seconds ---".format(time.time() - start_time))
