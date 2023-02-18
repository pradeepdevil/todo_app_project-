import pymysql
from flask import Flask, render_template
from flask import request, redirect


app=Flask(__name__)

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        # password="root123",
        db='shwetha',
    )

    # query = """CREATE TABLE employee (
    #                 id INT AUTO_INCREMENT primary key NOT NULL,
    #                 name  VARCHAR(20) NOT NULL,
    #                 salary VARCHAR(50)
    #            )"""
    # cur = conn.cursor()
    # cur.execute(query)

    return conn

@app.route("/")
def main():
    employees = []
    conn = mysqlconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee;")
    for row in cursor.fetchall():
        employees.append({"id": row[0], "name": row[1], "salary": row[2]})
    conn.close()
    return render_template("emp_list.html", employees=employees)

@app.route("/add-employee",methods=['GET','POST'])
def add_emp():
    if request.method=='GET':
        return render_template("add_emp.html", employee={})
    if request.method== 'POST':
        name=request.form["name"]
        salary=request.form["salary"]
        conn=mysqlconnect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO employee (name,salary) VALUES (%s,%s)",(name,salary))
        conn.commit()
        conn.close()
        return redirect('/')

@app.route("/update-employee/<int:id>", methods=['GET', 'POST'])
def update_employee(id):
    emp = []
    conn = mysqlconnect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employee WHERE id = %s", (id))
        row = cursor.fetchall()
        emp = {"id": row[0], "name": row[1], "salary": row[2]}
        return render_template("add_emp.html", employee=emp)
        return redirect('/')

    if request.method == 'POST':
        name = request.form["name"]
        salary = request.form["salary"]
        cursor.execute("UPDATE employee SET name = %s, salary = %s, WHERE id = %s", (name, salary, id))
        conn.commit()
        return redirect('/')

    conn.close()

@app.route('/delete-employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    conn = mysqlconnect()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employee WHERE id = %s", (id))
        row = cursor.fetchone()
        emp = {"id": row[0], "name": row[1], "salary": row[2]}
        return render_template("delete_emp_form.html", employee=emp)

    if request.method == 'POST':
        cursor.execute("DELETE FROM employee WHERE id = %s", (id))
        conn.commit()
        return redirect('/')

    conn.close()


if __name__ == '__main__':
    app.run()
