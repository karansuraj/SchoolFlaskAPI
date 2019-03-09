# SchoolFlaskAPI

Simple Python flask implementation to query a database of students and classes and add/delete students and classes for students. The local server can be run by running the api_school.py python script.

## GET API Calls

| URL                                                               | Function                                                        |
|-------------------------------------------------------------------|-----------------------------------------------------------------|
| /students/all                                                     | Returns JSON list of all students.                              |
| /classes/all                                                      | Returns JSON list of all classes                                |
| /students?id=&lastname=&firstname=&address=&major=                | Returns JSON list of filter criteria on students                |
| /classes?id=&amp;lastname=&amp;firstname=&amp;address=&amp;major= | Returns JSON list of all classes by filter criteria on students |


## POST API Calls

| URL                                                        | Function                                                         |
|------------------------------------------------------------|------------------------------------------------------------------|
| /students/add_student?lastname=&firstname=&address=&major= | Inserts new student with criteria into student table in database |


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
