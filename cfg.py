"""
profileID:
    [int] database id of this semester, update every semester required. eg:
    http://newjw.lixin.edu.cn/webapp/std/edu/lesson/std-elect-course!defaultPage.action?electionProfile.id=87
username:
    [str] student ID of course center.
password:
    [str] password of course center.
courseCode:
    [list->str] course codes needs elect.
visitT:
    [int] threads that visit course center.
electT:
    [int] threads that elect EACH course in courseCode list.
"""
profileID = 100
username = ''
password = ''
courseCode = []
visitT = 1
electT = 1
