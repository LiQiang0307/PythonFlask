from flask import Flask, render_template, request
from functools import wraps
from flask import session,redirect,url_for

import utils

app = Flask(__name__)
app.secret_key="liqiang"


def is_login(func):
    """
    判断是否登录
    :param func:
    :return:
    """
    @wraps(func)
    def check_login(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('hello_world'))
    return check_login


# 删除session
@app.route('/delete')
def delete():
    """
    退出登录，删除session
    :return:
    """
    # print(session.get('user_id'))
    session.pop('user_id')
    # print(session.get('user_id'))
    return render_template('login.html')


@app.route('/index')
@is_login
def login():
    """
    @is_login判断是否已经登录
    如果登录，则跳转到主页
    否则跳回到登录页面，不能通过路由直接访问主页
    :return:
    """
    return render_template("index.html")


@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def hello_world():
    """
    进行登录验证，验证账号密码是否正确
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 2.获取请求的参数
        username = request.form.get("username")
        password = request.form.get("password")
        # print(username)
        # 3.判断账号密码是否正确
        #从数据库读取数据

        #mongodb 查询条件
        myquery = {"username": username,"password":password}
        try:
            rs = utils.connect_mongodb(myquery)
            if rs:
                flag = True
            else:
                flag=False
        except:
            flag = False
        if(flag):
            session['user_id'] = username
            return redirect(url_for("login"))
        else:
            return render_template("login.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
