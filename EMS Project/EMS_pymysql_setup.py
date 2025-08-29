import pymysql

conn = pymysql.connect(host="localhost", user="root",
                       password="root@7900", database="employee_db")
qur1 = ("CREATE TABLE emp_db (emp_id VARCHAR(40) PRIMARY KEY,emp_name VARCHAR(50),mob_no VARCHAR(40),emp_salary VARCHAR(40));")
mycur = conn.cursor()
mycur.execute(qur1)
mycur.close()
conn.close()
