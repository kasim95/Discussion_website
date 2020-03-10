import flask
from flask import request, jsonify, g, current_app
import sqlite3

######################
# Tasks
# todo: add error handling for create post (if post already exists) (What is the criteria to check existing post?)

######################
# Reference: https://alvinalexander.com/android/sqlite-autoincrement-insert-value-primary-key
# Use SELECT last_insert_row_id() in SQL to get last autoincremented value

######################
# config variables
DATABASE = 'data.db'
DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)

######################
# Database
# app.config.from_envvar('APP_CONFIG')
# db_name: data.db

# table1: posts
# post_id
# community_id
# title
# description
# resource_url
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
    return "<h1>Welcome to CSUF Discussions API</h1>" \
           "<p>Use /posts for posts api and /votes for votes api</p>"


def get_response(status_code, message):
    return {"status_code": str(status_code), "message": str(message)}


# 404 page
@app.errorhandler(404)
def page_not_found(status_code=404):
    error_json = get_response(status_code=status_code, message="Resource not found")
    return jsonify(error_json), status_code


# function to execute a single query at once
def query_db(query, args=(), one=False, commit=False):
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


# function to execute multiple queries at once
def transaction_db(query, args, return_=False):
    # return_=True if the transaction has a query that returns a result
    conn = get_db()
    if len(query) != len(args):
        raise ValueError('arguments dont match queries')
    try:
        rv = []
        conn.execute('BEGIN')
        for i in range(len(query)):
            rv.append(conn.execute(query[i], args[i]).fetchall())
        conn.commit()
    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        conn.execute('rollback')
        print('Transaction failed. Rolled back')
        print(e)
        return False
    close_db()
    return True if not return_ else rv


# function to retrieve posts with filters for a number of posts n (default value of n is 100)
@app.route('/api/posts/filter', methods=['GET'])
def get_posts_filter():
    params = request.args
    query = 'SELECT post_id, title, published, username, community_name FROM posts ' \
             'INNER JOIN community ON posts.community_id=community.community_id ' \
             'INNER JOIN votes ON posts.vote_id=votes.vote_id WHERE'
    args = []

    post_id = params.get('post_id')
    filters = 0
    if post_id:
        query += ' post_id=? AND'
        args.append(post_id)
        filters += 1

    username = params.get('username')
    if username:
        query += ' username=? AND'
        args.append(username)
        filters += 1

    published = params.get('published')
    if published:
        query += ' published=? AND'
        args.append(published)
        filters += 1

    title = params.get('title')
    if title:
        query += ' title=? AND'
        args.append(title)
        filters += 1

    community_name = params.get('community_name')
    if community_name:
        query += ' community_name=? AND'
        args.append(community_name)
        filters += 1

    if filters > 0:
        query = query[:-4]
    else:
        query = query[:-6]

    number = params.get('n')
    if not number:
        number = 100
    query += ' ORDER BY published DESC LIMIT ?'
    args.append(number)

    print(query)
    q = query_db(query, tuple(args))

    if q:
        return jsonify(q), 200
    return page_not_found(404)


# function to add a new post to db
@app.route('/api/posts/create', methods=['POST'])
def create_post():
    params = request.get_json()

    query1 = 'INSERT INTO votes (upvotes, downvotes) VALUES (?, ?)'
    args1 = (0, 0)

    query_community = 'SELECT community_id FROM community WHERE community_name=?'
    args_community = (params['community_name'],)
    community_id = query_db(query_community, args_community, one=True, commit=False)
    print(community_id)
    if community_id is not None:
        if type(community_id) != list:
            id_ = community_id['community_id']
        else:
            id_ = community_id[0]['community_id']
        query3 = 'INSERT INTO posts (community_id, title, description, username, vote_id) ' \
                 'VALUES (?,?,?,?,(SELECT MAX(vote_id) FROM votes))'
        args3 = (id_, params['title'], params['description'], params['username'])
        q = transaction_db([query1, query3], [args1, args3])
    else:
        query2 = 'INSERT INTO community (community_name) VALUES (?)'
        args2 = (params['community_name'],)
        query3 = 'INSERT INTO posts (community_id, title, description, username, vote_id) ' \
                 'VALUES ((SELECT community_id FROM community WHERE community_name=?),?,?,?,(SELECT MAX(vote_id) FROM votes))'
        args3 = (params['community_name'], params['title'], params['description'], params['username'])
        q = transaction_db([query1, query2, query3], [args1, args2, args3])
    if not q:
        return page_not_found(404)
    return jsonify(get_response(status_code=201, message="Post created")), 201


# function to delete an existing post from db
@app.route('/api/posts/delete', methods=['GET'])
def delete_post():
    params = request.args

    post_id = params.get('post_id')
    if not post_id:
        return page_not_found(404)

    query1 = 'SELECT * FROM posts WHERE post_id=?'
    args1 = (post_id,)

    if not query_db(query1, args1):
        return jsonify(get_response(status_code=409, message="Post does not exist")), 409

    query2 = 'DELETE FROM votes WHERE vote_id=(SELECT vote_id FROM posts WHERE post_id=?)'
    args2 = (post_id,)

    query3 = 'DELETE FROM posts WHERE post_id=?'
    args3 = (post_id,)

    q = transaction_db([query2, query3], [args2, args3])
    if not q:
        return page_not_found(404)
    return jsonify(get_response(status_code=200, message="Post deleted")), 200


def main():
    app.run()


if __name__ == '__main__':
    main()
