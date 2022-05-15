# API FOR BOOK
## Getting Started
## Contents

1. Project detail
2. Installing Dependencies
3. Project setup

# 1-Project detail
This project is a class project given us by Mr OURO. The goals of this project can be summarized in these points:
- You need to build your API using python Flask / base
Postgres data
- You should document your API specifying the responses you
get after running each endpoint
- Deploy your API on the Heroku Cloud Platform

# 2-Installing Dependencies

#### Python version used
Python 3.10.4
Follow instructions to install the latest version of python for your platform (windows link there) on [python official web site](https://www.python.org/downloads/)
#### pip version used
pip 22.1 from C:\Users\Sidewinder\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)
Follow instructions to install the latest version of python for your platform on [pip official web site](https://pip.pypa.io/en/stable/cli/pip_download/)
#### Packages used
The requiered package.txt inside the tree structure contains all the requierd packages you need to use the API.


```bash
BOOK-API/
|----.gitignore
|----API_BIBLIOTHEQUE.postman_collection.json
|----Bookapi.py
|----README.md
|----requieredpackage.txt 
```

#### Install requieredpackage

```bash
pip install -r requieredpackage.txt 
or
pip3 install -r requieredpackage.txt 
```
#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

You can also use python extension for vscode if you are using visual studio code. you can find it on [vs code market place](https://marketplace.visualstudio.com/items?itemName=ms-python.python ) 


# 3- Project setup

#### Database setup
The project were made with postgres sql as database. You can use whatever database you want cause we used SQLAlchemy, an ORM of Flask. Check out the [official web site](https://www.sqlalchemy.org/). You just need to proceed  according to the [documentaition](https://docs.sqlalchemy.org/en/14/)  

### API reference
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://localhost:5000; which is set as a proxy in frontend configuration.

### Errors Handling
Errors are retourned as JSON objects in the following format: { "success":False "error": 400 "message":"Bad request }

The API will return four error types when requests fail: . 400: Bad request . 500: Internal server error . 422: Unprocessable . 404: Not found
