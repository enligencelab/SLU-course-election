from threading import Thread
from lixin1 import *


class CourseElect(Thread):
    def __init__(self, select):
        Thread.__init__(self)
        self.select = select

    def run(self):
        while 1:
            course_submit_state, course_submit_content = self.select.transmit()
            print(course_submit_state, course_submit_content)


class CourseVisit(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        login = Login()
        login_action = login.login_jw()
        print(login_action)
        if login_action == 'LoginSucceed':
            course_get = CourseList()
            course_get_action = course_get.connect_course()
            print(course_get_action)
            if course_get_action == 'CourseListGetSucceed':
                course_list = course_get.load_course_list()
                for courseNow in cfg.courseCode:
                    print('CourseRequired:', courseNow)
                    select = Select(course_list, courseNow)
                    course_found_result, course_info = select.query()
                    print(course_found_result, course_info)
                    if course_found_result == 'CourseFound':
                        for n in range(cfg.electT):
                            print('ElectThread:', n)
                            t_elect = CourseElect(select)
                            t_elect.start()


if __name__ == "__main__":
    for m in range(cfg.visitT):
        print('VisitThread:', m)
        tVisit = CourseVisit()
        tVisit.start()
