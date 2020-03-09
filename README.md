
# CPSC 449 Web back-end
## Project-1


1) use this code for generating 3 instance of foreman
```
foreman start -m all=3
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
