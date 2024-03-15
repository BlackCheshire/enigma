# Enigma Service

_Enigma_ service provides `/api/encrypt` endpoint, which transforms input data
in a deterministic way with secret key known only by the service & its keepers

The service has a basic Redis-based caching system that returns encryption
results of previous requests for the same input data and secret key

## Run Example

1. Clone config example:

   ```
   cp .env.example .env
   ```

2. Run Redis container:

   ```
   docker run -it \
     -v ./redis.conf.example:/usr/local/etc/redis/redis.conf:ro \
     -p 6379:6379 \
     redis:7 \
     redis-server /usr/local/etc/redis/redis.conf
   ```

3. Run Enigma app:

   ```
   pipenv run python -m enigma
   ```

4. Make test request:

   ```
   curl -X POST \
     http://localhost:13337/api/encrypt \
     -H 'Content-Type: application/json' \
     -d '{"data": "SGVsbG8sIEVuaWdtYSE="}'
   ```

   _Alternatively, visit `http://localhost:13337/docs` in browser_
