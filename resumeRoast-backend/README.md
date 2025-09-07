Learning - `uv sync`
While being in development make sure to run `development.sh`
Remove it in production

Make sure while while running the worker we have to run this command

```bash
rq worker --with-scheduler
```

We also need to add the url of redis
Run this on backend terminal of docker - Backend container - **Make sure to do this**

```bash
rq worker --with-scheduler --url redis://valkey:6379
```

https://python-rq.org/#the-worker
