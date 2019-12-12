import cfg
import demjson
import re
import requests
from bs4 import BeautifulSoup

session = requests.Session()
header1 = {
    'Host': 'newjw.lixin.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,zh-CN;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
}
header2 = {
    'Host': 'newjw.lixin.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,zh-CN;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Request': '1',
    'If-None-Match': '1546055702390_386756',
    'Cache-Control': 'max-age=0',
}
header3 = {
    'Host': 'newjw.lixin.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'en-US,zh-CN;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://newjw.lixin.edu.cn/webapp/std/edu/lesson/std-elect-course!defaultPage.action?electionProfile.id=' + str(
        cfg.profileID),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '27',
    'DNT': '1',
    'Connection': 'keep-alive',
}


class Login:
    def __init__(self):
        self.username = cfg.username
        self.password = cfg.password
        self.login = 'http://newjw.lixin.edu.cn/sso/login'

    def login_jw(self):
        login_state = session.post(self.login, data={'username': self.username, 'password': self.password}).status_code
        if login_state == 200:
            return 'LoginSucceed'
        else:
            return 'LoginFailed'


class CourseList:
    def __init__(self):
        self.enterPage = "http://newjw.lixin.edu.cn/webapp/std/edu/lesson/std-elect-course.action"
        self.coursePage = 'http://newjw.lixin.edu.cn/webapp/std/edu/lesson/std-elect-course!defaultPage.action?electionProfile.id='
        self.courseList = 'http://newjw.lixin.edu.cn/webapp/std/edu/lesson/std-elect-course!data.action?profileId='
        self.profileID = str(cfg.profileID)
        self.courseDatabase = []
        self.courseGetModel = None

    def connect_course(self):
        _ = session.get(self.enterPage)
        _ = session.get(self.coursePage + self.profileID)
        header4 = header1.copy()
        login_cookies = session.cookies.get_dict()
        course_cookies = '; '.join([i + '=' + j for i, j in login_cookies.items()])
        header4['Cookie'] = course_cookies
        self.courseGetModel = session.get(self.courseList + self.profileID, headers=header4)
        course_page_status = self.courseGetModel.status_code
        if course_page_status == 200:
            return 'CourseListGetSucceed'
        else:
            return 'CourseListGetFailed'

    def load_course_list(self):
        all_course_database = self.courseGetModel.text
        all_course_database = all_course_database.lstrip('var lessonJSONs = [').rstrip('];')
        all_course_database = re.sub("'", "\"", all_course_database)
        all_course_database = re.sub("},{id", "}#json_split#{id", all_course_database)
        all_course_database = all_course_database.split("#json_split#")
        if len(all_course_database) == 1 and all_course_database[0] == '':
            return {}
        for j in all_course_database:
            self.courseDatabase.append(demjson.decode(j))
        return self.courseDatabase


class Select:
    def __init__(self, course_database, course_now):
        self.courseDatabase = course_database
        self.courseCode = course_now
        self.courseID = 0
        self.selectPage = 'http://newjw.lixin.edu.cn/webapp/std/edu/lesson/std-elect-course!batchOperator.action?profileId='
        self.profileID = str(cfg.profileID)
        self.selectStateContent = None
        self.courseTransmit = None

    def query(self):
        for k in self.courseDatabase:
            if k['code'] == self.courseCode:
                self.courseID = k['id']
                return 'CourseFound', k
        else:
            return 'CourseNotFound', None

    def transmit(self):
        now_cookies = session.cookies.get_dict()
        transmit_cookies = '; '.join([i + '=' + j for i, j in now_cookies.items()])
        header3['Cookie'] = transmit_cookies
        self.courseTransmit = session.post(self.selectPage + self.profileID,
                                           data={'operator0': str(self.courseID) + ':true:0'})
        if self.courseTransmit.status_code == 200:
            select_state_page = BeautifulSoup(self.courseTransmit.text, features='html.parser')
            select_state_content = select_state_page.table.text
            self.selectStateContent = re.sub(r"\s", '', select_state_content)
            return 'CourseSubmitSucceed', self.selectStateContent
        else:
            return 'CourseSubmitFailed', None
