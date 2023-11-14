from flask import *
from flask_mysqldb import MySQL as sql
from wtforms import Form,StringField,TextAreaField,PasswordField,DateField,DateTimeField,DateTimeLocalField,validators,SelectField,SubmitField,SelectMultipleField
from passlib.hash import sha256_crypt as sha256
from functools import wraps
import os

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        
        if "girildi" in session:
            return f(*args,**kwargs)
        else:
            flash(message="Bu sayfayı görüntülemek için giriş yapmanız gerekiyor",category="danger")
            return redirect(url_for("ogrencigiris"))
        
    return decorated_function

app=Flask(__name__,template_folder="templates")
app.secret_key="zbeun"
app.static_folder = 'static'


app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="zbeun"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
zbeun=sql(app)


@app.route("/ogrencinotsistemi",methods=["GET","POST"])
@login_required
def ogrencinotsistemi():
    return render_template("ogrencinotsistemi.html")




class ogrencigirisclass(Form):
    ogrencino=StringField("Öğrenci No: ",validators=[validators.DataRequired("")])
    sifre=PasswordField("Şifre: ",validators=[validators.DataRequired("")])

@app.route("/")
def anasayfa():
    session.clear()
    return render_template("anasayfa.html")

@app.route("/ogrencigiris",methods=["GET","POST"])
def ogrencigiris():
    session.clear()
    form=ogrencigirisclass(request.form)
    if request.method=="POST":
        girilenogrencino=form.ogrencino.data
        uygulayici=zbeun.connection.cursor()
        sec="SELECT * FROM users WHERE ogrencino=%s"
        sonuc=uygulayici.execute(sec,(girilenogrencino,))
        
        if sonuc>0:
            veri=uygulayici.fetchone()
            girilensifre=form.sifre.data
            gerceksifre=veri["sifre"]
            gercekisim=veri["isim"]
            gercekogrno=veri["ogrencino"]
            if girilensifre==gerceksifre:
                flash(message=f"Giriş başarılı",category="info")
                session["girildi"]=True
                session["username"]=gercekisim
                return redirect(url_for("ogrencinotsistemi"))
                
            else:
                flash(message="Girilen bilgiler birbiri ile uyuşmamaktadır",category="danger")
                return render_template("ogrencigiris.html",form=form)
    
        else:
            flash(message="Girilen bilgiler birbiri ile uyuşmamaktadır",category="danger")
            return render_template("ogrencigiris.html",form=form)
    
    return render_template("ogrencigiris.html",form=form)

@app.route("/derskayit")
@login_required
def derskayit():
    return render_template("derskayit.html")

@app.route("/devamsizlik")
@login_required
def devamsizlik():
    return render_template("devamsizlik.html")

@app.route("/notbilgisi")
@login_required
def notbilgisi():
    return render_template("notbilgisi.html")

@app.route("/yazokulu")
@login_required
def yazokulu():
    return render_template("yazokulu.html")

@app.route("/mufredatdurumu")
@login_required
def mufredatdurumu():
    return render_template("mufredatdurumu.html")

@app.route("/donemort")
@login_required
def donemort():
    return render_template("donemort.html")


@app.route("/stajbasvur")
@login_required
def stajbasvur():
    return render_template("staj.html")


@app.route("/sifresifirla",methods=["GET","POST"])
def sifresifirla():
    session.clear()
    if request.method=="POST":
        girilenogrno=request.form["no"]
        girilenkizlik=request.form["kızlıksoyad"]
        girilenbabaadi=request.form["babaadi"]
        girilentcno=request.form["tcno"]
        girilentelno=request.form["telno"]
        if girilenogrno!="" and girilenkizlik!="" and girilenbabaadi!="" and girilentelno!="" and girilentelno!="" and girilentcno!="":
            return redirect(url_for("smsbilgi"))
        else:
            flash(message="Boş alan bırakmayın",category="danger")
            return render_template("passreset.html")
        
    return render_template("passreset.html")

@app.route("/65P74fTYu1YTQS168ACl")
@login_required
def smsbilgi():
    return render_template("smsbasarili.html")

@app.route("/cikis")
def cikis():
    session.clear()
    flash(message="Çıkış Yapıldı",category="info")
    return redirect(url_for("ogrencigiris"))

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)
    