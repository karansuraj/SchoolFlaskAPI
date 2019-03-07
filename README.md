# SchoolFlaskAPI

Simple Python flask implementation to query a database of students and classes and add/delete students and classes for students. The local server can be run by running the api_school.py python script.

## GET API Calls

| URL                                                               | Function                                                |
|-------------------------------------------------------------------|---------------------------------------------------------|
| /students/all                                                     | Returns JSON list of all students.                              |
| /classes/all                                                      | JSON list of all classes                                |
| /students?id=&lastname=&firstname=&address=&major=                | JSON list of filter criteria on students                |
| /classes?id=&amp;lastname=&amp;firstname=&amp;address=&amp;major= | JSON list of all classes by filter criteria on students |


## POST API Calls

| URL                                                        | Function                                                         |
|------------------------------------------------------------|------------------------------------------------------------------|
| /students/add_student?lastname=&firstname=&address=&major= | Inserts new student with criteria into student table in database |
