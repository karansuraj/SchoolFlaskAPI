import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/', methods=['GET'])
def home():
    return '''<h1>School Database</h1>
<p>An API reading data from a school database.</p>'''


@app.route('/classes/all', methods=['GET'])
def api_get_all_classes():
    # REST API call to get a list of all classes in the database

    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_students = cur.execute('SELECT * FROM CLASS;').fetchall()
    return jsonify(all_students)


@app.route('/classes', methods=['GET'])
def api_get_classes_for_student():
    # REST API call to get a list of all classes for a student

    query_parameters = request.args
    student_id = query_parameters.get('student_id')
    last_name = query_parameters.get('lastname')
    first_name = query_parameters.get('firstname')
    address = query_parameters.get('address')
    major = query_parameters.get('major')
    return jsonify(classes_for_student(student_id, last_name, first_name, address, major))


@app.route('/students/all', methods=['GET'])
def api_get_all_students():
    # REST API call to get a list of all students (including courses they're enrolled in)

    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_students = cur.execute('SELECT * FROM STUDENT;').fetchall()
    return jsonify(all_students)


@app.route('/students', methods=['GET'])
def api_get_student():
    # REST API call to get student(s) by filter criteria

    query_parameters = request.args
    student_id = query_parameters.get('id')
    last_name = query_parameters.get('lastname')
    first_name = query_parameters.get('firstname')
    address = query_parameters.get('address')
    major = query_parameters.get('major')
    return jsonify(get_student(student_id, last_name, first_name, address, major))


@app.route('/classes/add_class', methods=['POST'])
def api_insert_class():
    # REST API call to insert a class into the database (does not check if class already exists, unique id provided)

    course_name = request.values.get('course_name')
    try:
        conn = sqlite3.connect('school.db')
        sql = "INSERT INTO CLASS(CRN, COURSE_NAME) " \
              "VALUES((SELECT MAX(CRN) + 1 FROM CLASS), ?)"
        conn.execute(sql, (course_name, ))
        conn.commit()
        return course_name+" added to database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/students/add_student', methods=['POST'])
def api_insert_student():
    # REST API call to insert a student into the database (does not check if student already exists, unique id provided)

    last_name = request.values.get('lastname')
    first_name = request.values.get('firstname')
    address = request.values.get('address')
    major = request.values.get('major')
    try:
        conn = sqlite3.connect('school.db')
        sql = "INSERT INTO STUDENT(student_id, lastname, firstname, address, major) " \
              "VALUES((SELECT MAX(student_id) + 1 FROM STUDENT), ?,?,?,?)"
        conn.execute(sql, (last_name, first_name, address, major))
        conn.commit()
        return first_name+" "+last_name+" added to database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/students/add_student_class', methods=['POST'])
def api_insert_class_for_student():
    # REST API call to enroll a student in a class

    student_id = request.values.get('student_id')
    class_id = request.values.get('class_id')

    # Validate that student_id and class_id exist in schedule, else 404
    student = get_student(student_id, None, None, None, None)
    classes = get_classes(class_id, None)
    if len(student) == 0 or len(classes) == 0:
        return page_not_found(404)

    # Validate that student_id and class_id does NOT exist in schedule, else 404
    schedule = get_schedule(student_id, class_id)
    if len(schedule) != 0:
        return page_not_found(404)

    try:
        conn = sqlite3.connect('school.db')
        sql = "INSERT INTO SCHEDULE_TABLE(student_id, crn) VALUES(?,?)"
        conn.execute(sql, (student_id, class_id))
        conn.commit()
        return "Class ID "+class_id+" for Student ID "+student_id+" added to database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/classes/update_class', methods=['PUT'])
def api_update_class():
    # REST API call to update a class by crn id

    crn = request.values.get('id')
    course_name = request.values.get('course_name')
    class_object = get_classes(crn, None)
    if not course_name:
        course_name = class_object[0]['COURSE_NAME']

    # If ID doesn't exist in db, return 404
    if len(class_object) == 0:
        return page_not_found(404)

    try:
        conn = sqlite3.connect('school.db')
        student_sql = "UPDATE CLASS SET COURSE_NAME = ? WHERE crn = ? ;"
        conn.execute(student_sql, (course_name, crn))
        conn.commit()
        return "CRN/Course ID "+crn+" updated in database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/students/update_student', methods=['PUT'])
def api_update_student():
    # REST API call to update a student by id

    student_id = request.values.get('id')
    last_name = request.values.get('lastname')
    first_name = request.values.get('firstname')
    address = request.values.get('address')
    major = request.values.get('major')
    student_object = get_student(student_id, None, None, None, None)
    if not last_name:
        last_name = student_object[0]['LASTNAME']
    if not first_name:
        first_name = student_object[0]['FIRSTNAME']
    if not address:
        address = student_object[0]['ADDRESS']
    if not major:
        major = student_object[0]['MAJOR']

    # If ID doesn't exist in db, return 404
    if len(student_object) == 0:
        return page_not_found(404)

    try:
        conn = sqlite3.connect('school.db')
        student_sql = "UPDATE STUDENT SET lastname = ?, firstname = ?, address = ?, major = ? WHERE student_id = ? ;"
        conn.execute(student_sql, (last_name, first_name, address, major, student_id))
        conn.commit()
        return "Student ID "+student_id+" updated in database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/classes/delete_class', methods=['DELETE'])
def api_delete_class():
    # REST API call to delete a class from the database (and any classes on the schedule)

    crn = request.values.get('id')

    # Validate that student exists, else 404
    classes = get_classes(crn, None)
    if len(classes) == 0:
        return page_not_found(404)

    try:
        conn = sqlite3.connect('school.db')
        class_sql = "DELETE FROM CLASS WHERE crn = ? ;"
        conn.execute(class_sql, (crn, ))
        # Cascade delete not working, so need to include this
        schedule_table_sql = "DELETE FROM SCHEDULE_TABLE WHERE CRN = ? ;"
        conn.execute(schedule_table_sql, (crn, ))
        conn.commit()
        return "CRN/Course ID " + crn + " removed from database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/students/delete_student', methods=['DELETE'])
def api_delete_student():
    # REST API call to delete a student from the database (and any enrolled classes)

    student_id = request.values.get('id')

    # Validate that student exists, else 404
    student = get_student(student_id, None, None, None, None)
    if len(student) == 0:
        return page_not_found(404)

    try:
        conn = sqlite3.connect('school.db')
        student_sql = "DELETE FROM STUDENT WHERE student_id = ? ;"
        conn.execute(student_sql, student_id)
        # Cascade delete not working, so need to include this
        schedule_table_sql = "DELETE FROM SCHEDULE_TABLE WHERE student_id = ? ;"
        conn.execute(schedule_table_sql, (student_id, ))
        conn.commit()
        return "Student ID "+student_id+" removed from database."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


@app.route('/students/delete_student_class', methods=['DELETE'])
def api_delete_class_for_student():
    # REST API call to delete a student from a class

    student_id = request.values.get('student_id')
    class_id = request.values.get('class_id')

    # Validate that student_id and class_id exist in schedule, else 404
    schedule = get_schedule(student_id, class_id)
    if len(schedule) == 0:
        return page_not_found(404)

    try:
        conn = sqlite3.connect('school.db')
        sql = "DELETE FROM SCHEDULE_TABLE WHERE STUDENT_ID = ? AND CRN = ? ;"
        conn.execute(sql, (student_id, class_id))
        conn.commit()
        return "Student ID "+student_id+" deleted from Class ID "+class_id+"."

    except sqlite3.Error as e:
        print(e)
        return "Unable to write to database!"


# Helper Functions
def get_student(student_id, last_name, first_name, address, major):
    # Get student(s) filtered by id, last name, first name, address, and/or major

    query = "SELECT * FROM STUDENT WHERE"
    to_filter = []

    if student_id:
        query += ' student_id=? AND'
        to_filter.append(student_id)
    if last_name:
        query += ' lastname=? AND'
        to_filter.append(last_name)
    if first_name:
        query += ' firstname=? AND'
        to_filter.append(first_name)
    if address:
        query += ' address=? AND'
        to_filter.append(address)
    if major:
        query += ' major=? AND'
        to_filter.append(major)
    if not (student_id or last_name or first_name or address or major):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()
    # Add list of classes for each student in query output
    for res in results:
        res['CLASSES'] = classes_for_student(res['STUDENT_ID'], None, None, None, None)
    return results


def get_classes(crn, course_name):
    # Get class(es) filtered by crn course number and/or course name

    query = "SELECT * FROM CLASS WHERE"
    to_filter = []

    if crn:
        query += ' crn=? AND'
        to_filter.append(crn)
    if course_name:
        query += ' course_name=? AND'
        to_filter.append(course_name)

    query = query[:-4] + ';'
    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    return results


def get_schedule(student_id, crn):
    # Get the class enrollments students filtered by student_id and/or crn course number

    query = "SELECT * FROM SCHEDULE_TABLE WHERE"
    to_filter = []

    if crn:
        query += ' crn=? AND'
        to_filter.append(crn)
    if student_id:
        query += ' student_id=? AND'
        to_filter.append(student_id)

    query = query[:-4] + ';'
    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    return results


def classes_for_student(student_id, lastname, firstname, address, major):
    # Get a list of all classes a student is enrolled in

    query = "SELECT CLS.course_name Classes FROM STUDENT STD" \
            " INNER JOIN SCHEDULE_TABLE SCD" \
            "   ON STD.student_id = SCD.student_id" \
            " INNER JOIN CLASS CLS" \
            "   ON CLS.crn = SCD.crn" \
            "  WHERE"
    to_filter = []

    if student_id:
        query += ' STD.student_id=? AND'
        to_filter.append(student_id)
    if lastname:
        query += ' STD.lastname=? AND'
        to_filter.append(lastname)
    if firstname:
        query += ' STD.firstname=? AND'
        to_filter.append(firstname)
    if address:
        query += ' STD.address=? AND'
        to_filter.append(address)
    if major:
        query += ' STD.major=? AND'
        to_filter.append(major)

    query = query[:-4] + ';'

    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return convert_to_list(results, 'Classes')


def convert_to_list(dictionary, field):
    # Convert query output with a single column to a list
    out_dict = dict()
    out_dict[field] = []
    for d in dictionary:
        out_dict[field].append(d[field])
    return out_dict


app.run()
