# SE306Project
SE306Project - Intelligent E-Commerce Management System
Set Up and Run guide
made by DNDTech -- Wim Reuvekamp, Wyatt Redshaw, Nathan Tran
last modified 04/26/2023

--- intended for Windows 10

1. download or clone git repository to your machine
 - https://github.com/WimReuvekampSDSU/SE306Project.git

2. open a virtual environment (such as VS Code)
 - this can also be used to clone git repository using the link

3. in a terminal, enter 'pip --version' (versions used in development: 23.1, 23.1.2)
 - most virtual environments for python already have this installed
 - if your version is dated, it might not be compatible. Upgrade it with: 
	'pip install --upgrade pip'
	and following the steps from there.
 - if not installed, see the installation guide here: 
	https://pip.pypa.io/en/stable/installation/

4. Enter the following commands to install required libraries
	'python -m pip install Django' 			Django version: 4.2

5. 'pip install psycopg2-binary'				psycopg2-binary version: 2.9.6

6. if not already done, install PostgreSQL or similar. 
	A command line for SQL is necessary for the database.
 - https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
 - an admin app like pgAdmin can be helpful if there are database issues
 - it should be added to the system's PATH environment

7. in the sql shell (psql for postgresql), enter:
	'CREATE DATABASE dndtech;'	where 'dndtech' is the name of the database.
 - if having trouble creating a database, 
	it may be preferable to use pgAdmin and create a database within the app.

8. in SE306Project/bbay/settings.py (open in text editor or environment),
 - find 'DATABASES = { ...'
 - change "name" to 'dndtech' (or whatever you previously named the database'
 - change user and password, if needed or as appropriate to correspond with your environment
 - 'localhost' and '5432' should remain unchanged

9. 'python manage.py makemigrations'

10. 'python manage.py migrate'

11. 'python manage.py runserver'


How to run the server once libraries and database are installed

1. Run Steps 9-11 in the previous section
 - if there are issues migrating, delete any 'migrations' folders and restart at step 9

2. to view the website, go to the link given in the command prompt
 - should be something like 'http://127.0.0.1:8000/' or very similar
	Open in a browser (Chrome, Edge, Opera, etc)

3. To make a superuser:
 'python manage.py createsuperuser'
 - fill in the credentials as needed
 - runserver again, log in with the credentials as before
 - after log in, in the top right banner click on 'admin'
	Alternatively, go to http://<port>/admin/

If you need to delete or reset the database, make sure to delete the 'media' folder as well
