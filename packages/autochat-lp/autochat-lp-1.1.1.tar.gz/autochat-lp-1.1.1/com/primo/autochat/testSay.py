
import os
import configparser
from com.primo.autochat.AutoReply import AutoChat
if __name__ == '__main__':
    t = AutoChat()
    t.start()



# os.chdir("./dist")
#
# cf = configparser.ConfigParser()
#
# # cf.read("test.ini")
# cf.read("config.ini",encoding="utf-8")
# # cf.has_option()
#
# #return all section
# secs = cf.sections()
# if cf.has_option("config","谷歌"):
#     print(cf.options("config"))
