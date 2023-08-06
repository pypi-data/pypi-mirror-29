#coding=utf8
import requests
KEY = '088473409e6c4a0988417e4d1bbaa63a'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'ImitationG'
    }
    try:
        r = requests.post(apiUrl, data=data)
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        raise

print(get_response("你好"))