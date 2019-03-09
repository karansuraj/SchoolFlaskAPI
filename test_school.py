import os
import tempfile
import pytest

from school import *


def init_db():
    """ Init app database, creating new tables."""
    db = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    with app.open_resource('school_db_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@pytest.fixture
def client():
    """ Init school app with temp empty database and create empty tables"""
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    # app.config['DATABASE'] = 'school.db'
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        init_db()
    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    """ Validate that database being used for testing has empty tables """
    students = client.get('/students/all').get_json()
    classes = client.get('/classes/all').get_json()
    assert len(students) == 0 and len(classes) == 0


def test_add_student(client):
    """ Test adding new student, and validate there is only 1 student and that all fields are correct as entered """
    client.post(
        '/students/add_student?lastname=Suraj&firstname=Karan&address=10 Out of Ten&major=Biomedical Engineering')
    students = client.get('/students/all').get_json()
    assert len(students) == 1
    added_student = students[0]
    assert added_student['STUDENT_ID'] == 1
    assert added_student['ADDRESS'] == '10 Out of Ten'
    assert added_student['FIRSTNAME'] == 'Karan'
    assert added_student['LASTNAME'] == 'Suraj'
    assert added_student['MAJOR'] == 'Biomedical Engineering'


def test_add_multiple_students(client):
    """ Test adding new student, and validate there is only 1 student and all fields are correct as posted """
    client.post(
        '/students/add_student?lastname=Suraj&firstname=Karan&address=10 Out of Ten&major=Biomedical Engineering')
    client.post(
        '/students/add_student?lastname=Kipling&firstname=Rudyard&address=2 Lane&major=Literal Engineering')
    students = client.get('/students/all').get_json()
    assert len(students) == 2


def test_add_class(client):
    """ Test adding new class, and validate there is only 1 class and all fields are correct as posted """
    client.post('/classes/add_class?course_name=Underwater Basketweaving')
    classes = client.get('/classes/all').get_json()
    assert len(classes) == 1
    added_class = classes[0]
    assert added_class['CRN'] == 1
    assert added_class['COURSE_NAME'] == 'Underwater Basketweaving'


def test_add_student_to_class(client):
    """ Test adding a student to a class (after adding a student and creating a class) """
    client.post(
        '/students/add_student?lastname=Suraj&firstname=Karan&address=10 Out of Ten&major=Biomedical Engineering')
    client.post('/classes/add_class?course_name=Underwater Basketweaving')
    client.post('/students/add_student_class?student_id=1&class_id=1')
    schedule = client.get('/students/classes?student_id=1').get_json()
    assert 'Karan Suraj' in schedule and schedule['Karan Suraj'][0] == 'Underwater Basketweaving'


def test_delete_student(client):
    """ Test deleting a student (after adding one) """
    client.post(
        '/students/add_student?lastname=Suraj&firstname=Karan&address=10 Out of Ten&major=Biomedical Engineering')
    client.delete('/students/delete_student?id=1')
    students = client.get('/students/all').get_json()
    assert len(students) == 0
