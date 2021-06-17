from app import mysql


class Database(object):

    def __init__(self, user_id=None, f_name=None, course_code=None, old_course_code=None, course_name=None, l_name=None, password=None, email=None, username=None, type_id=None, yr_lv=None, idnum=None, department=None, dept_code=None, dept_name=None, old_department_code=None):
        self.user_id = user_id
        self.f_name = f_name
        self.l_name = l_name
        self.password = password
        self.email = email
        self.username = username
        self.type_id = type_id
        self.yr_lv = yr_lv
        self.idnum = idnum
        self.department = department
        self.dept_code = dept_code
        self.dept_name = dept_name
        self.course_code = course_code
        self.course_name = course_name
        self.old_course_code = old_course_code
        self.old_department_code = old_department_code

    def login(self):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM crude_studentdb.user WHERE username = '{}' and password = '{}'".format(self.username, self.password)

        cursor.execute(sql)
        display = cursor.fetchall()
        return display

    def validateLogin(self):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM crude_studentdb.user WHERE username = '{}'".format(self.username)

        cursor.execute(sql)
        display = cursor.fetchall()
        if display:
            for item in display:
                if item[2] != self.password:
                    return 2
                else:
                    return 0
        elif not display:
            return 1
        else:
            return 0

    @classmethod
    def user_type(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT type_id FROM crude_studentdb.user WHERE user_id = '%s'", [self])
        typeDetails = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()
        return typeDetails

    @classmethod
    def admin_course_list(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.course")
        courseDetails = cursor.fetchall()
        return courseDetails

    @classmethod
    def admin_prof_list(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT p.user_id, p.fname, p.lname, p.course_code, c.dept_code
                        FROM crude_studentdb.prof_profile p
                        LEFT JOIN crude_studentdb.course c on p.course_code=c.course_code""")
        profDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return profDetails

    @classmethod
    def admin_dept_list(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.department")
        deptDetails = cursor.fetchall()
        return deptDetails

    @classmethod
    def admin_student_list(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT s.user_id, s.fname, s.lname, s.id_number, s.year_level, s.course_code, c.course_name, c.dept_code
                FROM crude_studentdb.student_profile s
                LEFT JOIN crude_studentdb.course c on s.course_code=c.course_code""")
        studentDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return studentDetails

    @classmethod
    def prof_student_list(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT s.id_number, s.fname, s.lname, s.year_level, s.course_code FROM crude_studentdb.student_profile s 
                    LEFT JOIN crude_studentdb.prof_profile p on s.course_code=p.course_code
                     WHERE p.user_id=%s""",[self])
        studentDetails = cursor.fetchall()
        return studentDetails


    def viewUser(self):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM crude_studentdb.student_profile WHERE user_id = {}".format(self.user_id)

        cursor.execute(sql)
        display = cursor.fetchall()

        return display

    def add(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO crude_studentdb.user (user_id, password, email, username, type_id) VALUES (%s, %s, %s, %s, %s)",
            (self.user_id, self.password, self.email, self.username, self.type_id))
        mysql.connection.commit()

    def add_student(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO crude_studentdb.student_profile (fname, lname, user_id, id_number, year_level) VALUES (%s, %s, %s, %s, %s)",
            (self.f_name, self.l_name, self.user_id, self.idnum, self.yr_lv))
        mysql.connection.commit()

    def add_st_course(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE crude_studentdb.student_profile SET course_code = %s WHERE user_id = %s",
                       (self.course_code, self.user_id))
        mysql.connection.commit()

    def add_prof_course(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE crude_studentdb.prof_profile SET course_code = %s WHERE user_id = %s",
                       (self.course_code, self.user_id))
        mysql.connection.commit()

    def add_course(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO crude_studentdb.course (course_code, course_name, dept_code) VALUES (%s, %s, %s)",
            (self.course_code, self.course_name, self.dept_code))
        mysql.connection.commit()

    @classmethod
    def select_course(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.course WHERE course_code=%s", [self])
        courseDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return courseDetails

    @classmethod
    def select_student(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.student_profile WHERE user_id=%s", [self])
        studentDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return studentDetails

    @classmethod
    def select_prof(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.prof_profile WHERE user_id=%s", [self])
        profDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return profDetails

    @classmethod
    def select_department(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.department WHERE dept_code=%s", [self])
        courseDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return courseDetails

    def edit_course(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE crude_studentdb.course SET course_code=%s, course_name=%s, dept_code=%s WHERE course_code=%s",
                       (self.course_code, self.course_name, self.dept_code,self.old_course_code))
        mysql.connection.commit()

    def add_department(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO crude_studentdb.department (dept_code, dept_name) VALUES (%s, %s)",
            (self.dept_code, self.dept_name))
        mysql.connection.commit()

    def edit_departmert(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE crude_studentdb.department SET dept_code=%s, dept_name=%s WHERE dept_code=%s",
                       (self.dept_code, self.dept_name, self.old_department_code))
        mysql.connection.commit()

    def edit_student(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE crude_studentdb.student_profile SET id_number=%s, fname=%s, lname=%s, year_level=%s WHERE user_id=%s",
                       (self.idnum, self.f_name, self.l_name, self.yr_lv, self.user_id))
        mysql.connection.commit()

    def edit_prof(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE crude_studentdb.prof_profile SET fname=%s, lname=%s WHERE user_id=%s",
                       (self.f_name, self.l_name, self.user_id))
        mysql.connection.commit()

    @classmethod
    def course_list(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.course")
        courseDetails = cursor.fetchall()
        mysql.connection.commit()
        return courseDetails

    @classmethod
    def student_list(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.student_profile WHERE user_id=%s", [self])
        studentDetails = cursor.fetchall()
        mysql.connection.commit()
        return studentDetails

    @classmethod
    def prof_list(cls, self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.prof_profile WHERE user_id=%s", [self])
        profDetails = cursor.fetchall()
        mysql.connection.commit()
        return profDetails

    def add_prof(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO crude_studentdb.prof_profile (fname, lname, user_id, course_code) VALUES (%s, %s, %s, %s)",
            (self.f_name, self.l_name, self.user_id, self.course_code))
        mysql.connection.commit()

    @classmethod
    def dept_list(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM crude_studentdb.department")
        deptDetails = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return deptDetails


    def delete(self, user_id = None):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM crude_studentdb.user WHERE user_id =%s ",[self.user_id])
        mysql.connection.commit()

    def delete_department(self):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM crude_studentdb.department WHERE dept_code=%s",[self.dept_code])
        mysql.connection.commit()

    def delete_course(self):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM crude_studentdb.course WHERE course_code=%s",[self.course_code])
        mysql.connection.commit()