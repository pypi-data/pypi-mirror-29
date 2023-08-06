# 项目：标准程序库
# 模块：发送电子邮件
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-10-26 10:25

from email.mime.text import MIMEText
from email.message import Message
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from orange import *
import smtplib
import io
import base64

def sendmail(*messages):
    '''发送邮件'''
    with MailClient() as client:
        for message in messages:
            message.post(client)

def tsendmail(*args):
    '''采用线程发送邮件'''
    from threading import Thread
    Thread(target=sendmail,args=args).start()

class MailClient(smtplib.SMTP):
    '''构造邮件客户端，使用方法如下：
       client=MailClient(host,user,passwd)
    '''
    config={}   # 用于配置发送邮件的想着参数，如：host,user,passwd
    def __init__(self,host=None,user=None,passwd=None,*args,**kw):
        host=host or self.config.get('host')
        user=user or self.config.get('user')
        passwd=passwd or self.config.get('passwd')
        super().__init__(host,*args,**kw)
        self.login(user,passwd)

    def Mail(self,*args,**kw):
        m=Mail(*args,client=self,**kw)
        if m.sender is None:
            m.sender=self.config.get('sender')
        return m

class Mail:
    '''创建电子邮件，使用方法如下：
    mail=Mail(sender,to,subject,body,cc,bcc)
    添加图片：
    mail.add_image(filename,cid)
    添加文件附件：
    mail.add_file(filename)
    通过流附加文件：
    mail.add_fp(fp,filename)
    发送邮件：
    mail.post(client)
    '''
    def __init__(self,sender=None,to=None,subject=None,body=None,
                 cc=None,bcc=None,client=None):
        '''初绍化邮件'''
        self.attachments=[]
        self.subject=subject
        self.to=to
        self.sender=sender
        self.body=body
        self.cc=cc
        self.bcc=bcc
        self.client=client

    @property
    def message(self):
        '''获取邮件的MESSAGE属性'''
        body=MIMEText(self.body,'html','utf-8')
        if self.attachments:
            msg=MIMEMultipart()
            msg.attach(body)
            for attachment in self.attachments:
                msg.attach(attachment)
        else:
            msg=body
        msg['Subject']=self.subject
        msg['To']=self.to
        msg['Sender']=self.sender
        if self.cc:
            msg['Cc']=self.cc
        if self.bcc:
            msg['Bcc']=self.bcc
        return msg
        
    def __str__(self):
        return self.message.as_string()

    def add_file(self,filename):
        fn=Path(filename)
        ensure(fn.is_file(),'文件不存在！')
        self.add_fp(fn.open('rb'),fn.name)

    def add_fp(self,fp,filename,encoding='utf8'):
        filename='=?utf-8?b?%s?='%(base64.b64encode(
            filename.encode('UTF-8')).decode('utf-8'))
        if callable(fp):
            with io.BytesIO() as _fp:
                fp(_fp)
            fp=_fp
        fp.seek(0)
        a=MIMEText(fp.read(),'base64',encoding)
        a['Content-Type']='application/octet-stream'
        a['Content-Disposition']='attachment; filename= %s'%(filename)
        self.attachments.append(a)

    def add_image(self,filename,cid=None):
        with open(filename,'rb')as fn:
            msg=MIMEImage(fn.read())
            if cid:
                kw['Content-ID']=cid
            self.attachments.append(msg)

    def post(self,mailclient=None):
        mailclient=mailclient or self.client
        if mailclient:
            mailclient.send_message(self.message)

if __name__=='__main__':
    body='''
<h2>This is a test</h2>
我们是一群来自北方的儿儿狼。
'''
    msg=Mail('huangtao@czbank.com','huangtao@czbank.com','这是一封邮件',body)
    msg.add_file('~/abc.xlsx')

    from io import *
    with StringIO() as txt:
        txt.write('我们要去哪里？\n')
        txt.write('他们要干啥?\n')
        msg.add_fp(txt,'abc.txt')
    from orange.xlsx import *
    with BytesIO() as fn:
        with Book(fn) as book:
            book.worksheet='Sheet1'
            book.A1_D1='This is a title','title'
            book.A2=['姓名','年龄'],'h2'
        msg.add_fp(fn,'vacation.xlsx') 
    tsendmail('zhmail.czbank.com','huangtao','zxcv9169',msg)
    print('ok')
    
    
