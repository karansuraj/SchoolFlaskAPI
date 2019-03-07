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


@app.route('/', methods=['GET'])
def home():
    return '''<h1>School Database</h1>
<p>An API reading data from a school database.</p>'''


@app.route('/students/all', methods=['GET'])
def api_all_students():
    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_students = cur.execute('SELECT * FROM STUDENT;').fetchall()
    return jsonify(all_students)


@app.route('/classes/all', methods=['GET'])
def api_all_classes():
    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_students = cur.execute('SELECT * FROM CLASS;').fetchall()
    return jsonify(all_students)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/students', methods=['GET'])
def api_filter_students():
    query_parameters = request.args

    id = query_parameters.get('id')
    lastName = query_parameters.get('lastname')
    firstName = query_parameters.get('firstname')
    address = query_parameters.get('address')
    major = query_parameters.get('major')

    query = "SELECT * FROM STUDENT WHERE"
    to_filter = []

    if id:
        query += ' student_id=? AND'
        to_filter.append(id)
    if lastName:
        query += ' lastname=? AND'
        to_filter.append(lastName)
    if firstName:
        query += ' firstname=? AND'
        to_filter.append(firstName)
    if address:
        query += ' address=? AND'
        to_filter.append(address)
    if major:
        query += ' major=? AND'
        to_filter.append(major)
    if not (id or lastName or firstName or address or major):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@app.route('/classes', methods=['GET'])
def api_classes():
    query_parameters = request.args

    id = query_parameters.get('id')
    lastname = query_parameters.get('lastname')
    firstname = query_parameters.get('firstname')
    address = query_parameters.get('address')
    major = query_parameters.get('major')

    query = "SELECT CLS.course_name Classes FROM STUDENT STD" \
            " INNER JOIN SCHEDULE_TABLE SCD" \
            "   ON STD.student_id = SCD.student_id" \
            " INNER JOIN CLASS CLS" \
            "   ON CLS.crn = SCD.crn" \
            "  WHERE"
    to_filter = []

    if id:
        query += ' STD.student_id=? AND'
        to_filter.append(id)
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
    if not (id or lastname or firstname or address or major):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('school.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(convert_to_list(results, 'Classes'))


@app.route('/students/add_student', methods=['POST'])
def insert_student():
    test = request.values
    lastname = request.values.get('lastname')
    firstname = request.values.get('firstname')
    address = request.values.get('address')
    major = request.values.get('major')
    try:
        conn = sqlite3.connect('school.db')
        sql = "INSERT INTO STUDENT(student_id, lastname, firstname, address, major) VALUES((SELECT MAX(student_id) + 1 FROM STUDENT), ?,?,?,?)"
        conn.execute(sql, (lastname, firstname, address, major))
        conn.commit()
        return firstname+" "+lastname+" added to database."

    except:
        return "Unable to write to database! Please check that db is not locked and try again later."


def convert_to_list(dict,field):
    # Convert single column to a list
    out_dict = {}
    out_dict[field] = []
    for d in dict:
        out_dict[field].append(d[field])
    return out_dict

app.run()