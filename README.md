
# DoIt
DoIt app is an application that allows user to manage their time better by creating, updating and checking out tasks of their lists. 



## Setup


To install requirements of the project execute the following command:

    $ pip install -r requirements.txt

Establish connection to a database of your choice. I used PostgreSQL for this project. Create migrations and migrate:

    $ python manage.py makemigrations then $ python manage.py migrate

To start the app:

    $ python manage.py runserver
## License

[MIT](https://choosealicense.com/licenses/mit/)

