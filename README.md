Discussion_website

# 3 instance of foreman
foreman start -m all=3

root {%SITE_ROOT%}

localhost/posts{
  proxy /api/posts http://127.0.0.1:5000
}
localhost/votes{
  proxy / http://127.0.0.1:5100
}


localhost:{$PORT}
root {%SITE_ROOT%}
proxy /posts http://127.0.0.1:5000
proxy /votes http://127.0.0.1:5100
