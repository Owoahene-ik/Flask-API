from flask import request, url_for, jsonify, logging , Response
from flask_api import FlaskAPI, status, exceptions
import psycopg2
import psycopg2.extras
from flask_restful import Resource, Api, reqparse
import json



app = FlaskAPI(__name__)

try:
	conn = psycopg2.connect(database="Flask", user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
	#logging.info("Connected to PostgreSQL database!")
except:
	#logging.exception("Failed to get database connection!")
	print("Cannot connect to database")
	
parser = reqparse.RequestParser()

@app.route('/student', methods=['GET','POST'])
def student():
	if request.method == 'GET':
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		fetch_all_as_dict = lambda cursor: [dict(row) for row in cursor]
		
		# declare lambda function

		cur.execute("SELECT * FROM STUDENT")
		
		
		results = fetch_all_as_dict(cur)
		
		#return jsonify(results)
		
		if len(results) > 0:
			return jsonify({"responseCode":  "00", "message": "Students fetched successfully", "data": results}), 200
			
			
			
		else:
			return jsonify({"responseCode":  "00", "message": "No data found", "data": None}), 404
		
		#conn.close()
		cur.close()
			
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
		
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		fetch_all_as_dict = lambda cursor: [dict(row) for row in cursor]
		
		# declare lambda function

		cur.execute("SELECT * FROM STUDENT")
		
		
		results = fetch_all_as_dict(cur)
		
		#return jsonify(results)
		
		if len(results) > 0:
			return jsonify({"responseCode":  "00", "message": "Students fetched successfully", "data": results}), 201
			
		cur.close()	
			
		
		
		
		
@app.route("/students/<email>", methods = ['GET','PUT','DELETE'])
def user(email):
	if request.method=='GET':
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		fetch_all_as_dict = lambda cursor: [dict(row) for row in cursor]

		temp = ("SELECT * FROM STUDENT where email = %s")
		cur.execute(temp,(email,))
		
		#res = cur.fetchone()
											
		if cur is not None:
			return jsonify(fetch_all_as_dict(cur)), 200
		else:		
			return('No username found'), 404
			
			
	if request.method== 'PUT':
		print(email)
		cur = conn.cursor()
		thun = ("SELECT email FROM STUDENT where email = %s")
		cur.execute(thun,(email,))
		tes = cur.fetchone()
		print(tes[0])
		if tes[0] == email:
			print(request)
			up_first = request.form.get('fname')
			up_age = request.form.get('aged')
			up_email = request.form.get('countr')
		
			guess = ("update student set first_name = %s,age = %s, country = %s where email =%s ")
			cur.execute(guess, (up_first,up_age,up_email,(email,)))
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
		
		delt = ("delete from student where email = %s")
		cur.execute(delt,(email,))
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