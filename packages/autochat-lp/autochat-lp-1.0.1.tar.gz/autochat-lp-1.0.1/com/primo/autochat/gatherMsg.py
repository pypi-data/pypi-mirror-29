import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    # msg['User']
    print(msg['Text'])

itchat.auto_login()
itchat.run()