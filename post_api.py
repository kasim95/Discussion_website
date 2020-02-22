import flask
from flask import request, jsonify, g
import sqlite3


app = flask.Flask(__name__)
######################
# app.config.from_envvar('APP_CONFIG')
# db_name: data
# table1: posts
#	post_id
#	post_header
# 	post_desc
#	date
#	visibilty
#	username

# table2: votes
# cols: 
# 	post_id
# 	upvotes
#	downvotes
#	awards

# table3: users
# cols:
#	username
#	password
#	email
#	age
######################

# add functions to initialize db, and close db connection and to query from db
def init_db():
	pass


def close_db():
	pass


def query_db():
	pass
#


@app.route('/', methods=['GET'])
def home():
	return "<h1>Welcome to CSUF Discussions</h1><p>This site is under development</p>"


@app.errorhandler(404)
def page_not_found(error):
	return "<h1>404</h1><p>Resource not found</p>", 404


@app.route('/api/v1/posts/get', methods=['GET'])
def get_posts():
	params = request.args
	n = params.get('n')
	community = params.get('community')
	post_id = params.get('post_id')
	query = "SELECT * FROM data WHERE"
	param_values = []

	# enter code for all params such as query+= 'n=? AND' and param_values.append(n)
	# community = $_all_$ means all communities
	
	#results = query_db(query, param_values)
	#return jsonify(results)
	return "<h1>Under Development</h1>"	


@app.route('/api/v1/posts/create', methods=['POST'])
def create_post():
	params = request.data
	# enter code to add post to database and refresh home page
	
	# return "<h2>Post already exists</h2>, 409"
	# return "<h2>Post Created Successfully</h2>", 201
	pass


@app.route('/api/v1/posts/delete', methods=['GET'])
def delete_post():
	# enter code to request a delete operation in database, hide visibility of post and refresh home page
	pass


def main():
	app.run()


if __name__ == '__main__':
	main()
