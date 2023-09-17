from services import app
#
# import requests
# from flask import Flask, render_template, request, redirect
# import psycopg2
#
# app = Flask(__name__)
#
# conn = psycopg2.connect(database="carParser",
#                         user="postgres",
#                         password="plombier520796",
#                         host="localhost",
#                         port="5432")
#
# cursor = conn.cursor()
#
#
# @app.route('/', methods=['POST', 'GET'])
# def main():
#     if request.method == 'POST':
#         if request.form.get("login"):
#             return redirect("/login")
#
#     return render_template('main.html')
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         if request.form.get("login"):
#             login = request.form.get('login')
#             password = request.form.get('password')
#             if login == "" or password == "":
#                 return render_template("login.html", empty_credentials=True)
#             else:
#                 cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(login),
#                                                                                       str(password)))
#                 records = list(cursor.fetchall())
#                 if len(records) == 0:
#                     return render_template("login.html", not_registered=True)
#                 else:
#                     return render_template('account.html', full_name=records[0][1], login=records[0][2],
#                                            password=records[0][3])
#         elif request.form.get("registration"):
#             return redirect("/registration")
#     return render_template('login.html')
#
#
# @app.route('/registration/', methods=['POST', 'GET'])
# def registration():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         login = request.form.get('login')
#         password = request.form.get('password')
#         if name == "":
#             return render_template('registration.html', name_null=True)
#         elif login == "":
#             return render_template('registration.html', login_null=True)
#         elif password == "":
#             return render_template('registration.html', password_null=True)
#         else:
#             cursor.execute("SELECT login FROM users WHERE login = '{0}';".format(str(login)))
#             log = list(cursor.fetchall())
#             if len(log) != 0:
#                 return render_template('registration.html', login_exists=True)
#             else:
#                 cursor.execute("SELECT password FROM users WHERE password = '{0}';".format(str(password)))
#                 passw = list(cursor.fetchall())
#                 if len(passw) != 0:
#                     return render_template('registration.html', password_exists=True)
#                 else:
#                     username = str(name)
#                     symbols = any(char in "1234567890<>\|№@=[]{}~.,:;!_*-+()/#¤%&)" for char in username)
#                     if symbols:
#                         return render_template('registration.html', symbolsError=True)
#                     else:
#                         cursor.execute('INSERT INTO users (name, login, password) VALUES (%s, %s, %s);',
#                                        (str(name), str(login), str(password)))
#                         conn.commit()
#                         return redirect('/login/')
#     return render_template('registration.html')
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
