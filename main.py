import argparse
import datetime
import logging
import re
import sys
import time

from client import Client


def arg_parser():
    def log_level(arg_value, pat=re.compile(r'(debug|info|warning|error|critical)', re.IGNORECASE)):
        if not pat.match(arg_value):
            raise argparse.ArgumentError
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
    client.run()
    exit(client.exitcode)


if __name__ == '__main__':
    main()
