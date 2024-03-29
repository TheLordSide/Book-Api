# API FOR BOOK
## Getting Started
## Contents

1. Project detail
2. Installing Dependencies
3. Project setup
4. Api Endpoints

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

#### API reference
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://localhost:5000; which is set as a proxy in frontend configuration.

#### Errors Handling
Errors are retourned as JSON objects in the following format:

```bash
{
    "response": "Method not allowed",
    "succes": false
}
```

```bash
{
    "response": "Ressource not found",
    "succes": false
}
```

The API will return two errors types when requests fail: 

```bash
. 405: Method not allowed 
. 404: Not found
```

# 4- Api Endpoints
There are 4 HTTP methods used : GET, POST, PATCH, DELETE for Book and Category.

#### GET/book/showallcategories

##### Show all categories

This endpoints returns the list of all categories, success value, Number of saved categories.
the URL based on local server :
```bash
 http://127.0.0.1:5000/book/showallcategories

```

```bash
{
    "Liste de categories": [
        {
            "id": 1,
            "libelle_categorie": "Fiction"
        },
        {
            "id": 2,
            "libelle_categorie": "Horreur"
        },
        {
            "id": 3,
            "libelle_categorie": "Conte"
        },
        {
            "id": 4,
            "libelle_categorie": "Harlequin"
        },
        {
            "id": 5,
            "libelle_categorie": "Science"
        },
        {
            "id": 6,
            "libelle_categorie": "Mecanique"
        },
        {
            "id": 7,
            "libelle_categorie": "Biologie"
        },
        {
            "id": 8,
            "libelle_categorie": "Manuel"
        },
        {
            "id": 9,
            "libelle_categorie": "Etudes"
        },
        {
            "id": 10,
            "libelle_categorie": "Divertissement"
        }
    ],
    "Nombre de categories": 10,
    "success": true
}
```

#### POST/book/addcategories

##### Add a category

This endpoints returns success value, Number of saved categories.
the URL based on local server :
```bash
http://127.0.0.1:5000/book/addcategories

```
```bash
{
    "Nombre de Categorie": 8,
    "Response": "enregistrement effectué",
    "success": true
}


```

#### GET/book/showallcategories/?id

##### Search category by ID

This endpoints returns success value, a list result from the search by ID of a category.
the URL based on local server :
```bash
 http://127.0.0.1:5000/book/showallcategories/1

```
```bash
{
    "Id recherche": 1,
    "Listecategorie": [
        {
            "id": 1,
            "libelle": "Fiction"
        }
    ],
    "Nombre de categories": 10,
    "success": true
}

```

#### DELETE/book/deletecategorie/?id

##### Delete a category by ID

This endpoints returns success value, Number of saved categories, the deleted category ID
the URL based on local server :
```bash
http://127.0.0.1:5000/book/deletecategorie/10

```
```bash
{
    "Categorie effacée": 10,
    "Nombre de Categories": 7,
    "Response": "Suppression effectuée correctement",
    "success": true
}

```

#### PATCH/book/updatecategory/?id

##### Update a category by ID

This endpoints returns success value, Number of saved categories, the updated category ID
the URL based on local server :
```bash
http://127.0.0.1:5000/book/updatecategory/3

```
```bash
{
    "Nombre de Categories": 8,
    "Response": "Modifie avec succes",
    "id categorie moodifiee": 3,
    "success": true
}

```

#### GET/book/showbooklist

##### Show a list of books

This endpoints returns success value, Number of saved books, the list of saved books
the URL based on local server :
```bash
http://127.0.0.1:5000/book/showbooklist

```
```bash

{
    "Liste de livres": [
        {
            "auteur": "aliexpress",
            "categorie_id": 1,
            "date_publication": "Mon, 25 May 1987 00:00:00 GMT",
            "editeur": "kodjovi",
            "id": 1,
            "isbn": "12345678",
            "titre": "Le vent se leve"
        },
        {
            "auteur": "Lord",
            "categorie_id": 2,
            "date_publication": "Mon, 25 Jul 1977 00:00:00 GMT",
            "editeur": "Yves le curseur",
            "id": 2,
            "isbn": "12345678",
            "titre": "Ali aux pays des merveilles"
        }
    ],
    "Nombre de livres": 2,
    "success": true
}


```


#### GET/book/showbooklist/id?

##### Show a list of books

This endpoints returns success value, Number of saved books, the book searched by ID
the URL based on local server :
```bash
http://127.0.0.1:5000/book/showbooklist/1

```
```bash

{
    "Id recherché": 1,
    "Listecategorie": [
        {
            "auteur": "aliexpress",
            "categorie_id": 1,
            "date_publication": "Mon, 25 May 1987 00:00:00 GMT",
            "editeur": "kodjovi",
            "id": 1,
            "isbn": "12345678",
            "titre": "Le vent se leve"
        }
    ],
    "success": true
}


```


#### POST/book/addbooks

##### Add a book

This endpoints returns success value, Number of saved book
the URL based on local server :
```bash
http://127.0.0.1:5000/book/addbooks

```
```bash
{
    "Nombre de Livres": 4,
    "Response": "enregistrement effectué",
    "success": true
}

```

#### DELETE/book/deletebook/?id

##### Delete a book

This endpoints returns success value, Number of saved books, the deleted book ID
the URL based on local server :
```bash
http://127.0.0.1:5000/book/deletebook/4

```
```bash
{
    "Livre effacé": 4,
    "Nombre de Livres": 3,
    "Response": "Suppression effectuée correctement",
    "success": true
}

```
#### GET/bookbook/showbooklist/?id

##### Delete a book

This endpoints returns success value, Number of saved books, The searched book by category ID
the URL based on local server :
```bash
http://127.0.0.1:5000/book/showbooklist/4

```
```bash
{
    "Id recherché": 3,
    "Liste de Livres": [
        {
            "auteur": "Lord",
            "categorie_id": 3,
            "date_publication": "Mon, 25 Jul 1977 00:00:00 GMT",
            "editeur": "Yves le curseur",
            "id": 3,
            "isbn": "123456787",
            "titre": "la peche du dimanche"
        }
    ],
    "success": true
}
```

#### PATCH/book/updatebook/?id

##### Update a book

This endpoints returns success value, The updated book by ID, number of book
the URL based on local server :
```bash
http://127.0.0.1:5000/book/updatebook/1

```
```bash
{
    "Nombre de Livres": 6,
    "Response": "Modifie avec succes",
    "id categorie moodifiee": 1,
    "success": true
}
```