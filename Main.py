import argparse
import base64
import datetime
import logging
import random
import re
import sys

from pyquery import PyQuery
from requests import session
from retry import retry

homeURL = 'http://selfreport.shu.edu.cn/'
loginURL = 'https://newsso.shu.edu.cn/login'
reportURL = 'http://selfreport.shu.edu.cn/DayReport.aspx'
template = r'{"p1_BaoSRQ":{"Text":"%s"},"p1_DangQSTZK":{"F_Items":[["良好","良好",1],["不适","不适",1]],"SelectedValue":"良好"},"p1_ZhengZhuang":{"Hidden":true,"F_Items":[["感冒","感冒",1],["咳嗽","咳嗽",1],["发热","发热",1]],"SelectedValueArray":[]},"p1_ZaiXiao":{"F_Items":[["不在校","不在校",1],["宝山","宝山校区",1],["延长","延长校区",1],["嘉定","嘉定校区",1],["新闸路","新闸路校区",1]],"SelectedValue":"%s"},"p1_GuoNei":{"F_Items":[["国内","国内",1],["国外","国外",1]],"SelectedValue":"%s"},"p1_DangQSZD":{"Required":true,"SelectedValue":"%s","F_Items":[["上海","上海",1],["湖北","湖北",1],["其他","其他",1]]},"p1_ddlSheng":{"F_Items":[["-1","选择省份",1,"",""],["北京","北京",1,"",""],["天津","天津",1,"",""],["上海","上海",1,"",""],["重庆","重庆",1,"",""],["河北","河北",1,"",""],["山西","山西",1,"",""],["辽宁","辽宁",1,"",""],["吉林","吉林",1,"",""],["黑龙江","黑龙江",1,"",""],["江苏","江苏",1,"",""],["浙江","浙江",1,"",""],["安徽","安徽",1,"",""],["福建","福建",1,"",""],["江西","江西",1,"",""],["山东","山东",1,"",""],["河南","河南",1,"",""],["湖北","湖北",1,"",""],["湖南","湖南",1,"",""],["广东","广东",1,"",""],["海南","海南",1,"",""],["四川","四川",1,"",""],["贵州","贵州",1,"",""],["云南","云南",1,"",""],["陕西","陕西",1,"",""],["甘肃","甘肃",1,"",""],["青海","青海",1,"",""],["内蒙古","内蒙古",1,"",""],["广西","广西",1,"",""],["西藏","西藏",1,"",""],["宁夏","宁夏",1,"",""],["新疆","新疆",1,"",""],["香港","香港",1,"",""],["澳门","澳门",1,"",""],["台湾","台湾",1,"",""]],"SelectedValueArray":["%s"]},"p1_ddlShi":{"Enabled":true,"F_Items":%s,"SelectedValueArray":["%s"]},"p1_ddlXian":{"Enabled":true,"F_Items":%s,"SelectedValueArray":["%s"]},"p1_XiangXDZ":{"Label":"国内详细地址","Text":"%s"},"p1_QueZHZJC":{"F_Items":[["是","是",1,"",""],["否","否",1,"",""]],"SelectedValueArray":["%s"]},"p1_CengFWH":{"Label":"2020年1月10日后是否在湖北逗留过"},"p1_CengFWH_RiQi":{"Hidden":true},"p1_CengFWH_BeiZhu":{"Hidden":true},"p1_JieChu":{"Label":"01月26日至02月09日是否与来自湖北发热人员密切接触"},"p1_JieChu_RiQi":{"Hidden":true},"p1_JieChu_BeiZhu":{"Hidden":true},"p1_TuJWH":{"Label":"01月26日至02月09日是否乘坐公共交通途径湖北"},"p1_TuJWH_RiQi":{"Hidden":true},"p1_TuJWH_BeiZhu":{"Hidden":true},"p1_JiaRen":{"Label":"01月26日至02月09日家人是否有发热等症状"},"p1_JiaRen_BeiZhu":{"Hidden":true},"p1":{"IFrameAttributes":{}}}'


class Client:

    def __init__(self, username, password, date):
        self.session = session()
        self.username = username
        self.password = password
        self.date = date
        self.data = {}

    @retry(tries=5, logger=logging)
    def login(self):
        self.session.headers = {}
        self.data = {'username': self.username, 'password': self.password, 'login_submit': '登录'}
        self.session.post(loginURL, data=self.data, timeout=10)
        resp = self.session.get(homeURL, timeout=10)
        assert resp.status_code == 200, 'GET URL %s returns %d' % (homeURL, resp.status_code)
        assert '健康之路' in resp.text, '登录失败'
        logging.info('登录成功')

    def __get_data(self):
        resp = self.session.get('http://selfreport.shu.edu.cn/DayReport.aspx')
        doc = PyQuery(resp.text)
        html = doc.html()
        zxMatch = re.findall(r'f7_state={.+?"SelectedValue":"(.+?)"', html)[0]
        gnMatch = re.findall(r'f8_state={.+?"SelectedValue":"(.+?)"', html)[0]
        szMatch = re.findall(r'f9_state={.+?"SelectedValue":"(.+?)"', html)[0]
        shengMatch = re.findall(r'f10_state={.+?"SelectedValueArray":\["(.+?)"]', html)[0]
        shiMatch = re.findall(r'f11_state={.+?"F_Items":(.+?),"SelectedValueArray":\["(.+?)"]', html)[0]
        xianMatch = re.findall(r'f12_state={.+?"F_Items":(.+?),"SelectedValueArray":\["(.+?)"]', html)[0]
        xxMatch = re.findall(r'f13_state={.+?"Text":"(.+?)"', html)[0]
        jcMatch = re.findall(r'f14_state={.+?"SelectedValueArray":\["(.+?)"]', html)[0]
        F_State = template % (self.date, zxMatch, gnMatch, szMatch, shengMatch, *shiMatch, *xianMatch, xxMatch, jcMatch)
        return {
            'F_State': base64.b64encode(F_State.encode()),
            '__VIEWSTATE': doc.find('#__VIEWSTATE').attr('value'),
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEGENERATOR': doc.find('#__VIEWSTATEGENERATOR').attr('value'),
            'p1$ChengNuo': 'p1$ChengNuo',
            'p1$BaoSRQ': self.date,
            'p1$DangQSTZK': '良好',
            'p1$TiWen': str(36 + random.randint(2, 10) / 10.0),
            'F_TARGET': 'p1_ctl00_btnSubmit',
            'p1_Collapsed': 'false',
            'p1$CengFWH_RiQi': '',
            'p1$CengFWH_BeiZhu': '',
            'p1$JieChu_RiQi': '',
            'p1$JieChu_BeiZhu': '',
            'p1$TuJWH_RiQi': '',
            'p1$TuJWH_BeiZhu': '',
            'p1$JiaRen_BeiZhu': '',
            'p1$ZaiXiao': zxMatch,
            'p1$GuoNei': gnMatch,
            'p1$DangQSZD': szMatch,
            'p1$ddlSheng$Value': shengMatch,
            'p1$ddlShi$Value': shiMatch[1],
            'p1$ddlXian$Value': xianMatch[1],
            'p1$XiangXDZ': xxMatch,
            'p1$QueZHZJC$Value': jcMatch,
            'p1$QueZHZJC': '否',  # 返沪返校途中
            'p1$DaoXQLYGJ': '',  # 旅游国家
            'p1$DaoXQLYCS': '',  # 旅游城市
            'p1$Address2': '中国'
        }

    def run(self):
        report_data = self.__get_data()
        msg_pattern = re.compile(r'(?<=F.alert\({message:\')(.*?)(?=\',)')

        @retry(tries=10, delay=1, max_delay=64, backoff=2, logger=logging)
        def submit(data):
            resp = self.session.post(reportURL, data=data, timeout=10)
            assert resp.status_code == 200, 'POST %s returns %d' % (reportURL, resp.status_code)
            msg = msg_pattern.findall(resp.text)[0]
            assert msg == '提交成功', msg
            return msg

        msg = submit(report_data)
        logging.info(msg + ': ' + report_data['p1$TiWen'])


def arg_parser():
    def log_level(arg_value, pat=re.compile(r'(debug|info|warning|error|critical)', re.IGNORECASE)):
        if not pat.match(arg_value):
            raise argparse.ArgumentParser
        return arg_value

    parser = argparse.ArgumentParser(description='SHU 自动报告 ncov 的脚本。')
    parser.add_argument('username', help='一卡通账号')
    parser.add_argument('password', help='一卡通密码')
    parser.add_argument('-d', '--date', help='上报日期',
                        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(),
                        default=datetime.date.today())
    parser.add_argument('-l', '--log_level', default='info', type=log_level,
                        help='日志级别 (debug, info, warning, error, critical)')
    return parser


def main():
    args = arg_parser().parse_args()
    fmt = "%(levelname)s %(message)s"
    logging.basicConfig(stream=sys.stdout, format=fmt, level=eval("logging." + args.log_level.upper()))

    client = Client(args.username, args.password, args.date)
    try:
        client.login()
        client.run()
    except Exception as ERR:
        logging.error(str(ERR))
        exit(1)


if __name__ == '__main__':
    main()
