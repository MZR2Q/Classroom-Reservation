from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
from datetime import datetime as dt
import html
import random
from sender import sender
app = Flask(__name__)
app.secret_key = '444444444444444444444'


@app.route('/room/<id>', methods=['GET', 'POST'])
def available_hours(id):

    room_number = id
    conn = sqlite3.connect('ClassRoomDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Classes WHERE Room=?', (room_number,))
    available_hours = cursor.fetchall()
    free = ''
    if available_hours == []:
        print('free')
        free = 'free'
    return render_template('SearchForTimeAv.html', frees=free, available_hours=available_hours, room=room_number)


@app.route('/rese', methods=['GET', 'POST'])
def resm():
    if request.method == 'POST':
        room__ = html.escape(request.form.get('room_number'))
        day___ = html.escape(request.form.get('day'))
        strt__ = html.escape(request.form.get('start_time'))
        endt__ = html.escape(request.form.get('end_time'))
        emai__ = html.escape(request.form.get('Email').lower())
        name__ = html.escape(request.form.get('Name'))
        vcode  = random.randint(10000000000000, 90000000000000)
        vaf    = f'''
        Confirm your reservation by clicking on the link below <br> <br> <br>
        http://10.170.13.111:80/aceptcheck/{html.escape(str(vcode))}
'''


        print(room__,day___,strt__,endt__,emai__,name__,vcode)
        conn = sqlite3.connect('ClassRoomDB.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Classes (Room, Day, StartTime, EndTime, resemail, resname, rescode, isre) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (room__, day___, strt__, endt__, emai__, name__, str(vcode), 'y'))
        conn.commit()
        conn.close()
        sender(emai__,str(vaf))



        return redirect('/checkemail')



@app.route('/aceptcheck/<v>', methods=['GET', 'POST'])
def vch(v):
    conn = sqlite3.connect('ClassRoomDB.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Classes SET vcodedone = ? WHERE rescode = ?", ('y', html.escape(v)))
    conn.commit()
    
    cursor.execute('SELECT * FROM Classes WHERE rescode = ?', (html.escape(v),))

    resd = cursor.fetchall()
    resd = resd[0]
    mas = f'''
        {resd[5]} <br>
        {resd[6]} - {resd[7]} <br>
        Reservation Number : {resd[17]} <br>
    '''
    sender(resd[16],str(mas))
    conn.close()
    return redirect('/done')

@app.route('/dashman', methods=['GET', 'POST'])
def admindash():

    conn = sqlite3.connect('ClassRoomDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Classes WHERE isre="y"')
    allres = cursor.fetchall()
    print(allres)

    return render_template('dashres.html',allres=allres)

@app.route('/done', methods=['GET', 'POST'])
def done():
    return render_template('done.html')


@app.route('/checkemail', methods=['GET', 'POST'])
def checkemail():
    return render_template('checkemail.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)