from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)



@app.route('/')
def main():
    return render_template('./main.html')


'''@app.route('/deleteform')
def deleteform():
    return render_template('./delete.html')'''


@app.route('/delete')
def delete():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123321",
        database="mydb"
    )
    with mydb:
        print('started')
        mycursor = mydb.cursor()
        result = request.args
        table = result['table']
        delid = result['id']
        query = 'delete from ' + table + ' where id' + table + ' = %s'
        mycursor.execute(query, (delid,))
        mydb.commit()
        print('deleted')
        return '0'


@app.route('/addform')
def addform():
    return render_template('./add.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123321",
        database="mydb"
    )
    with mydb:
        mycursor = mydb.cursor()
        data = request.values
        table = data['table']
        array = []
        inputs = "("
        temp = data['form'].split('&')
        for i in temp:
            array.append(i.split('=')[1])
        tuple(array)
        print(array)
        for i in range(0, len(array)):
            if array[i] == '':
                array[i] = None
        task = 'insert into '+table
        if table == 'student':
            task += ' (Sname, idFaculty, idDepartment, Year) values '
        elif table == 'lecturer':
            task += ' (LName, idDepartment, Position, WorkLength) values '
        elif table == 'department':
            task += ' (DName, idFaculty, Phone, AmountOfLecturers, Head) values '
        elif table == 'faculty':
            task += ' (FName, StudAmount, FoundationDate, Head ) values '
        elif table == 'marks':
            task += ' (idStudent, idLecturer, Mark, Date, Subject) values '
        else:
            return '0'
        for i in range(0, len(array)):
            inputs += '%s,'
        inputs = inputs[0:len(inputs)-1] + ')'
        task += inputs
        mycursor.execute(task, array)
        mydb.commit()
        print('commited')
        return '0'


@app.route('/change')
def change():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123321",
        database="mydb"
    )
    with mydb:
        mycursor = mydb.cursor()
        data = request.values
        table = data['table']
        query = "update " + table + " set "
        if table == 'student':
            query += ' Sname = %s, idFaculty=%s, idDepartment = %s, Year = %s where idStudent = %s ;'
        elif table == 'lecturer':
            query += ' LName = %s, idDepartment=%s, Position = %s, WorkLength = %s where idLecturer = %s ; '
        elif table == 'department':
            query += ' DName = %s, idFaculty = %s, Phone = %s, AmountOfLecturers=%s, Head = %s where idDepartment = %s ; '
        elif table == 'faculty':
            query += ' FName = %s, StudAmount=%s, FoundationDate = %s, Head = %s where idFaculty = %s ;'
        elif table == 'marks':
            query += ' idStudent = %s, idLecturer = %s, Mark = %s, Date = %s, Subject = %s where ;'
        else:
            return '0'
        print(query)
        'mycursor.execute(query, array)'
        print('changed')
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
