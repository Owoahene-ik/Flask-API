from flask import request, url_for, jsonify, logging 
from flask_api import FlaskAPI, status, exceptions
import psycopg2
from flask_restful import Resource, Api, reqparse



app = FlaskAPI(__name__)

try:
	conn = psycopg2.connect(database="Flask", user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
	#logging.info("Connected to PostgreSQL database!")
except:
	#logging.exception("Failed to get database connection!")
	print("Cannot connect to database")
	
#parser = reqparse.RequestParser()

@app.route('/student', methods=['GET','POST'])
def student():
	if request.method == 'GET':
		cur = conn.cursor()

		stud = ("SELECT * FROM STUDENT")
		cur.execute(stud)
		
		results = cur.fetchall();
		
		if len(results) > 0:
			return jsonify(results)
			
			conn.commit()
			#conn.close()
			cur.close()
			
		else:
			return('No data found')
			
	if request.method == 'POST':
		cur = conn.cursor()

		NUM = ("SELECT MAX(STUDENT_ID) FROM STUDENT")
		cur.execute(NUM)
		
		take = cur.fetchone()
		
		
		
		add_first = request.form.get('first')
		add_second = request.form.get('last')
		add_age = request.form.get('age')
		add_country= request.form.get('country')
		add_email = request.form.get('email')
		
		
		
		
		varg = "INSERT INTO STUDENT (first_name,last_name, age, country, email) VALUES (%s, %s, %s, %s,%s)"
		
		cur.execute(varg, (add_first,add_second, add_age, add_country, add_email))
		conn.commit()
		
		fin = ("SELECT * FROM STUDENT")
		cur.execute(fin)
		
		ans = cur.fetchall();
		
		conn.commit()
		#conn.close()
		cur.close()
		
		return jsonify(ans), 201
		
		
		
@app.route("/students/<email>", methods = ['GET','PUT','DELETE'])
def user(email):
	if request.method=='GET':
		cur = conn.cursor()

		temp = ("SELECT * FROM STUDENT where email = %s", (email),)
		cur.execute(temp,)
		
		res = cur.fetchone()
							
		if res is not None:
			return jsonify(res), 201
		else:		
			return('No username found')
			
	if request.method== 'PUT':
		cur = conn.cursor()
		thun = ("SELECT * FROM STUDENT where email = %s")
		cur.execute(thun,(email))
		tes = cur.fetchone()
		if tes == email:
			up_first = request.form('fname')
			up_age = request.form('aged')
			up_email = request.form('country')
		
			guess = ("update student set first_name = %s,age = %s, country = %s where email =%s ",(email))
			cur.execute(guess, (up_first,up_age,up_email))
			conn.commit()
			
			
			tee = ("SELECT * FROM STUDENT")
			cur.execute(tee)
		
			dee = cur.fetchall();
		
			conn.commit()
			#conn.close()
			cur.close()
		
			return jsonify(dee), 201
		else:
			return('User does not not exist so cannot update')
	if request.method == 'DELETE':
		cur = conn.cursor()
		
		delt = ("delete fro student where email = %s")
		cur.execute(delt,(email))
		conn.commit()
		
		lee = ("SELECT * FROM STUDENT")
		cur.execute(lee)
		
		IKJ = cur.fetchall();
		
		conn.commit()
		#conn.close()
		cur.close()
		return jsonify(IKJ), 201
		
				
					
			
	
	











if __name__ == "__main__":
	
    app.run(debug=True)