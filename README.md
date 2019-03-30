# CU Climbing Team Sign In System
A project to track practice attendance for the University of Colorado, Boulder, Climbing Team. Team members "sign in" by swiping their BuffOne cards in a card reader and their attendance is logged in a simple postgresql database. This project was designed to be run on a Raspberry Pi, using a USB card reader to process input, and a simple 16x2 LCD screen to display output. 

# Dependencies
* PostgreSQL - An open source object-relational database system. 
* pyscopg2 - A PostgreSQL adapter for python
```bash
sudo apt install postgresql libpq-dev postgresql-client postgresql-client-common -y
```
```bash
pip install psycopg2
```
# Database Setup
Login to postgres and create database.
```bash
psql -U myusername -h localhost
```
```sql
CREATE DATABASE mydatabase;
```
Create database.ini file to store database connection information:
```ini
[postgresql]
host=localhost
database=mydatabase
user=myusername
password=mypassword
```
# Usage 
Run the program from sign_in.py using python3. Tables will be created automatically if not already created. 
```bash
python3 sign_in.py
```


# Authors
* **Harold Ainsworth** - *Initial Work*
