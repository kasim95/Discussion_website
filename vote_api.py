import flask
from flask import request, jsonify, g, current_app
import sqlite3
#config
DATABASE = 'data.db'
DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)

######################
# app.config.from_envvar('APP_CONFIG')
# db_name: data.db

# table1: posts
#	post_id
#	community_id
#	title
# 	description
#	published
#	username
#	vote_id

# table2: votes
# 	vote_id
# 	upvotes
#	downvotes

# table3: community
#	community_id
#	name
######################

def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
			)
		g.db.row_factory = make_dicts
	return g.db



def query_db(query, args=(), one=False, commit=False):
	# one=True means return single record
	# commit = True for post and delete query
	cur = get_db()
	try:
		if commit:
			rv = cur.execute(query, args)
			cur.commit()
		else:
			rv = cur.execute(query, args).fetchall()
	except sqlite3.OperationalError as e:
		print(e)
	close_db()
	if not commit:
		return (rv[0] if rv else None) if one else rv
	else:
		return 200

def transaction_db(query, args):
	cur = get_db()
	if len(query) != len(args):
		raise ValueError('arguments dont match queries')
	try:
		cur.execute('BEGIN')
		for i in range(len(query)):
			cur.execute(query[i], args[i])
		conn.commit()
	except sqlite3.OperationalError as e:
		cur.execute(rollback)
		print(e)

	close_db()
	return 'Transaction Completed'

@app.cli.command('init')
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('data.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.teardown_appcontext
def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


@app.route('/', methods=['GET'])
def home():
	return "<h1>Welcome to CSUF Discussions</h1><p>This site is under development</p>"

@app.errorhandler(404)
def page_not_found(error):
	return "<h1>404</h1><p>Resource not found</p>", 404

@app.route('/api/votes/upvote',methods=['GET'])
def submit_upvote():
    params = request.args
    post_id = params.get('post_id')
    if not post_id:
        return page_not_found(404)
    query1= 'UPDATE votes SET upvotes=upvotes+1 WHERE vote_id=?'
    args1=(post_id)
    query_db(query, args, one=True, commit=True)
    return render_template('submit_vote.html',post_id),200



def main():
	app.run()


if __name__ == '__main__':
	main()
