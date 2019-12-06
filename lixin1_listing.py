from lixin1 import *

login = Login()
login_action = login.login_jw()
print(login_action)
if login_action == 'LoginSucceed':
    course_get = CourseList()
    course_get_action = course_get.connect_course()
    print(course_get_action)
    if course_get_action == 'CourseListGetSucceed':
        course_list = course_get.load_course_list()
        with open("lixin1_course.txt", "w", encoding="utf-8") as course_list2:
            for course2 in course_list:
                for course2_attr, course2_val in course2.items():
                    course2_val = str(course2_val) + "\t"
                    course_list2.write(course2_val)
                course_list2.write("\n")
