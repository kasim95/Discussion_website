
# CPSC 449 Web Backend Engineering
## Project-1
### Project Members:
* Raj Chhatbar (chhatbarraj@csu.fullerton.edu) | Role: Ops
* Mohammed Kasim Panjri (kasimp@csu.fullerton.edu) | Role: Dev 1 Posts API
* Harlik Shah (shahharlik@csu.fullerton.edu) | Role: Dev 2 Votes API


#### ---------------------------------- Dev Ops-------------------------------------------
1) Use this code for generating 3 instance of foreman in a terminal
```
foreman start -m post=3,vote=3
```

2) In separate terminal run
```
ulimit -n 8192 && caddy
```

3) Then go to localhost:2015/posts or localhost:2015/votes
ex: to get all post in Database run
http://localhost:2015/posts/filter

#### ---------------------------------- Post API-------------------------------------------

#### ---------------------------------- Vote API-------------------------------------------


--------------------
Upvote a post:
Example request:
curl -i -X POST -H "Content-Type: application/json" -d '{"vote_id":"2"}' 'http://127.0.0.1:5000/upvotes'

--------------------
Downvote a post:
Example request:
curl -i -X POST -H "Content-Type: application/json" -d '{"vote_id":"2"}' 'http://127.0.0.1:5000/downvotes'
--------------------
Report the number of upvotes and downvotes for a post:
Example request:
curl -i 'http://localhost:2015/votes/get?vote_id=2';
--------------------
List the n top-scoring posts to any community:
Example request:
curl -i 'http://localhost:2015/votes/getTop?n=3';
--------------------
Given a list of post identifiers, return the list sorted by score.:
Example request:
curl -i -X POST -H "Content-Type: application/json" -d '{"post_ids":["1","3"]}' 'http://127.0.0.1:5000/getList'
#### ---------------------------------- Vote API-------------------------------------------

## License
[MIT](https://choosealicense.com/licenses/mit/)

