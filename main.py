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

homeURL = 'https://selfreport.shu.edu.cn/'
loginURL = 'https://newsso.shu.edu.cn/login'
reportURL = 'https://selfreport.shu.edu.cn/DayReport.aspx'
template = r'{"p1_BaoSRQ":{"Text":"%s"},"p1_DangQSTZK":{"F_Items":[["良好","良好",1],["不适","不适",1]],"SelectedValue":"良好"},"p1_ZhengZhuang":{"Hidden":true,"F_Items":[["感冒","感冒",1],["咳嗽","咳嗽",1],["发热","发热",1]],"SelectedValueArray":[]},"p1_ZaiXiao":{"F_Items":[["不在校","不在校",1],["宝山","宝山校区",1],["延长","延长校区",1],["嘉定","嘉定校区",1],["新闸路","新闸路校区",1]],"SelectedValue":"%s"},"p1_GuoNei":{"F_Items":[["国内","国内",1],["国外","国外",1]],"SelectedValue":"%s"},"p1_ddlGuoJia":{"DataTextField":"ZhongWen","DataValueField":"ZhongWen","Hidden":true,"F_Items":[["-1","选择国家",1,"",""],["阿尔巴尼亚","阿尔巴尼亚",1,"",""],["阿尔及利亚","阿尔及利亚",1,"",""],["阿富汗","阿富汗",1,"",""],["阿根廷","阿根廷",1,"",""],["阿拉伯联合酋长国","阿拉伯联合酋长国",1,"",""],["阿鲁巴","阿鲁巴",1,"",""],["阿曼","阿曼",1,"",""],["阿塞拜疆","阿塞拜疆",1,"",""],["埃及","埃及",1,"",""],["埃塞俄比亚","埃塞俄比亚",1,"",""],["爱尔兰","爱尔兰",1,"",""],["爱沙尼亚","爱沙尼亚",1,"",""],["安道尔","安道尔",1,"",""],["安哥拉","安哥拉",1,"",""],["安圭拉","安圭拉",1,"",""],["安提瓜和巴布达","安提瓜和巴布达",1,"",""],["奥地利","奥地利",1,"",""],["奥兰群岛","奥兰群岛",1,"",""],["澳大利亚","澳大利亚",1,"",""],["巴巴多斯","巴巴多斯",1,"",""],["巴布亚新几内亚","巴布亚新几内亚",1,"",""],["巴哈马","巴哈马",1,"",""],["巴基斯坦","巴基斯坦",1,"",""],["巴勒斯坦","巴勒斯坦",1,"",""],["巴林","巴林",1,"",""],["巴拿马","巴拿马",1,"",""],["巴西","巴西",1,"",""],["白俄罗斯","白俄罗斯",1,"",""],["百慕大","百慕大",1,"",""],["保加利亚","保加利亚",1,"",""],["贝宁","贝宁",1,"",""],["比利时","比利时",1,"",""],["冰岛","冰岛",1,"",""],["波多黎各","波多黎各",1,"",""],["波兰","波兰",1,"",""],["波斯尼亚和黑塞哥维那","波斯尼亚和黑塞哥维那",1,"",""],["玻利维亚","玻利维亚",1,"",""],["伯利兹","伯利兹",1,"",""],["博茨瓦纳","博茨瓦纳",1,"",""],["不丹","不丹",1,"",""],["布基纳法索","布基纳法索",1,"",""],["布隆迪","布隆迪",1,"",""],["布维岛","布维岛",1,"",""],["朝鲜","朝鲜",1,"",""],["赤道几内亚","赤道几内亚",1,"",""],["丹麦","丹麦",1,"",""],["德国","德国",1,"",""],["东帝汶","东帝汶",1,"",""],["东帝汶","东帝汶",1,"",""],["多哥","多哥",1,"",""],["多米尼加","多米尼加",1,"",""],["俄罗斯联邦","俄罗斯联邦",1,"",""],["厄瓜多尔","厄瓜多尔",1,"",""],["厄立特里亚","厄立特里亚",1,"",""],["法国","法国",1,"",""],["法国大都会","法国大都会",1,"",""],["法罗群岛","法罗群岛",1,"",""],["法属波利尼西亚","法属波利尼西亚",1,"",""],["法属圭亚那","法属圭亚那",1,"",""],["梵蒂冈","梵蒂冈",1,"",""],["菲律宾","菲律宾",1,"",""],["斐济","斐济",1,"",""],["芬兰","芬兰",1,"",""],["佛得角","佛得角",1,"",""],["冈比亚","冈比亚",1,"",""],["刚果","刚果",1,"",""],["刚果（金）","刚果（金）",1,"",""],["哥伦比亚","哥伦比亚",1,"",""],["哥斯达黎加","哥斯达黎加",1,"",""],["格林纳达","格林纳达",1,"",""],["格鲁吉亚","格鲁吉亚",1,"",""],["根西岛","根西岛",1,"",""],["古巴","古巴",1,"",""],["瓜德罗普岛","瓜德罗普岛",1,"",""],["关岛","关岛",1,"",""],["圭亚那","圭亚那",1,"",""],["哈萨克斯坦","哈萨克斯坦",1,"",""],["海地","海地",1,"",""],["韩国","韩国",1,"",""],["荷兰","荷兰",1,"",""],["黑山","黑山",1,"",""],["洪都拉斯","洪都拉斯",1,"",""],["基里巴斯","基里巴斯",1,"",""],["吉布提","吉布提",1,"",""],["吉尔吉斯斯坦","吉尔吉斯斯坦",1,"",""],["几内亚","几内亚",1,"",""],["几内亚比绍","几内亚比绍",1,"",""],["加拿大","加拿大",1,"",""],["加纳","加纳",1,"",""],["加蓬","加蓬",1,"",""],["柬埔寨","柬埔寨",1,"",""],["捷克","捷克",1,"",""],["津巴布韦","津巴布韦",1,"",""],["喀麦隆","喀麦隆",1,"",""],["卡塔尔","卡塔尔",1,"",""],["科科斯（基林）群岛","科科斯（基林）群岛",1,"",""],["科摩罗","科摩罗",1,"",""],["科特迪瓦","科特迪瓦",1,"",""],["科威特","科威特",1,"",""],["克罗地亚","克罗地亚",1,"",""],["肯尼亚","肯尼亚",1,"",""],["库克群岛","库克群岛",1,"",""],["拉脱维亚","拉脱维亚",1,"",""],["莱索托","莱索托",1,"",""],["老挝","老挝",1,"",""],["黎巴嫩","黎巴嫩",1,"",""],["立陶宛","立陶宛",1,"",""],["利比里亚","利比里亚",1,"",""],["利比亚","利比亚",1,"",""],["列支敦士登","列支敦士登",1,"",""],["留尼汪岛","留尼汪岛",1,"",""],["卢森堡","卢森堡",1,"",""],["卢旺达","卢旺达",1,"",""],["罗马尼亚","罗马尼亚",1,"",""],["马达加斯加","马达加斯加",1,"",""],["马恩岛","马恩岛",1,"",""],["马尔代夫","马尔代夫",1,"",""],["马耳他","马耳他",1,"",""],["马拉维","马拉维",1,"",""],["马来西亚","马来西亚",1,"",""],["马里","马里",1,"",""],["马其顿","马其顿",1,"",""],["马绍尔群岛","马绍尔群岛",1,"",""],["马提尼克岛","马提尼克岛",1,"",""],["马约特","马约特",1,"",""],["毛里求斯","毛里求斯",1,"",""],["毛里塔尼亚","毛里塔尼亚",1,"",""],["美国","美国",1,"",""],["美属萨摩亚","美属萨摩亚",1,"",""],["蒙古","蒙古",1,"",""],["蒙特塞拉特","蒙特塞拉特",1,"",""],["孟加拉","孟加拉",1,"",""],["秘鲁","秘鲁",1,"",""],["密克罗尼西亚","密克罗尼西亚",1,"",""],["缅甸","缅甸",1,"",""],["摩尔多瓦","摩尔多瓦",1,"",""],["摩洛哥","摩洛哥",1,"",""],["摩纳哥","摩纳哥",1,"",""],["莫桑比克","莫桑比克",1,"",""],["墨西哥","墨西哥",1,"",""],["纳米比亚","纳米比亚",1,"",""],["南非","南非",1,"",""],["南斯拉夫","南斯拉夫",1,"",""],["瑙鲁","瑙鲁",1,"",""],["尼泊尔","尼泊尔",1,"",""],["尼加拉瓜","尼加拉瓜",1,"",""],["尼日尔","尼日尔",1,"",""],["尼日利亚","尼日利亚",1,"",""],["纽埃","纽埃",1,"",""],["挪威","挪威",1,"",""],["诺福克岛","诺福克岛",1,"",""],["帕劳","帕劳",1,"",""],["皮特凯恩群岛","皮特凯恩群岛",1,"",""],["葡萄牙","葡萄牙",1,"",""],["日本","日本",1,"",""],["瑞典","瑞典",1,"",""],["瑞士","瑞士",1,"",""],["萨尔瓦多","萨尔瓦多",1,"",""],["萨摩亚","萨摩亚",1,"",""],["塞尔维亚","塞尔维亚",1,"",""],["塞拉利昂","塞拉利昂",1,"",""],["塞内加尔","塞内加尔",1,"",""],["塞浦路斯","塞浦路斯",1,"",""],["塞舌尔","塞舌尔",1,"",""],["沙特阿拉伯","沙特阿拉伯",1,"",""],["圣诞岛","圣诞岛",1,"",""],["圣多美和普林西比","圣多美和普林西比",1,"",""],["圣赫勒拿","圣赫勒拿",1,"",""],["圣基茨和尼维斯","圣基茨和尼维斯",1,"",""],["圣卢西亚","圣卢西亚",1,"",""],["圣马力诺","圣马力诺",1,"",""],["圣文森特和格林纳丁斯","圣文森特和格林纳丁斯",1,"",""],["斯里兰卡","斯里兰卡",1,"",""],["斯洛伐克","斯洛伐克",1,"",""],["斯洛文尼亚","斯洛文尼亚",1,"",""],["斯威士兰","斯威士兰",1,"",""],["苏丹","苏丹",1,"",""],["苏里南","苏里南",1,"",""],["所罗门群岛","所罗门群岛",1,"",""],["索马里","索马里",1,"",""],["塔吉克斯坦","塔吉克斯坦",1,"",""],["泰国","泰国",1,"",""],["坦桑尼亚","坦桑尼亚",1,"",""],["汤加","汤加",1,"",""],["特立尼达和多巴哥","特立尼达和多巴哥",1,"",""],["突尼斯","突尼斯",1,"",""],["图瓦卢","图瓦卢",1,"",""],["土耳其","土耳其",1,"",""],["土库曼斯坦","土库曼斯坦",1,"",""],["托克劳","托克劳",1,"",""],["瓦利斯群岛和富图纳群岛","瓦利斯群岛和富图纳群岛",1,"",""],["瓦努阿图","瓦努阿图",1,"",""],["危地马拉","危地马拉",1,"",""],["委内瑞拉","委内瑞拉",1,"",""],["文莱","文莱",1,"",""],["乌干达","乌干达",1,"",""],["乌克兰","乌克兰",1,"",""],["乌拉圭","乌拉圭",1,"",""],["乌兹别克斯坦","乌兹别克斯坦",1,"",""],["西班牙","西班牙",1,"",""],["西撒哈拉","西撒哈拉",1,"",""],["希腊","希腊",1,"",""],["新加坡","新加坡",1,"",""],["新喀里多尼亚","新喀里多尼亚",1,"",""],["新西兰","新西兰",1,"",""],["匈牙利","匈牙利",1,"",""],["叙利亚","叙利亚",1,"",""],["牙买加","牙买加",1,"",""],["亚美尼亚","亚美尼亚",1,"",""],["也门","也门",1,"",""],["伊拉克","伊拉克",1,"",""],["伊朗","伊朗",1,"",""],["以色列","以色列",1,"",""],["意大利","意大利",1,"",""],["印度","印度",1,"",""],["印度尼西亚","印度尼西亚",1,"",""],["英国","英国",1,"",""],["约旦","约旦",1,"",""],["越南","越南",1,"",""],["赞比亚","赞比亚",1,"",""],["泽西岛","泽西岛",1,"",""],["乍得","乍得",1,"",""],["直布罗陀","直布罗陀",1,"",""],["智利","智利",1,"",""],["中非","中非",1,"",""]],"SelectedValueArray":["-1"]},"p1_ddlSheng":{"F_Items":[["-1","选择省份",1,"",""],["北京","北京",1,"",""],["天津","天津",1,"",""],["上海","上海",1,"",""],["重庆","重庆",1,"",""],["河北","河北",1,"",""],["山西","山西",1,"",""],["辽宁","辽宁",1,"",""],["吉林","吉林",1,"",""],["黑龙江","黑龙江",1,"",""],["江苏","江苏",1,"",""],["浙江","浙江",1,"",""],["安徽","安徽",1,"",""],["福建","福建",1,"",""],["江西","江西",1,"",""],["山东","山东",1,"",""],["河南","河南",1,"",""],["湖北","湖北",1,"",""],["湖南","湖南",1,"",""],["广东","广东",1,"",""],["海南","海南",1,"",""],["四川","四川",1,"",""],["贵州","贵州",1,"",""],["云南","云南",1,"",""],["陕西","陕西",1,"",""],["甘肃","甘肃",1,"",""],["青海","青海",1,"",""],["内蒙古","内蒙古",1,"",""],["广西","广西",1,"",""],["西藏","西藏",1,"",""],["宁夏","宁夏",1,"",""],["新疆","新疆",1,"",""],["香港","香港",1,"",""],["澳门","澳门",1,"",""],["台湾","台湾",1,"",""]],"SelectedValueArray":["%s"]},"p1_ddlShi":{"Enabled":true,"F_Items":%s,"SelectedValueArray":["%s"]},"p1_ddlXian":{"Enabled":true,"F_Items":%s,"SelectedValueArray":["%s"]},"p1_TongZWDLH":{"Required":false,"Hidden":true,"F_Items":[["是","是",1],["否","否",1]],"SelectedValue":null},"p1_XiangXDZ":{"Label":"国内详细地址","Text":"%s"},"p1_QueZHZJC":{"F_Items":[["是","是",1,"",""],["否","否",1,"",""]],"SelectedValueArray":["%s"]},"p1_FanXRQ":{"Hidden":true},"p1_WeiFHYY":{"Hidden":true},"p1_ShangHJZD":{"Hidden":true},"p1_CengFWH":{"Label":"2020年1月10日后是否在湖北逗留过"},"p1_CengFWH_RiQi":{"Hidden":true},"p1_CengFWH_BeiZhu":{"Hidden":true},"p1_JieChu":{"Label":"01月26日至02月09日是否与来自湖北发热人员密切接触"},"p1_JieChu_RiQi":{"Hidden":true},"p1_JieChu_BeiZhu":{"Hidden":true},"p1_TuJWH":{"Label":"01月26日至02月29日是否乘坐公共交通途径湖北"},"p1_TuJWH_RiQi":{"Hidden":true},"p1_TuJWH_BeiZhu":{"Hidden":true},"p1_JiaRen":{"Label":"01月26日至02月29日家人是否有发热等症状"},"p1_JiaRen_BeiZhu":{"Hidden":true},"p1_SuiSM":{"Required":false,"Hidden":true,"F_Items":[["红色","红色",1],["黄色","黄色",1],["绿色","绿色",1]],"SelectedValue":null},"p1_SuiSMSM":{"Hidden":true,"IFrameAttributes":{}},"p1":{"IFrameAttributes":{}}}'


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
        print('登录成功')

    def __get_data(self):
        resp = self.session.get(reportURL)
        doc = PyQuery(resp.text)
        html = doc.html()
        tiwen = 36.5 + random.uniform(0, 0.3)
        tiwen = round(tiwen, 1)
        zxMatch = re.findall(r'f8_state={.*?"SelectedValue":"(.+?)"', html)[0]
        gnMatch = re.findall(r'f14_state={.*?"SelectedValue":"(.+?)"', html)[0]
        shengMatch = re.findall(r'f16_state={.+?"SelectedValueArray":\["(.+?)"]', html)[0]
        shiMatch = re.findall(r'f17_state={.*?"F_Items":(.+?),"SelectedValueArray":\["(.+?)"]', html)[0]
        xianMatch = re.findall(r'f18_state={.*?"F_Items":(.+?),"SelectedValueArray":\["(.+?)"]', html)[0]
        # print(shiMatch)
        xxMatch = re.findall(r'f20_state={.*?"Text":"(.+?)"', html)[0]
        F_State = template % (
        self.date, zxMatch, gnMatch, shengMatch, shiMatch[0], shiMatch[1], xianMatch[0], xianMatch[1], xxMatch, "否")
        return {
            'F_State': base64.b64encode(F_State.encode()),
            '__VIEWSTATE': doc.find('#__VIEWSTATE').attr('value'),
            '__EVENTTARGET': 'p1$ctl00$btnSubmit',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEGENERATOR': doc.find('#__VIEWSTATEGENERATOR').attr('value'),
            'p1$ChengNuo': 'p1_ChengNuo',
            'p1$BaoSRQ': self.date,
            'p1$DangQSTZK': '良好',
            'p1$TiWen': str(tiwen),
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
            "p1$MingTDX": "不到校",
            "p1$MingTJC": "否",
            "p1$BanChe_1$Value": '0',
            "p1$BanChe_1": '不需要乘班车',
            "p1$BanChe_2$Value": '0',
            "p1$BanChe_2": '不需要乘班车',
            'p1$GuoNei': '国内',
            "p1$ddlGuoJia$Value": "-1",
            "p1$ddlGuoJia": "选择国家",
            'p1$ddlSheng$Value': shengMatch,
            'p1$ddlSheng': shengMatch,
            'p1$ddlShi$Value': shiMatch[1],
            'p1$ddlShi': shiMatch[1],
            'p1$ddlXian$Value': xianMatch[1],
            'p1$ddlXian': xianMatch[1],
            'p1$XiangXDZ': xxMatch,
            "p1$FanXRQ": "",
            "p1$WeiFHYY": "",
            "p1$ShangHJZD": "",
            'p1$QueZHZJC$Value': '否',
            'p1$QueZHZJC': '否',
            'p1$DangRGL': '否',  # 是否隔离
            'p1$DaoXQLYGJ': '',  # 旅游国家
            'p1$DaoXQLYCS': '',  # 旅游城市
            'p1$Address2': '中国',
            'p1$SuiSM': '绿色',  # 随申码颜色
            'p1$LvMa14Days': '是',  # 截止今天是否连续14天健康码为绿色
            'p1$GeLDZ': '',
            "p1_SuiSMSM_Collapsed": "false",
            "p1_GeLSM_Collapsed": 'false',
            "p1_SuiSMSM_Collapsed": 'false'
        }

    def run(self):
        report_data = self.__get_data()
        msg_pattern = re.compile(r'F.alert\({message:\'(.*?)\',')

        @retry(tries=10, delay=1, max_delay=64, backoff=2, logger=logging)
        def submit(data):
            resp = self.session.post(reportURL, data=data, timeout=10)
            assert resp.status_code == 200, 'POST %s returns %d with %s' % (reportURL, resp.status_code, resp.text)
            print(resp.status_code)
            msg = msg_pattern.findall(resp.text)[0]
            assert msg == '提交成功', msg
            return msg

        msg = submit(report_data)
        print(datetime.datetime.today())
        print(msg + ': ' + report_data['p1$TiWen'])


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
                        default=(datetime.date.today() + datetime.timedelta(days=1)))
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
