import requests


# Telegram notification
def telegram_send_message(message):
    w = 'https://api.telegram.org/bot5875292982:AAGEHSR1NqmA04OWt_vp2vTIPGUSJ4W9Luw/sendmessage?chat_id=305034927&text='
    #message = 'hellow'

    Dict_data = {"UrlBox" : w+message , 
                "AgentList" : "Mozilla+Firefox" ,
                "VersionsList" : "VersionsList" ,
                "MethodList" : "POST"}

    send = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx" , data=Dict_data)
    if send.status_code == 200:
        print('message send to telegram bot')
    else:
        print('message fail to send')   
