
# CPSC 449 Web Backend Engineering
## Project-1
### Project Members:
* Raj Chhatbar (chhatbarraj@csu.fullerton.edu) | Role: Ops
* Mohammed Kasim Panjri (kasimp@csu.fullerton.edu) | Role: Dev 1 Posts API
* Harlik Shah (shahharlik@csu.fullerton.edu) | Role: Dev 2 Votes API

1) use this code for generating 3 instance of foreman
```
foreman start -m post=3,vote=3
```

2) in separate terminal run
```
ulimit -n 8192 && caddy
```

3) Then go to localhost:2015/posts or localhost:2015/votes
ex: to get all post in Database run
http://localhost:2015/posts/api/posts/all


## License
[MIT](https://choosealicense.com/licenses/mit/)
