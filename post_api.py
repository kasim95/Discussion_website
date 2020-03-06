import flask
from flask import request, jsonify, g, current_app
import sqlite3

# todo: add error handling for create post (if post already exists)
# todo: add error handling for delete post (if post does not exist)
# todo: add url to posts table in db

# config variables
DATABASE = 'data.db'
DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)

######################
# app.config.from_envvar('APP_CONFIG')
# db_name: data.db

# table1: posts
# post_id
# community_id
# title
# description
# published
# username
# vote_id

# table2: votes
# vote_id
# upvotes
# downvotes

# table3: community
# community_id
# name
######################


# helper function used to convert each query result row into dictionary
def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


# get db from flask g namespace
def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
			)
		g.db.row_factory = make_dicts
	return g.db


# initiate db with '$flask init'
@app.cli.command('init')
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('data.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


# close db connection
@app.teardown_appcontext
def close_db(e=None):
	if e is not None:
		print(f'Closing db: {e}')
	db = g.pop('db', None)
	if db is not None:
		db.close()

# home page
@app.route('/', methods=['GET'])
def home():
	return "<h1>Welcome to CSUF Discussions</h1>" \
			"<p>This site is under development</p>"


# 404 page
@app.errorhandler(404)
def page_not_found(status_code=404):
	return "<h1>404 in flask</h1><p>Resource not found</p>", status_code


# function to execute a single query at once
def query_db(query, args=(), one=False, commit=False):
	# one=True means return single record
	# commit = True for post and delete query
	conn = get_db()
	try:
		if commit:
			rv = conn.execute(query, args)
			conn.commit()
		else:
			rv = conn.execute(query, args).fetchall()
	except sqlite3.OperationalError as e:
		print(e)
		return page_not_found(404)
	close_db()
	if not commit:
		return (rv[0] if rv else None) if one else rv
	return True


# function to execute multiple queries at once
def transaction_db(query, args):
	conn = get_db()
	if len(query) != len(args):
		raise ValueError('arguments dont match queries')
	try:
		conn.execute('BEGIN')
		for i in range(len(query)):
			conn.execute(query[i], args[i])
		conn.commit()
	except sqlite3.OperationalError as e:
		conn.execute('rollback')
		print('Transaction failed. Rolled back')
		print(e)
		return False
	close_db()
	return True


# function to retrieve all posts without any filters
@app.route('/api/posts/all', methods=['GET'])
def get_posts_all():
	query = 'SELECT * FROM posts'
	all_posts = query_db(query)
	return jsonify(all_posts), 200


# function to retrieve posts with filters
@app.route('/api/posts/filter')
def get_posts_filter():
	return page_not_found(404)


# function to add a new post to db
@app.route('/api/posts/create', methods=['POST'])
def create_post():
	params = request.get_json(force=True)

	query1 = 'INSERT INTO votes (upvotes, downvotes) VALUES (?, ?)'
	args1 = (0, 0)

	query2 = 'INSERT INTO posts (community_id, title, description, username, vote_id) VALUES (?,?,?,?,(SELECT MAX(vote_id) FROM votes))'
	args2 = (2, params['title'], params['description'], params['username'])

	q = transaction_db([query1, query2], [args1, args2])
	if not q:
		return page_not_found(404)
	return "<h1>Post created</h1>", 201


# function to delete an existing post from db
@app.route('/api/posts/delete', methods=['GET'])
def delete_post():
	params = request.args

	post_id = params.get('post_id')
	if not post_id:
		return page_not_found(404)

	query1 = 'DELETE FROM votes WHERE vote_id=(SELECT vote_id FROM posts WHERE post_id=?)'
	args1 = (post_id)

	query2 = 'DELETE FROM posts WHERE post_id=?'
	args2 = (post_id)

	q = transaction_db([query1, query2], [args1, args2])
	if not q:
		return page_not_found(404)
	return "<h1>Post Deleted</h1>", 200


def main():
	app.run()


if __name__ == '__main__':
	main()
