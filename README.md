# SchoolFlaskAPI

Simple Python 3 flask implementation to query a database of students and classes and add/delete students and classes for students. The local server can be run by running the **school.py** python script. Test cases written with **pytest** for a few API calls are provided in **test_school.py**. A persisted populated sqlite database, used by the app, and its corresponding SQL are provided in **school.db** and school_db_sample.sql. The base schema for the sqlite database used in the app is provided in school_db_schema.sql

## API Calls/Endpoints
Below is a table of all possible insert/create (POST), update (PUT), delete (DELETE), and view (GET) requests that can be made for this API. A JSON export of sample Postman requests is also provided (school.postman_collection.json).

| Function                                     | Request Type | Params                                                                      | Sample Request URL Format                                          |
|----------------------------------------------|--------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------|
| Inserts new student                          | POST         | lastname, firstname, address, major                                         | /students/add_student?lastname=&firstname=&address=&major=         |
| Updates a student by id                      | PUT          | id (mandatory), lastname, firstname, address, major                         | /students/update_student?id=&lastname=&firstname=&address=&major=  |
| Deletes a student by id                      | DELETE       | id (mandatory)                                                              | /students/delete_student?id=                                       |
| Inserts new class                            | POST         | course_name                                                                 | /classes/add_class?course_name=                                    |
| Updates a class by id/crn                    | PUT          | id (mandatory), course_name                                                 | /classes/update_class?id=&course_name=                             |
| Deletes a class by id/crn                    | DELETE       | id (mandatory)                                                              | /classes/delete_class?id=                                          |
| Enrolls student in class                     | POST         | student_id (mandatory), class_id (mandatory)                                | /students/add_student_class?student_id=&class_id=                  |
| Deletes student from class                   | DELETE       | student_id (mandatory), class_id (mandatory)                                | /students/delete_student_class?student_id=&class_id=               |
| Get all students                             | GET          |                                                                             | /students/all                                                      |
| Get all classes                              | GET          |                                                                             | /classes/all                                                       |
| Get all classes student(s) enrolled in       | GET          | student_id (use alone for one student), lastname, firstname, address, major | /students/classes?student_id=&lastname=&firstname=&address=&major= |
| Get all classes all students are enrolled in | GET          |                                                                             | /students/classes/all                                              |
| Get student(s)                               | GET          | id (use alone for one student), lastname, firstname, address, major         | /students?id=&lastname=&firstname=&address=&major=                 |
| Get class(es)                                | GET          | id (use alone for one class), course_name                                   | /classes?id=&course_name=                                          |

## Required Python Dependencies
* flask
* pytest
* pytest-mock
* sqlite3
* tempfile
