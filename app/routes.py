from flask import render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap
from app import app, mysql
from app.forms import LoginForm
import app.controller as models
import random

Bootstrap(app)


def idgen():
    newId = random.randint(100000, 999999)
    return newId


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        userDetails = request.form
        user_id = idgen()
        password = userDetails['passw']
        email = userDetails['mail']
        username = userDetails['uname']
        type_id = 2
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM crude_studentdb.user WHERE username = %s OR email = %s", (username, email))
        account = cur.fetchone()
        if account:
            flash('Username or Email already taken! Please use a different one.')
        else:
            data = models.Database(user_id=user_id, password=password, email=email, username=username,
                                   type_id=type_id)
            data.add()
            return redirect(url_for('register_student2', user_id=user_id))
    return render_template('register_student.html', title='register student')


@app.route('/register_student2/<int:user_id>', methods=['GET', 'POST'])
def register_student2(user_id):
    if request.method == 'POST':
        userDetails = request.form
        f_name = userDetails['fname']
        l_name = userDetails['lname']
        yr_lv = userDetails['yr_lv']
        idnum = userDetails['idno']
        user_id = user_id
        data = models.Database(f_name=f_name, l_name=l_name, user_id=user_id, idnum=idnum, yr_lv=yr_lv)
        data.add_student()
        return redirect(url_for('login'))
    return render_template('register_student2.html', title='register student')


@app.route('/register_professor', methods=['GET', 'POST'])
def register_professor():
    if request.method == 'POST':
        userDetails = request.form
        user_id = idgen()
        password = userDetails['passw']
        email = userDetails['mail']
        username = userDetails['uname']
        type_id = 3
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM crude_studentdb.user WHERE username = %s OR email = %s", (username, email))
        account = cur.fetchone()
        if account:
            flash('Username or Email already taken! Please use a different one')
        else:
            data = models.Database(user_id=user_id, password=password, email=email, username=username,
                                   type_id=type_id)
            data.add()
            return redirect(url_for('register_professor2', user_id=user_id))
    return render_template('register_professor.html', title='register professor')


@app.route('/register_professor2/<int:user_id>', methods=['GET', 'POST'])
def register_professor2(user_id):
    courseDetails = models.Database.course_list()
    if request.method == 'POST':
        userDetails = request.form
        f_name = userDetails['fname']
        l_name = userDetails['lname']
        user_id = user_id
        course_code = userDetails['course']
        data = models.Database(f_name=f_name, l_name=l_name, user_id=user_id, course_code=course_code)
        data.add_prof()
        return redirect(url_for('login'))
    return render_template('register_professor2.html', courseDetails=courseDetails, title='register professor')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db = models.Database()
    if form.validate_on_submit():
        db = models.Database(username=form.username.data,
                             password=form.password.data)

        if db.validateLogin() == 1:
            flash('Invalid Login. User does not exist', 'danger')
        elif db.validateLogin() == 2:
            flash('Invalid Login. Wrong Password', 'danger')
        else:
            user = db.login()
            session['user'] = user
            return redirect(url_for('home', user_id=user[0][0]))

    if 'user' in session:
        user = session['user']
        return redirect(url_for('home', user_id=user[0][0]))

    return render_template('login.html', form=form)


@app.route('/home/<int:user_id>')
def home(user_id):
    if 'user' in session:
        typeDetails = models.Database.user_type(user_id)
        return render_template('mock_homepage.html', user_id=user_id, typeDetails=typeDetails)
    else:
        return redirect(url_for('login'))


@app.route('/admin_course_list', methods=['GET', 'POST'])
def admin_course_list():
    if 'user' in session:
        courseDetails = models.Database.admin_course_list()
        return render_template("course_list.html", courseDetails=courseDetails)


@app.route('/admin_prof_list', methods=['GET', 'POST'])
def admin_prof_list():
    if 'user' in session:
        profDetails = models.Database.admin_prof_list()
        return render_template("prof_list.html", profDetails=profDetails)


@app.route('/admin_dept_list', methods=['GET', 'POST'])
def admin_dept_list():
    if 'user' in session:
        deptDetails = models.Database.admin_dept_list()
        return render_template("dept_list.html", deptDetails=deptDetails)


@app.route('/admin_student_list', methods=['GET', 'POST'])
def admin_student_list():
    if 'user' in session:
        studentDetails = models.Database.admin_student_list()
        return render_template("student_list.html", studentDetails=studentDetails)

@app.route('/prof_student_list/<int:user_id>', methods=['GET', 'POST'])
def prof_student_list(user_id):
    if 'user' in session:
        studentDetails = models.Database.prof_student_list(user_id)
        return render_template("prof_student_list.html", studentDetails=studentDetails)


@app.route('/student_course_sel/<int:user_id>', methods=['GET', 'POST'])
def student_course(user_id):
    if 'user' in session:
        courseDetails = models.Database.course_list()
        typeDetails = models.Database.user_type(user_id)
        if request.method == 'POST':
            userDetails = request.form
            course_code = userDetails['course']
            data = models.Database(course_code=course_code, user_id=user_id)
            data.add_st_course()
            flash('Course Successfully updated')
            return redirect(url_for('home', user_id=user_id))
        return render_template('student_course.html', title='Course Selection', courseDetails=courseDetails,
                               typeDetails=typeDetails, user_id=user_id)
    else:
        return redirect(url_for('login'))


@app.route('/prof_course_sel/<int:user_id>', methods=['GET', 'POST'])
def prof_course(user_id):
    if 'user' in session:
        courseDetails = models.Database.course_list()
        typeDetails = models.Database.user_type(user_id)
        if request.method == 'POST':
            userDetails = request.form
            course_code = userDetails['course']
            data = models.Database(course_code=course_code, user_id=user_id)
            data.add_prof_course()
            flash('Course Successfully updated')
            return redirect(url_for('home', user_id=user_id))
        return render_template('student_course.html', title='Course Selection', courseDetails=courseDetails,
                               typeDetails=typeDetails, user_id=user_id)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/delete/<int:user_id>')
def delete(user_id):
    if 'user' in session:
        flash("Account Has been deleted")
        data = models.Database(user_id=user_id)
        data.delete(user_id)
        return redirect(url_for('login'))

@app.route('/delete_department/<string:dept_code>')
def delete_department(dept_code):
    if 'user' in session:
        flash("College Has been deleted")
        data = models.Database(dept_code=dept_code)
        data.delete_department()
        return redirect(url_for('admin_dept_list'))

@app.route('/delete_course/<string:course_code>')
def delete_course(course_code):
    if 'user' in session:
        flash("Course Has been deleted")
        data = models.Database(course_code=course_code)
        data.delete_course()
        return redirect(url_for('admin_course_list'))


@app.route('/add_course/', methods=['GET', 'POST'])
def add_course():
    if 'user' in session:
        deptDetails = models.Database.dept_list()
        if request.method == "POST":
            userDetails = request.form
            course_code = userDetails['course_code']
            course_name = userDetails['course_name']
            dept_code = userDetails['dept']
            data = models.Database(course_code=course_code, course_name=course_name, dept_code=dept_code)
            data.add_course()
            return redirect(url_for('admin_course_list'))

        return render_template('add_course.html', deptDetails=deptDetails)

@app.route('/edit_course/<string:course_code>', methods=['GET','POST'])
def edit_course(course_code):
    if 'user' in session:
        deptDetails = models.Database.dept_list()
        courseDetails = models.Database.select_course(course_code)
        if request.method == "POST":
            userDetails = request.form
            new_course_code = userDetails['course_code']
            course_name = userDetails['course_name']
            dept_code = userDetails['dept']
            data = models.Database(course_code=new_course_code, course_name=course_name, dept_code=dept_code, old_course_code=course_code)
            data.edit_course()
            return redirect(url_for('admin_course_list'))
        return render_template('edit_course.html', deptDetails=deptDetails, courseDetails=courseDetails)

@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if 'user' in session:
        if request.method == "POST":
            userDetails = request.form
            dept_code = userDetails['dept_code']
            dept_name = userDetails['dept_name']
            data = models.Database(dept_code=dept_code, dept_name=dept_name)
            data.add_department()
            return redirect(url_for('admin_dept_list'))

        return render_template('add_department.html')


@app.route('/edit_department/<string:dept_code>', methods=['GET','POST'])
def edit_department(dept_code):
    if 'user' in session:
        deptDetails = models.Database.select_department(dept_code)
        if request.method == "POST":
            userDetails = request.form
            new_dept_code = userDetails['dept_code']
            dept_name = userDetails['dept_name']
            data = models.Database(dept_code=new_dept_code, dept_name=dept_name, old_department_code=dept_code)
            data.edit_departmert()
            return redirect(url_for('admin_dept_list'))

        return render_template('edit_department.html',deptDetails=deptDetails)


@app.route('/student_profile/<int:user_id>', methods=['GET', 'POST'])
def student_profile(user_id):
    if 'user' in session:
        studentDetails = models.Database.student_list(user_id)
        return render_template('student_profile.html', studentDetails=studentDetails, user_id=user_id)


@app.route('/edit_student/<int:user_id>', methods=['GET', 'POST'])
def edit_student(user_id):
    if 'user' in session:
        studentDetails = models.Database.student_list(user_id)
        if request.method == "POST":
            userDetails = request.form
            first_name = userDetails['fname']
            last_name = userDetails['lname']
            year_lvl = userDetails['yr_lv']
            student_id = userDetails['idno']
            data = models.Database(f_name=first_name, l_name=last_name, yr_lv=year_lvl, idnum=student_id, user_id=user_id)
            data.edit_student()
            return redirect(url_for('student_profile', user_id=user_id))
        return render_template('edit_student.html', studentDetails=studentDetails, user_id=user_id)


@app.route('/prof_profile/<int:user_id>', methods=['GET', 'POST'])
def prof_profile(user_id):
    if 'user' in session:
        profDetails = models.Database.prof_list(user_id)
        return render_template('prof_profile.html', profDetails=profDetails, user_id=user_id)

@app.route('/edit_prof/<int:user_id>', methods=['GET', 'POST'])
def edit_prof(user_id):
    if 'user' in session:
        profDetails = models.Database.prof_list(user_id)
        if request.method == "POST":
            userDetails = request.form
            first_name = userDetails['fname']
            last_name = userDetails['lname']
            data = models.Database(f_name=first_name, l_name=last_name, user_id=user_id)
            data.edit_prof()
            return redirect(url_for('prof_profile', user_id=user_id))
        return render_template('edit_prof.html', profDetails=profDetails, user_id=user_id)

@app.route('/nav1')
def nav1():
    return render_template('nav1.html')

@app.route('/teachermenu')
def teachermenu():
    return render_template('teachermenu.html')


@app.route('/scratch')
def scratch():
    return render_template('scratch.html')