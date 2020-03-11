
curl 'http://127.0.0.1:5000/all';
# [
#   {
#     "downvotes": 24,
#     "upvotes": 111,
#     "vote_id": 1
#   },
#   {
#     "downvotes": 25,
#     "upvotes": 113,
#     "vote_id": 2
#   },
#   {
#     "downvotes": 22,
#     "upvotes": 100,
#     "vote_id": 3
#   },
#   {
#     "downvotes": 2,
#     "upvotes": 1,
#     "vote_id": 5
#   }
# ]
#

#Question 1
#curl 'http://127.0.0.1:5000/upvotes?vote_id=2';
# curl 'http://127.0.0.1:5000/all';
# [
#   {
#     "downvotes": 24,
#     "upvotes": 111,
#     "vote_id": 1
#   },
#   {
#     "downvotes": 25,
#     "upvotes": 114,
#     "vote_id": 2
#   },
#   {
#     "downvotes": 22,
#     "upvotes": 100,
#     "vote_id": 3
#   },
#   {
#     "downvotes": 2,
#     "upvotes": 1,
#     "vote_id": 5
#   }
# ]

#Question 2
#curl 'http://127.0.0.1:5000/downvotes?vote_id=1';
# curl 'http://127.0.0.1:5000/all';
# [
#   {
#     "downvotes": 25,
#     "upvotes": 111,
#     "vote_id": 1
#   },
#   {
#     "downvotes": 25,
#     "upvotes": 114,
#     "vote_id": 2
#   },
#   {
#     "downvotes": 22,
#     "upvotes": 100,
#     "vote_id": 3
#   },
#   {
#     "downvotes": 2,
#     "upvotes": 1,
#     "vote_id": 5
#   }
# ]

#Question 3
#curl -i 'http://127.0.0.1:5000/get?vote_id=2';
#
# [
#   {
#     "downvotes": 25,
#     "upvotes": 114
#   }
# ]
#

#Question 4
# curl 'http://127.0.0.1:5000/getTop?n=3';
# [
#   {
#     "post_id": 2
#   },
#   {
#     "post_id": 1
#   },
#   {
#     "post_id": 3
#   }
# ]

#Question 5
# curl 'http://127.0.0.1:5000/getList?post_ids=1,2,3';
# [
#   {
#     "downvotes": 25,
#     "upvotes": 114,
#     "vote_id": 2
#   },
#   {
#     "downvotes": 25,
#     "upvotes": 111,
#     "vote_id": 1
#   },
#   {
#     "downvotes": 22,
#     "upvotes": 100,
#     "vote_id": 3
#   }
# ]


#/api/votes/getTop
echo 'test finished';
