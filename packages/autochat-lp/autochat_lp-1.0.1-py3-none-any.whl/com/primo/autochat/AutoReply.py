# !/usr/bin/env python
#coding=utf8
import itchat
import os
import configparser,logging

LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT,datefmt=DATE_FORMAT)

def get_response(msg):
    cf = configparser.ConfigParser()
    # cf.read("test.ini")
    cf.read("config.ini", encoding="utf-8")
    for opt in cf.options("config"):
        if msg.index(opt) > 0:
            logging.info("find response %s",cf.get("config",opt))
            return cf.get("config",opt)
    return None


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 这里设置一个默认回复
    if msg['ForwardFlag'] :
        logging.info("my word: %s", msg['Text'])
    else:
        logging.info("speak word: %s",msg['Text'])
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply

def start():
    os.chdir("./dist")
    itchat.auto_login(hotReload=True)
    itchat.run()