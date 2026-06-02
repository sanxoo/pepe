## 파이썬 API 와꾸 정리
- 준비
```
$ docker run -d -p 5432:5432 -v postgresql:/var/lib/postgresql -e POSTGRES_PASSWORD=postgres --name ... postgres
$ docker run -d -p 6379:6379 -name ... redis
```
- 개발
```
$ uv init ...
$ cd ...
$ uv add ...
```
```
$ vi ...
$ vi tests/test...
$ pytest
$ ruff check
$ uv run -m ...
$ ruff format
```
```
$ git status
$ git add -A
$ git commit -m ...
$ git remote add origin git@github.com:...
$ git push -u -f origin main
```
- 배포
```
$ npm install -g pm2
$ pm2 install pm2-logrotate
$ pm2 start --name ... python3 -- -m ...
$ tail -f ~/.pm2/logs/...
```
- 수정
```
$ git branch
$ git fetch origin
$ git reset --hard origin/main
$ git checkout -b ...
```
```
$ vi ...
$ vi tests/test...
$ pytest
$ ruff check
$ uv run -m ...
$ ruff format
```
```
$ git status
$ git add -A
$ git commit -m ...
$ git push

$ git branch -d ...
```
