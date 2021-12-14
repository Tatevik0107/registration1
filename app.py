from flask import Flask, render_template, request, redirect 
import psycopg2 
FP="Error. Please return to the previous page and repeat the try. Surely you mustn`t leave field"
MP="empty. <br/> Ошибка. Пожалуйста вернитесь на предыдущую страницу и повторите попытку. Поле"
LP="не должно быть пустым."
 
app=Flask(__name__) 
@app.route('/',methods=['GET']) 
def ref(): 
    return redirect("/login/") 

 
@app.route('/login/', methods=['GET','POST']) 
def index(): 
    if request.method=='POST': 
        if request.form.get("login"): 
            login = request.form.get('username') 
            password = request.form.get('password') 
            conn = psycopg2.connect(database = "service",user="postgres",password="2002",host="localhost",port="5432") 
            cursor=conn.cursor() 
            cursor.execute("SELECT name FROM users.user WHERE login=%s and password=%s", 
            (str(login), str(password))) 
            records = list(cursor.fetchall()) 
            if len(records)==0:
                error="Error. Please return to the previous page and repeat the try. Login or Password are incorrect. <br/> Ошибка. Пожалуйста вернитесь на предыдущую страницу и повторите попытку. Логин или пароль введены неправильно."
                error.encode('utf-8')
                return (error)
            return render_template('account.html', full_name = records[0][0]) 
        if request.form.get("registration"): 
            return redirect('/registration/') 
    return render_template('login.html') 
@app.route('/registration/', methods=['GET','POST']) 
def registration(): 
    if request.method=='POST': 
        name = request.form.get('name') 
        if name=='':
            error=FP+" 'Your name' "+MP+" 'Your name' "+LP
            error.encode('utf-8')
            return (error)
        login = request.form.get('login') 
        if login=='':
            error=FP+" 'Login' "+MP+" 'Login' "+LP
            error.encode('utf-8')
            return (error)

        password = request.form.get('password') 
        if password=='':
            error=FP+" 'Password' "+MP+" 'Password' "+LP
            error.encode('utf-8')
            return (error)
        conn = psycopg2.connect(database = "service",user="postgres",password="2002",host="localhost",port="5432") 
        cursor=conn.cursor() 
        cursor.execute("INSERT INTO users.user (name,login,password) VALUES (%s ,%s ,%s)", 
        (str(name), str(login), str(password))) 
        conn.commit() 
        return redirect('/login/') 
 
    return render_template('registration.html')

