import flask
from flask import request, jsonify, g
import sqlite3

#config
DATABASE = 'data.db'
DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)
# manual config variables
# app.config['APP_CONFIG'] = 'api.cfg'
# app.config['DEBUG'] = True
# app.config['DATABASE'] = 'data.db'

######################
# app.config.from_envvar('APP_CONFIG')
# db_name: data
# table1: posts
#	post_id
#	post_title
# 	post_text
#	post_summary
#	date
#	visibilty
#	username

# table2: votes
# cols: 
# 	post_id
# 	upvotes
#	downvotes
#	awards
######################


# add functions to initialize db, and close db connection and to query from db
def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(app.config['DATABASE'])
		db.row_factory = make_dicts
	return db


def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv


@app.cli.command('init')
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('data.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()
#


@app.route('/', methods=['GET'])
def home():
	return "<h1>Welcome to CSUF Discussions</h1><p>This site is under development</p>"


@app.errorhandler(404)
def page_not_found(error):
	return "<h1>404</h1><p>Resource not found</p>", 404


"""
@app.route('/api/posts/get', methods=['GET'])
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
"""


@app.route('/api/posts/all', methods=['GET'])
def get_posts_all():
	all_posts = query_db(
		'''SELECT * FROM posts;'''
	)
	return jsonify(all_posts), 200


@app.route('/api/posts/create', methods=['POST'])
def create_post():
	params = request.get_json(force=True)
	# enter code to add post to database
	query =f"INSERT INTO posts (id, community, title, description, published, visibility, username, votes_id) VALUES ({2}, {'csuf'}, {params['title']}, {params['description']}, {params['published']}, {1}, {params['username']}, {10002}); INSERT INTO votes(votes_id, upvotes, downvotes) VALUES({10002}, {500}, {20});SELECT * FROM posts;"
	post = query_db(query, (), None)
	# return "<h2>Post already exists</h2>, 409"
	# return "<h2>Post Created Successfully</h2>", 201
	return f"<h3>Post Created</h3>{jsonify(post)}\n", 201


@app.route('/api/posts/delete', methods=['GET'])
def delete_post():
	# enter code to request a delete operation in database, hide visibility of post and refresh home page
	pass


def main():
	app.run()


if __name__ == '__main__':
	main()
