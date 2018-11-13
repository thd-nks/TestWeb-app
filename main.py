from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('./main.html')


@app.route('/deleteform')
def deleteform():
    return render_template('./delete.html')


@app.route('/delete')
def delete():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123321",
        database="mydb"
    )
    with mydb:
        mycursor = mydb.cursor()
        result = request.args
        table = result['table']
        delid = result['id']
        query = 'delete from ' + table + ' where id' + table + ' = %s'
        mycursor.execute(query, (delid,))
        mydb.commit()
        return '0'


@app.route('/addform')
def addform():
    return render_template('./add.html')


@app.route('/add')
def add():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123321",
        database="mydb"
    )
    with mydb:
        mycursor = mydb.cursor()
        result = request.args
        table = result['table']
        array = []
        amount = "("
        temp = result['form'].split('&')
        for i in temp:
            array.append(i.split('=')[1])
        tuple(array)
        task = 'insert into '+table
        if table == 'student':
            task += ' (Sname, idFaculty, idDepartment, Year) values '
        for i in range(0, len(array)):
            amount += '%s,'
        amount = amount[0:len(amount)-1] + ')'
        task += amount
        mycursor.execute(task, array)
        mydb.commit()
        print('commited')
        return '0'


@app.route('/data')
def data():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123321",
        database="mydb"
    )
    with mydb:
        mycursor = mydb.cursor()
        t = request.args.get('table')
        mycursor.execute('SELECT * from %s' % t)
        arr = mycursor.fetchall()
        column_names = [desc[0] for desc in mycursor.description]
        return jsonify(columns=column_names, result=arr)


if __name__ == '__main__':
    Flask.run(app, debug=True)
