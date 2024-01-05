from flask import Flask, render_template, request, redirect, send_file
from rembg import remove 
import os
import random
from io import BytesIO
import pymysql.cursors
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sendermail import sender, password


app = Flask(__name__)   
  
db = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='lib',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


con = db.cursor()

logged = False
@app.route('/')   
def main():   
    return render_template('login.html')


@app.route('/check_acc', methods=['POST'])
def check_acc():
    global logged
    if request.method == 'POST':
        kullanici_ismi = request.form.get('username')
        kullanici_sifre = request.form.get('password')

        con.execute('SELECT username, password FROM kullanıcı_bilgi')
        kimlikler = con.fetchall()
        db.commit()
        for kimlik in kimlikler:
            isim = kimlik['username']
            sifre = kimlik['password']

        if kullanici_ismi == isim and kullanici_sifre == sifre:
            logged = True
            return redirect('/anasayfa')

        else:
            #! Hata
            return """Sizi yönlendirmekte bir sorun yaşıyoruz.
            1) Geçersiz kimlik bilgileri
            2) Sunucu kapalı"""


@app.route('/anasayfa')
def index():
    global logged
    if logged == True:
        return render_template("anasayfa.html")   
    else:
        #! Hata
        return('Sayfaya girmeden önce giriş yapın. Hesabınız yoksa bir hesap oluşturun')

@app.route('/upload')
def upload():
    global logged
    if logged == True:
        return render_template('yukle.html')
    else:
        #! Hata
        return('Sayfaya girmeden önce giriş yapın. Hesabınız yoksa bir hesap oluşturun')
    
  
@app.route('/basarili', methods=['POST'])
def basarili():
    if request.method == 'POST':
        file = request.files['file']
        input_data = file.read()

        output_data = remove(input_data)
        fname = random.randint(0, 9999999)
        output_path = str(fname)+'.png'


        return send_file(BytesIO(output_data), download_name=output_path)
    
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/create_acc', methods=['POST'])
def create_acc():
    global logged
    global kayıt_id
    if request.method == 'POST':
        kayıt_isim = request.form.get('username')
        kayıt_sifre = request.form.get('password')
        kayıt_posta = request.form.get('email')
        kayıt_id = random.randint(0, 9999999)
        con.execute('SELECT email FROM kullanıcı_bilgi')
        mailler = con.fetchall()
        db.commit()
        for mail in mailler:
            kontrol_mail = mail['email']

        if kayıt_posta in kontrol_mail:
            return 'Bu maille kayıt olunmuş.'
        elif not kayıt_posta in kontrol_mail:
            con.execute('INSERT INTO kullanıcı_bilgi VALUES(%s, %s, %s, %s)', (kayıt_id, kayıt_isim, kayıt_sifre, kayıt_posta))
            db.commit()
            return redirect('/reg_sonuc')
        else:
            #! Hata
            print('Bilinmeyen hata!')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/change_password', methods = ['POST'])
def change_password():
    if request.method == 'POST':
        sifirla_id = request.form.get('ID')
        sifirla_email = request.form.get('femail')

        con.execute('SELECT password FROM kullanıcı_bilgi WHERE id = '+sifirla_id)
        bul_sifre = con.fetchall()
        db.commit()

        for bulunan_sifre in bul_sifre:
            gonder_sifre = bulunan_sifre['password']
        email_address = sender
        app_password = password

        to_email = sifirla_email
        
        subject = 'Şifren'
        body = gonder_sifre

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

@app.route('/reg_sonuc')
def reg_sonuc():
    global kayıt_id
    return render_template('reg_sonuc.html', kayıt_id = kayıt_id)
  
if __name__ == '__main__':  
    app.run(debug=True) 