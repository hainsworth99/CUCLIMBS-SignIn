# CU Climbing Team Sign In System
A project to track practice attendance for the University of Colorado, Boulder, Climbing Team. Team members "sign in" by swiping their BuffOne cards in a card reader and their attendance is logged in a simple postgresql database. This project was designed to be run on a [Raspberry Pi](https://www.raspberrypi.org/products/), using a [USB card reader](https://www.amazon.com/gp/product/B00E85TH9I/ref=ox_sc_act_title_1?smid=A6DGR5H6GM540&psc=1) to process input, and a simple [16x2 LCD screen](https://www.adafruit.com/product/181) to display output. 

# Dependencies
* [PostgreSQL](https://www.postgresql.org/) - An open source object-relational database system. 
* [pyscopg2](http://initd.org/psycopg/) - A PostgreSQL adapter for python
```bash
sudo apt install postgresql libpq-dev postgresql-client postgresql-client-common -y
```
```bash
pip3 install psycopg2
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
As the program runs, card swipes through the USB card reader will be automatically processed and team member will be added to the database as needed. 
# Authors
* **Harold Ainsworth** - *Initial Work*
