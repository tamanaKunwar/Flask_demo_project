from flask_api import FlaskAPI
from flask import request, Response, json
import psycopg2
from psycopg2._psycopg import IntegrityError


APP = FlaskAPI(__name__)

def database_connection(query):
    hostname = 'localhost'
    database = 'student'
    username = 'postgres'
    pwd = 'Tamana@19'
    port_id = 5432
    conn = None
    cor = None
    try:
        conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        return cur
    except IntegrityError as e:
        response = e.pgerror
        print("@@@@@@@")
        print(response)
        return response

@APP.route('/getStudentDetails/rollno/<rollNo>', methods = ['GET'])
def getStudentDetails(rollNo):
    script = ''' select stu.roll_no, stu.name, stu.father_name, sub.sub_name, sub.sub_teacher from 
    studentdetails as stu inner join subjectdetails as sub on stu.sub_id = sub.sub_id
    where stu.roll_no = ''' + rollNo

    result = database_connection(script)

    my = result.fetchone()
    val = [i for i in my]
    json_val = {
        'rollno' : val[0],
        'name' : val[1],
        "father's name" : val[2],
        'subject name' : val[3],
        'teacher' : val[4]
    }
    json_resp = json.dumps(json_val)
    return Response(json_resp, mimetype='application/json', status=200)

@APP.route('/addStudent', methods=['POST'])
def AddStudent():
    name = request.data['name']
    roll_no = request.data['roll_no']
    father_name = request.data['father_name']
    sub_id = request.data['sub_id']
    script = f" INSERT INTO studentdetails(roll_no, name, father_name, sub_id) VALUES({roll_no},'{name}','{father_name}',{sub_id})"
    result = database_connection(script)
    json_response = json.dumps({"msg" : str(result)})
    return Response(json_response, mimetype='application/json', status=200)

@APP.route('/deleteStudent/rollno/<rollNo>', methods= ['DELETE'])
def DeleteStudent(rollNo):
    roll_no = rollNo
    script = f" DELETE FROM studentdetails WHERE roll_no = {roll_no}"
    result = database_connection(script)
    json_response = json.dumps({"msg": str(result)})
    return Response(json_response, mimetype= 'application/json', status=200)

@APP.route('/updateStudent/rollno/<rollNo>', methods=['PUT'])
def UpdateStudent(rollNo):
    roll_no = rollNo
    name = request.data['name']
    father_name = request.data['father_name']
    sub_id = request.data['sub_id']
    script = f"UPDATE studentdetails SET name='{name}', father_name='{father_name}', sub_id={sub_id} WHERE roll_no={roll_no}"
    result = database_connection(script)
    json_response = json.dumps({"msg":str(result)})
    return Response(json_response, mimetype='application/json', status=200)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)