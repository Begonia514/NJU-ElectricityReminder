import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import traceback

#查询网站网址，仙林与鼓楼不同
url='http://114.212.254.14:8899/query/Default.aspx'
#发送邮箱，我的小号
mailSender = '3143180454@qq.com'
#授权码，此次我做了隐藏
authcode = 'ilovebegonia'
#接收邮箱
mailAccepter = '2239849100@qq.com'
#设置警告电量
warningNum = 30


def mail(message):
    try:
        msg = MIMEText(message, 'plain', 'utf-8')
        #发信源
        msg['From'] = formataddr(["bego", mailSender])
        #收信者
        msg['To'] = formataddr(["贝果", mailAccepter])
        #主题
        msg['Subject'] = "快没电辣"
        #调用IMAP/SMTP服务
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(mailSender, authcode)
        #发送
        server.sendmail(mailSender, [mailAccepter, ], msg.as_string())

        server.quit()  # 关闭连接
    except Exception as e:
        print("邮件发送出现异常！")
        traceback.print_exc()
        return False
    return True



def getNumAndDate():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Ext-Net': 'delta=true',
        'X-Requested-With': 'XMLHttpRequest',
    }
    #这里我就随便找个11舍为例了（为了防止自己房间号被暴露）
    data = {
        'submitDirectEventConfig': '{"config":{"extraParams":{"rid":"1082"}}}',
        'hid_bui_name': '11舍',
        'hid_floor_id': '001',
        'hid_floor_name': '第1层',
        'hid_r_id': '1082',
        'hid_room_name': '101房间',
        '__EVENTTARGET': 'ctl04',
        '__EVENTARGUMENT': '-|public|RoomQuery'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Ext-Net': 'delta=true',
        'X-Requested-With': 'XMLHttpRequest',
    }
    #这里我就随便找个例子了（为了防止自己房间号被暴露）
    data = {
        'submitDirectEventConfig': '{"config":{"extraParams":{"rid":"201"}}}',
        'hid_bui_name': '02舍',
        'hid_floor_id': '001',
        'hid_floor_name': '第1层',
        'hid_r_id': '201',
        'hid_room_name': '104房间',
        '__EVENTTARGET': 'ctl04',
        '__EVENTARGUMENT': '-|public|RoomQuery'
    }


    response = requests.post(url=url,data=data,headers=headers)
    # print(response.text)

    #为了转json，把原本result两边加上双引号
    response_text = response.text.replace('result','"result"')

    respdata = json.loads(response_text)
    respdata = json.loads(respdata['result'])

    remainValue = respdata['remain']
    updateTime = respdata['dttm']


    # print(remainValue,updateTime)
    return remainValue,updateTime
# print(getNumAndDate())

if __name__ == "__main__":
    #运行脚本用于检测与发邮件，定时系统准备交给crontab，每天12:30和22:30准备定时任务（这个时间舍友都在宿舍也方便让他们一起充电费）
    remain, time = getNumAndDate()
    #追加方式打开
    with open('./electricityNumRecord.txt','a') as f:
        f.write(str(time)+' '+str(remain)+'kwh\n')
        f.close()

    if remain <= warningNum:
        message = f"电费不足！还剩余{remain}kwh"

        ret = mail(message)
        if ret:
            print("邮件发送成功")
        else:
            print("邮件发送失败")

    print("执行完毕")


