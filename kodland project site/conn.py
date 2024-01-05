import pymysql.cursors
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sendermail import *

  
db = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='lib',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

con = db.cursor()

con.execute('SELECT password FROM kullanıcı_bilgi WHERE id = 1')
a = con.fetchall()
db.commit()

for aa in a:
    oof = aa['password']

print(oof)

email_address = sender
app_password = password

to_email = 'thefirstvaloplayer@gmail.com'
        
subject = 'Şifren'
body = 'kchjgd'

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    # Gmail'e giriş yap
    server.login(email_address, app_password)

    # E-posta oluştur
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # E-postayı gönder
    server.sendmail(email_address, to_email, message.as_string())

