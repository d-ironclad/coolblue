## Requirements

Docker compose and Linux/Mac (last one with enabled virtualization), was tested on both.

## How to run

```bash
./example.sh
```

Application will run at http://localhost:8000/

API documentation available at http://localhost:8000/api/schema/swagger-ui

## Design

This is Django+DRF app, which receives problem parameters, sends them to RabbitMQ, where messages acknowleged by Celery worker(s), which run solver. Solution stored in Redis until request from author (or expiration).

1. My first assumption was that there's no need in longterm storage for problem and solution instances - it seems hardly reusable. Even if there are some patterns in delivery routes, they are distinct enough, so attempts to look for similarities would be an overhead and increased time as the result, so relationship database is used only to keep user data (I was tempted to use SQLite for this).

2. There's 1 queue where problems are published, which is consumed by Celery workers with default prefork execution pool (recommended for tasks CPU-bound task, and VRP problems seems like one that uses CPU a lot).

3. Because calculation result is relatively small and short-living (1.), I've decided to use Redis as it's final destination. Depending on RPS it can set a high toll on memory, but result lifespan is adjustable, + it's possible to switch Celery result backend if needed.
