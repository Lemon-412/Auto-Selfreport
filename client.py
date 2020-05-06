import base64
import datetime
import logging
import random
import re
import time

from pyquery import PyQuery
from requests import session
from retry import retry

from config import *


class TooEarlyError(Exception):
    pass


class Client(object):

    def __init__(self, username, password, date):
        super().__init__()
        self.session = session()
        self.username = username
        self.password = password
        self.date = date
        self.submit_data = None
        self.exitcode = 0

    @retry(tries=5, logger=logging)
    def _login(self):
        self.session.headers = {}
        data = {'username': self.username, 'password': self.password, 'login_submit': '登录'}
        self.session.post(loginURL, data=data, timeout=10)
        resp = self.session.get(reportURL, timeout=10)
        time.sleep(5)
        assert resp.status_code == 200, 'GET URL %s returns %d' % (homeURL, resp.status_code)
        assert '每日一报' in resp.text, '登录失败'
        logging.info('登录成功')

    def __get_data(self):
        if self.submit_data is not None:
            return self.submit_data
        # data = {'day': (self.date - datetime.timedelta(days=1))}
        resp = self.session.get(reportURL)
        doc = PyQuery(resp.text)
        html = doc.html()
        zxMatch = re.findall(r'f8_state={.*?"SelectedValue":"(.+?)"', html)[0]
        gnMatch = "国内"
        shengMatch = re.findall(r'f16_state={.*?"SelectedValueArray":\["(.+?)"]', html)[0]
        shiMatch = re.findall(r'f17_state={.*?"F_Items":(.+?),"SelectedValueArray":\["(.+?)"]', html)[0]
        xianMatch = re.findall(r'f18_state={.*?"F_Items":(.+?),"SelectedValueArray":\["(.+?)"]', html)[0]
        tzMatch = re.findall(r'f19_state={.*?"SelectedValue":"(.+?)"', html)
        xxMatch = re.findall(r'f20_state={.*?"Text":"(.+?)"', html)[0]
        jcMatch = "否"
        ssMatch = re.findall(r'f43_state={.*?"SelectedValue":"(.+?)"', html)
        if len(tzMatch) and len(ssMatch):  # 上海
            F_State = re.sub(r'\s+', '', template[0]) % (
                self.date, zxMatch, gnMatch, shengMatch, *shiMatch, *xianMatch,
                tzMatch[0], xxMatch, jcMatch, ssMatch[0])
            shanghai = True
        else:
            F_State = re.sub(r'\s+', '', template[1]) % (
                self.date, zxMatch, gnMatch, shengMatch, *shiMatch, *xianMatch, xxMatch, jcMatch)
            shanghai = False

        # resp = self.session.get(reportURL, params=data)
        # doc = PyQuery(resp.text)

        self.submit_data = {
            'F_State': base64.b64encode(F_State.encode()),
            '__VIEWSTATE': doc.find('#__VIEWSTATE').attr('value'),
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEGENERATOR': doc.find('#__VIEWSTATEGENERATOR').attr('value'),
            'p1$ChengNuo': 'p1_ChengNuo',
            'p1$BaoSRQ': self.date,
            'p1$DangQSTZK': '良好',
            'p1$TiWen': random.randint(1, 6) * 0.1 + 36,
            'F_TARGET': 'p1_ctl00_btnSubmit',
            'p1$BanChe_1$Value': 0,
            'p1$BanChe_1': '不需要乘班车',
            'p1$BanChe_2$Value': 0,
            'p1$BanChe_2': '不需要乘班车',
            'p1$CengFWH_RiQi': '',
            'p1$CengFWH_BeiZhu': '',
            'p1$JieChu_RiQi': '',
            'p1$JieChu_BeiZhu': '',
            'p1$TuJWH_RiQi': '',
            'p1$TuJWH_BeiZhu': '',
            'p1$JiaRen_BeiZhu': '',
            'p1$ZaiXiao': zxMatch,
            'p1$MingTDX': '不到校',
            'p1$MingTJC': '否',
            'p1$GuoNei': gnMatch,
            'p1$ddlGuoJia$Value': -1,
            'p1$ddlGuoJia': '选择国家',
            'p1$ddlSheng$Value': shengMatch,
            'p1$ddlSheng': shengMatch,
            'p1$ddlShi$Value': shiMatch[1],
            'p1$ddlShi': shiMatch[1],
            'p1$ddlXian$Value': xianMatch[1],
            'p1$ddlXian': xianMatch[1],
            'p1$XiangXDZ': xxMatch,
            'p1$QueZHZJC$Value': jcMatch,
            'p1$QueZHZJC': jcMatch,
            'p1$DangRGL': '否',
            'p1$DaoXQLYGJ': '',  # 旅游国家
            'p1$DaoXQLYCS': '',  # 旅游城市
            'p1$LvMa14Days': '是',
            'p1$Address2': '',
            'p1$GeLDZ': '',
            'p1_BanCSM_Collapsed': 'false',
            'p1_SuiSMSM_Collapsed': 'false',
            'p1_Collapsed': 'false'
        }
        if shanghai:
            self.submit_data['p1$TongZWDLH'] = tzMatch[0]
            self.submit_data['p1$SuiSM'] = ssMatch[0]
        return self.submit_data

    @retry(TooEarlyError, delay=1, logger=logging)
    def _report(self):
        report_data = self.__get_data()
        msg_pattern = re.compile(r'F.alert\({message:\'(.*?)\',')

        @retry(tries=5, delay=1, logger=logging)
        def submit(data):
            resp = self.session.post(reportURL, data=data, headers=header, timeout=10)
            assert resp.status_code == 200, 'POST %s returns %d' % (reportURL, resp.status_code)
            msg = msg_pattern.findall(resp.text)[0]
            assert msg == '提交成功' or msg == '只能填报当天或补填以前的信息', msg
            return msg

        msg = submit(report_data)
        if msg == '只能填报当天或补填以前的信息':
            raise TooEarlyError(msg)
        logging.info(msg + ' ' + str(report_data['p1$TiWen']))

    def run(self):
        try:
            self._login()
            self._report()
        except Exception as ERR:
            logging.error(str(ERR))
            self.exitcode = 1
