# CUCLIMBS sign-in system
# author: Harold Ainsworth, CU Climbing Team, spring 2019
# sign_in.py - driver file for sign-in program
import sys
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as char_lcd
import datetime as dt
import psycopg2 as pg
from config import config

def record_attendance(conn, lcd, student_data):
	""" records student practice attendence for the current date """

	cur = conn.cursor()

	#insert student into students table
	insert_student = """ INSERT INTO students(student_id, student_name) VALUES(%s, %s); """
	try:
		print('Adding student to database...', end=' ')
		cur.execute(insert_student, student_data)
		print('Done.')
	except (Exception, pg.IntegrityError) as error:
		# if student already in database, IntegrityError thrown as student_id is PK
		print('Student already exists, skipping.')
	conn.commit()

	# record student attendance in attendance table
	insert_attend = """ INSERT INTO attendance(student_id, practice_date) VALUES(%s, %s); """
	print('Logging attendance to database...', end=' ')
	# check if student has already checked in today
	check_dup = """ SELECT * FROM attendance WHERE student_id = %s AND practice_date = %s """
	cur.execute(check_dup, (student_data[0], 'TODAY'))
	if len(cur.fetchall()) == 0:
		# if entry not yet recorded for today...
		# insert student's attendance for today
		cur.execute(insert_attend, (student_data[0], 'TODAY'))
		print('Done.')
	else:
		print('Attendance already logged, skipping.')

	conn.commit()
	lcd.clear()
	lcd.message = '{}\nThank You!'.format(student_data[1])
	print('Task completed, databases are up-to-date.')
	time.sleep(2)

def name_from_data(card_data):
	""" parses first/lastname and student id from card_data """
	# data stored in following format:
	# %B[CARDNUMBER]=[STUDENTID]=[FIRSTNAME/LASTNAME]=[???]?;[CARDNUMBER]=[???]?
	# where both [???] are some unkown number

	# return None if error reading card or card_data formatted incorrectly
	if card_data[1] != 'B' or card_data.count('=') != 4:
		return None

	# split data into fields delimited by '='
	fields = card_data.split('=')
	# [STUDENTID] is second field
	# [FIRSTNAME/LASTNAME] is third field
	sid = fields[1]
	first_last_name = fields[2]
	# replace '/'with ' 'in first/last name
	first_last_name = first_last_name.replace('/', ' ')
	# convert to tuple and return
	return (sid, first_last_name)

def init_tables(cur):
	""" initializes the tables in the PostgreSQL database """
	commands = (
		"""
		CREATE TABLE IF NOT EXISTS students(
			student_id INTEGER,
			student_name VARCHAR(100),
			PRIMARY KEY (student_id)
		)
		""",
		"""
		CREATE TABLE IF NOT EXISTS attendance(
			id SERIAL,
			student_id INTEGER,
			practice_date DATE,
			PRIMARY KEY (id)
		)
		"""
	)
	print('Initializing tables...', end=' ')
	for command in commands:
		try:
			cur.execute(command)
		except (Exception, pg.DatabaseError) as error:
			print(error)
	print('Done.')

def main():
	# LCD pin config
	lcd_rs = digitalio.DigitalInOut(board.D26)
	lcd_en = digitalio.DigitalInOut(board.D19)
	lcd_d7 = digitalio.DigitalInOut(board.D27)
	lcd_d6 = digitalio.DigitalInOut(board.D22)
	lcd_d5 = digitalio.DigitalInOut(board.D24)
	lcd_d4 = digitalio.DigitalInOut(board.D25)
	lcd_backlight = digitalio.DigitalInOut(board.D13)

	# LCD size
	lcd_columns = 16
	lcd_rows = 2

	# LCD class init
	lcd = char_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5,
		 lcd_d6, lcd_d7, lcd_columns, lcd_rows)

	# connect to the psql database
	try:
		print('Connecting to PostgreSQL database...', end=' ')
		params = config()
		conn = pg.connect(**params)
	except (Exception, pg.OperationalError) as error:
		print(error)
		print('Exiting...')
		sys.exit()
	print('Done.')
	# initialize tables in database if not exist
	init_tables(conn.cursor())

	# main program loop
	while True:
		# get data from card reader
		print('-'*60)
		lcd.clear()
		lcd.message = 'Please swipe\nBuffOne...'
		card_data = input('Please swipe card.\n')
		if card_data == "":
			# for debugging purposes, stop program if enter pressed
			print('Exiting...')
			conn.close()
			lcd.clear()
			sys.exit()
		print('Processing...')
		student_data = name_from_data(card_data)

		# ensure data read from card properly
		if student_data is not None:
			# if success...
			record_attendance(conn, lcd, student_data)
		else:
			# if error
			lcd.clear()
			lcd.message = 'Error, please\ntry again.'
			print('Error, try again.')
			time.sleep(1.5)

	# clean up
	conn.close()

if __name__ == '__main__':
	main()
