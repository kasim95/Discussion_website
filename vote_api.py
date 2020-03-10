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


def query_db(query, args=(), one=False, commit=True):
    # one=True means return single record
    # commit = True for post and delete query
    conn = get_db()
    try:
        rv = conn.execute(query, args).fetchall()
        if commit:
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)
        return page_not_found(404)
    close_db()
    if not commit:
        return (rv[0] if rv else None) if one else rv
    return True

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


# function to retrieve all votes without any filters
@app.route('/api/votes/all', methods=['GET'])
def get_posts_all():
    query = 'SELECT * FROM votes'
    all_votes = query_db(query)
    return jsonify(all_votes), 200

# Upvote a post
@app.route('/api/votes/upvotes',methods=['GET'])
def get_upvotes():
	params = request.args
	vote_id = params.get('vote_id')
	query = 'UPDATE votes SET upvotes=upvotes + 1 WHERE vote_id IN (SELECT vote_id FROM posts WHERE post_id = ?)'
	args = (vote_id,)
	update_upvotes = query_db(query,args,one=True)
	return jsonify(update_upvotes),200

#Downvote a post
@app.route('/api/votes/downvotes',methods=['GET'])
def get_downvotes():
	params = request.args
	vote_id = params.get('vote_id')
	query = 'UPDATE votes SET downvotes=downvotes+1 WHERE vote_id IN (SELECT vote_id FROM posts WHERE post_id = ?)'
	args = (vote_id,)
	update_downvotes = query_db(query,args,one=True)
	return jsonify(update_downvotes),200

#Report the number of upvotes and downvotes for a post
@app.route('/api/votes/get',methods=['GET'])
def get_retrievevotes():
	params = request.args
	vote_id = params.get('vote_id')
	query = 'SELECT upvotes,downvotes FROM votes INNER JOIN posts ON posts.vote_id = votes.vote_id WHERE post_id = ?'
	args = (vote_id,)
	update_get = query_db(query,args,one=True)
	return jsonify(update_get),200

#List the n top-scoring posts to any community
@app.route('/api/votes/getTop',methods=['GET'])
def get_topvotes():
	params = request.args
	n = params.get('n')
	query = 'SELECT posts.post_id FROM posts INNER JOIN votes on posts.vote_id = votes.vote_id ORDER BY abs(upvotes-downvotes) DESC LIMIT ?'
	#query = 'SELECT abs(upvotes-downvotes) as Scores FROM votes ORDER BY Scores DESC LIMIT ?'
	#query = 'SELECT * FROM votes WHERE vote_id=?'
	args = (n,)
	update_getTop = query_db(query,args,one=True)
	return jsonify(update_getTop),200

#Given a list of post identifiers, return the list sorted by score.
@app.route('/api/votes/getList',methods=['GET'])
def get_topList():
	params = request.args
	post_ids = params.get('post_ids')
	post_ids = post_ids.split(',')

	post_ids = list(map(int,post_ids))

	t= tuple(post_ids)
	query = 'SELECT votes.vote_id,upvotes,downvotes FROM posts inner join votes on posts.vote_id = votes.vote_id WHERE posts.post_id IN {} ORDER BY (upvotes-downvotes) DESC'.format(t)

	args = (post_ids,)
	update_getList = query_db(query,commit=False)
	return jsonify(update_getList),200


def main():
	app.run()


if __name__ == '__main__':
	main()
