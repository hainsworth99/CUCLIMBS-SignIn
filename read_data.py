# CUCLIMBS sign-in system
# author: Harold Ainsworth, CU Climbing Team, spring 2019
# read_data.py - retrieve team attendance data from database
import sys
import psycopg2 as pg
from config import config

def get_students(conn):
	cur = conn.cursor()
	# return list of all students in database in format (student_id, student_name)
	cur.execute('SELECT * FROM students')
	return cur.fetchall()

def get_student_attendance(conn):
	cur = conn.cursor()
	students = get_students(conn)
	attendance = []
	select_count = """ SELECT COUNT(DISTINCT practice_date)
			AS practice_count
			FROM attendance
			WHERE student_id = %s """
	for student in students:
		cur.execute(select_count, (student[0],))
		count = cur.fetchall()[0][0]
		attendance.append((student[0],student[1],count))
	return attendance

def get_practice_count(conn):
	cur = conn.cursor()
	# counting number of distinct dates gives the number of practices held
	cur.execute('SELECT COUNT(DISTINCT practice_date) AS practice_count FROM attendance')
	# get and return query results
	results = cur.fetchall()
	return results[0][0]

def main():
	# connect to psql database
	try:
		print('Connecting to PostgreSQL database...', end=' ')
		params = config()
		conn = pg.connect(**params)
	except (Exception, pg.OperationalError) as error:
		print(error)
		print('Exiting...')
		sys.exit()
	print('Done.')

	# get count of practices held and list of student attendance
	count = get_practice_count(conn)
	student_attendance = get_student_attendance(conn)
	# print table
	print('-'*84)
	print('|{:>10} |{:>45} |{:>12} |{:>8} |'.format('SID:', 'Name:', 'Attendance:', 'Status:'))
	for student in student_attendance:
		status = 'good' if (float(student[2])/count) >= 0.5 else 'bad'
		print('-'*84)
		print('|{:>10} |{:>45} |{:>6}  / {:>2} |{:>8} |'
		.format(student[0], student[1], student[2], count, status))
	print('-'*84)

if __name__ == '__main__':
	main()
