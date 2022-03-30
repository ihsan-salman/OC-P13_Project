# OC-P13_Project-FavArche  

Need to archive your favorite work ?  
FavArche is the solution at your problem !

#  Installation and requierements 

first of all, download [Python](https://www.python.org/) by going in the official website and choose the version 3.9 ([Python download](https://www.python.org/downloads/)).

then, install [Pip](https://pypi.org/project/pip/) by entering in the terminal the following command line:
```bash
python3 -m pip --version  #for unix
python get-pip.py         #for windows
```
after that, you have the choice to download the zip of the code or clone with the following command Line:
```bash
git clone https://github.com/ihsan-salman/OC-P13_Project.git
```
Create an virtual environment with the following command line:
```bash
python3 -m venv <name of your environment>
```
then activate it with the following command line:
```bash
<name of your environment>\Scripts\activate.bat # for windows
source <name of your environment>/bin/activate # for unix
```
then you need to add some environments variables to make all works good
```bash
For Unix:

export SECRET_KEY=<value of your secret key>
export IP_ADRESS=<value of ip adress> #if you want to use this application with you own server
export DATABASE_USER=<name of your database user>
export DATABASE_PASSWORD=<password of your database user>
export EMAIL_HOST_USER=<your own email adress>
export EMAIL_HOST_PASSWORD=<password of your email adress>
```
For windows, follow this [tutorial](https://phoenixnap.com/kb/windows-set-environment-variable) and add all the variables you need as the top.

finally, use the requirements document by entering the following command in the terminal:
```bash
pip3 install -r requirements.txt      # for unix
pip install -r requirements.txt       # for windows
```

# How to use the program

To start the program, go to this website:
```bash
http://192.241.138.251/
```

Or you can launch the website with Django command:
```bash
cd FavArche        # place in the good file

manage.py runserver          # launch the local server

http://127.0.0.1:8000/       # local url
```
