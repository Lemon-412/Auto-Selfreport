from requests import session
from time import sleep
from random import randint


class Client:
    def __init__(self, username, password, date):
        self.session = session()
        self.username = username
        self.password = password
        self.data = {}
        self.report_data = {
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': 'U71WZqTsjKUyIBegOZ1fx7f8DgD6xO0ECrpstz2hET5Hs0SvhH26ISt2abya31jOzUtFtM5vREvQlMAVIf9a7DovdPgvF7bOreWgYw3vVyRBkX8zdDJPewgFy6aAcjIjIyDXWHFBI3nFdycyB76fMAo38MS6M1qnu3SaI8qg1q9FXmp39s75jr9hPNqBUpaZpBmG8z28MxIsxiije2ZOBsuE4OGI/1/bcSGjGC3jGweFUPIWJ2MC4Jclx3grHlZRmOpQ7oAxqvhGaJaVK67tfeUeDlIocOarhZcAESmg2yorFYc+uA9VbLqO1qex5Oi5ttUShX3HYY8ENK8dLgZosUskw4ngjWXFOy0f1BvnLWYbcu6tPTrf0V3YbPdfM8RbjGLtJZrf+xlnVCuF/MVx1I/iASTo0pu1V5HHeB7oel1knA84/Lrox/CcyeTPHeH2hiE1SFraqAvUMD3y0YwJ/PyMRQ9cwphVYSB1mLeFnesTzXW/B9mqjuEcxdsAoiA+1gCmfiUQW8X2J/R52IAT8uxxDj8Z9jPoR5GdK9TeN8CqHsOB2cbXehYspj2wb6xCnOHWBXPndeLN8J0RbBmjA9ykizt65S60ZHL6rjPz4cxV856a0wkpsG2jON/k6MPbYoiP0Kb1rUai4PQ43jWVp7gQZjt3azswFu7DuuA2Wr0ljxNQ77UNkCP/1tZ6Wx4N',
            '__VIEWSTATEGENERATOR': '7AD7E509',
            'p1$ChengNuo': 'p1_ChengNuo',
            'p1$BaoSRQ': date,
            'p1$DangQSTZK': '良好',
            'p1$TiWen': '37',
            'p1$ZaiXiao': '不在校',
            'p1$GuoNei': '国内',
            'p1$DangQSZD': '上海',
            'p1$ddlSheng$Value': '上海',
            'p1$ddlSheng': '上海',
            'p1$ddlShi$Value': '上海市',
            'p1$ddlShi': '上海市',
            'p1$ddlXian$Value': '浦东新区',
            'p1$ddlXian': '浦东新区',
            'p1$XiangXDZ': '浦东新区', #  家庭住址
            'p1$QueZHZJC$Value': '否',
            'p1$QueZHZJC': '否',
            'p1$DaoXQLYGJ': '',
            'p1$DaoXQLYCS': '',
            'p1$CengFWH_RiQi': '',
            'p1$CengFWH_BeiZhu': '',
            'p1$JieChu_RiQi': '',
            'p1$JieChu_BeiZhu': '',
            'p1$TuJWH_RiQi': '',
            'p1$TuJWH_BeiZhu': '',
            'p1$JiaRen_BeiZhu': '',
            'p1$Address2': '中国上海市上海市浦东新区世纪大道2001号',
            'p1_Collapsed': 'false',
            'F_STATE': 'eyJwMV9CYW9TUlEiOnsiVGV4dCI6IjIwMjAtMDItMTcifSwicDFfRGFuZ1FTVFpLIjp7IkZfSXRlbXMiOltbIuiJr+WlvSIsIuiJr+WlvSIsMV0sWyLkuI3pgIIiLCLkuI3pgIIiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuiJr+WlvSJ9LCJwMV9aaGVuZ1podWFuZyI6eyJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIuaEn+WGkiIsIuaEn+WGkiIsMV0sWyLlkrPll70iLCLlkrPll70iLDFdLFsi5Y+R54OtIiwi5Y+R54OtIiwxXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9aYWlYaWFvIjp7IkZfSXRlbXMiOltbIuS4jeWcqOagoSIsIuS4jeWcqOagoSIsMV0sWyLlrp3lsbEiLCLlrp3lsbHmoKHljLoiLDFdLFsi5bu26ZW/Iiwi5bu26ZW/5qCh5Yy6IiwxXSxbIuWYieWumiIsIuWYieWumuagoeWMuiIsMV0sWyLmlrDpl7jot68iLCLmlrDpl7jot6/moKHljLoiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuS4jeWcqOagoSJ9LCJwMV9HdW9OZWkiOnsiRl9JdGVtcyI6W1si5Zu95YaFIiwi5Zu95YaFIiwxXSxbIuWbveWkliIsIuWbveWkliIsMV1dLCJTZWxlY3RlZFZhbHVlIjoi5Zu95YaFIn0sInAxX0RhbmdRU1pEIjp7IlJlcXVpcmVkIjp0cnVlLCJTZWxlY3RlZFZhbHVlIjoi5LiK5rW3IiwiRl9JdGVtcyI6W1si5LiK5rW3Iiwi5LiK5rW3IiwxXSxbIua5luWMlyIsIua5luWMlyIsMV0sWyLlhbbku5YiLCLlhbbku5YiLDFdXX0sInAxX2RkbFNoZW5nIjp7IkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup55yB5Lu9IiwxLCIiLCIiXSxbIuWMl+S6rCIsIuWMl+S6rCIsMSwiIiwiIl0sWyLlpKnmtKUiLCLlpKnmtKUiLDEsIiIsIiJdLFsi5LiK5rW3Iiwi5LiK5rW3IiwxLCIiLCIiXSxbIumHjeW6hiIsIumHjeW6hiIsMSwiIiwiIl0sWyLmsrPljJciLCLmsrPljJciLDEsIiIsIiJdLFsi5bGx6KW/Iiwi5bGx6KW/IiwxLCIiLCIiXSxbIui+veWugSIsIui+veWugSIsMSwiIiwiIl0sWyLlkInmnpciLCLlkInmnpciLDEsIiIsIiJdLFsi6buR6b6Z5rGfIiwi6buR6b6Z5rGfIiwxLCIiLCIiXSxbIuaxn+iLjyIsIuaxn+iLjyIsMSwiIiwiIl0sWyLmtZnmsZ8iLCLmtZnmsZ8iLDEsIiIsIiJdLFsi5a6J5b69Iiwi5a6J5b69IiwxLCIiLCIiXSxbIuemj+W7uiIsIuemj+W7uiIsMSwiIiwiIl0sWyLmsZ/opb8iLCLmsZ/opb8iLDEsIiIsIiJdLFsi5bGx5LicIiwi5bGx5LicIiwxLCIiLCIiXSxbIuays+WNlyIsIuays+WNlyIsMSwiIiwiIl0sWyLmuZbljJciLCLmuZbljJciLDEsIiIsIiJdLFsi5rmW5Y2XIiwi5rmW5Y2XIiwxLCIiLCIiXSxbIuW5v+S4nCIsIuW5v+S4nCIsMSwiIiwiIl0sWyLmtbfljZciLCLmtbfljZciLDEsIiIsIiJdLFsi5Zub5bedIiwi5Zub5bedIiwxLCIiLCIiXSxbIui0teW3niIsIui0teW3niIsMSwiIiwiIl0sWyLkupHljZciLCLkupHljZciLDEsIiIsIiJdLFsi6ZmV6KW/Iiwi6ZmV6KW/IiwxLCIiLCIiXSxbIueUmOiCgyIsIueUmOiCgyIsMSwiIiwiIl0sWyLpnZLmtbciLCLpnZLmtbciLDEsIiIsIiJdLFsi5YaF6JKZ5Y+kIiwi5YaF6JKZ5Y+kIiwxLCIiLCIiXSxbIuW5v+ilvyIsIuW5v+ilvyIsMSwiIiwiIl0sWyLopb/ol48iLCLopb/ol48iLDEsIiIsIiJdLFsi5a6B5aSPIiwi5a6B5aSPIiwxLCIiLCIiXSxbIuaWsOeWhiIsIuaWsOeWhiIsMSwiIiwiIl0sWyLpppnmuK8iLCLpppnmuK8iLDEsIiIsIiJdLFsi5r6z6ZeoIiwi5r6z6ZeoIiwxLCIiLCIiXSxbIuWPsOa5viIsIuWPsOa5viIsMSwiIiwiIlF_STATE1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5LiK5rW3Il19LCJwMV9kZGxTaGkiOnsiRW5hYmxlZCI6dHJ1ZSwiRl9JdGVtcyI6W1siLTEiLCLpgInmi6nluIIiLDEsIiIsIiJdLFsi5LiK5rW35biCIiwi5LiK5rW35biCIiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyLkuIrmtbfluIIiXX0sInAxX2RkbFhpYW4iOnsiRW5hYmxlZCI6dHJ1ZSwiRl9JdGVtcyI6W1siLTEiLCLpgInmi6nljr/ljLoiLDEsIiIsIiJdLFsi6buE5rWm5Yy6Iiwi6buE5rWm5Yy6IiwxLCIiLCIiXSxbIuWNoua5vuWMuiIsIuWNoua5vuWMuiIsMSwiIiwiIl0sWyLlvpDmsYfljLoiLCLlvpDmsYfljLoiLDEsIiIsIiJdLFsi6ZW/5a6B5Yy6Iiwi6ZW/5a6B5Yy6IiwxLCIiLCIiXSxbIumdmeWuieWMuiIsIumdmeWuieWMuiIsMSwiIiwiIl0sWyLmma7pmYDljLoiLCLmma7pmYDljLoiLDEsIiIsIiJdLFsi6Jm55Y+j5Yy6Iiwi6Jm55Y+j5Yy6IiwxLCIiLCIiXSxbIuadqOa1puWMuiIsIuadqOa1puWMuiIsMSwiIiwiIl0sWyLlrp3lsbHljLoiLCLlrp3lsbHljLoiLDEsIiIsIiJdLFsi6Ze16KGM5Yy6Iiwi6Ze16KGM5Yy6IiwxLCIiLCIiXSxbIuWYieWumuWMuiIsIuWYieWumuWMuiIsMSwiIiwiIl0sWyLmnb7msZ/ljLoiLCLmnb7msZ/ljLoiLDEsIiIsIiJdLFsi6YeR5bGx5Yy6Iiwi6YeR5bGx5Yy6IiwxLCIiLCIiXSxbIumdkua1puWMuiIsIumdkua1puWMuiIsMSwiIiwiIl0sWyLlpYnotKTljLoiLCLlpYnotKTljLoiLDEsIiIsIiJdLFsi5rWm5Lic5paw5Yy6Iiwi5rWm5Lic5paw5Yy6IiwxLCIiLCIiXSxbIuW0h+aYjuWMuiIsIuW0h+aYjuWMuiIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5rWm5Lic5paw5Yy6Il19LCJwMV9YaWFuZ1hEWiI6eyJMYWJlbCI6IuWbveWGheivpue7huWcsOWdgCIsIlRleHQiOiLogIDljY7ot680MjHlvIQxNeWPtzcwMiJ9LCJwMV9RdWVaSFpKQyI6eyJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDEsIiIsIiJdLFsi5ZCmIiwi5ZCmIiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyLlkKYiXX0sInAxX0NlbmdGV0giOnsiTGFiZWwiOiIyMDIw5bm0MeaciDEw5pel5ZCO5piv5ZCm5Zyo5rmW5YyX6YCX55WZ6L+HIn0sInAxX0NlbmdGV0hfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9DZW5nRldIX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWVDaHUiOnsiTGFiZWwiOiIwMuaciDAz5pel6IezMDLmnIgxN+aXpeaYr+WQpuS4juadpeiHqua5luWMl+WPkeeDreS6uuWRmOWvhuWIh+aOpeinpiJ9LCJwMV9KaWVDaHVfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWVDaHVfQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1R1SldIIjp7IkxhYmVsIjoiMDLmnIgwM+aXpeiHszAy5pyIMTfml6XmmK/lkKbkuZjlnZDlhazlhbHkuqTpgJrpgJTlvoTmuZbljJcifSwicDFfVHVKV0hfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9UdUpXSF9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfSmlhUmVuIjp7IkxhYmVsIjoiMDLmnIgwM+aXpeiHszAy5pyIMTfml6XlrrbkurrmmK/lkKbmnInlj5Hng63nrYnnl4fnirYifSwicDFfSmlhUmVuX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9BZGRyZXNzMiI6eyJUZXh0Ijoi5Lit5Zu95LiK5rW35biC5LiK5rW35biC5rWm5Lic5paw5Yy65LiW57qq5aSn6YGTMjAwMeWPtyJ9LCJwMSI6eyJJRnJhbWVBdHRyaWJ1dGVzIjp7fX19',
            'F_TARGET': 'p1_ctl00_btnSubmit',
        }

    def login(self):
        while True:
            try:
                self.session.headers = {}
                self.data = {'username': self.username, 'password': self.password, 'login_submit': '登录'}
                self.session.post('https://newsso.shu.edu.cn/login', data=self.data, timeout=10)
                ret = self.session.get('http://selfreport.shu.edu.cn/', timeout=10)
                assert ret.text.find('健康之路') != -1, '登录失败'
                print('登录成功')
                sleep(1)
            except Exception as ERR:
                print('ERR in Client::login: ' + str(ERR))
                sleep(5)
                continue
            break

    def run(self):
        while True:
            try:
                self.report_data['p1$TiWen'] = str(36+randint(2, 10)/10.0)
                self.session.post('http://selfreport.shu.edu.cn/DayReport.aspx', data=self.report_data, timeout=10)
            except Exception as ERR:
                print('ERR in Client::run: ' + str(ERR))
                sleep(10)
                continue
            print(self.report_data['p1$TiWen'], end=', ', flush=True)
            sleep(5)  # 太快就是作死


def main():
    client = Client('username', 'password', '2020-02-16')
    client.login()
    client.run()


if __name__ == '__main__':
    main()
