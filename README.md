## Requirements

Docker compose and Linux/Mac (last one with enabled virtualization), was tested on both.

## How to run

```bash
./example.sh
```

Application will run at http://localhost:8000/

API documentation available at http://localhost:8000/api/schema/swagger-ui

Problem example for POST _/api/solve/_
```json
{
    "coordinates": [
        {"lat":456, "lon": 320},
        {"lat":228, "lon": 0},
        {"lat":912, "lon": 0},
        {"lat":0, "lon": 80},
        {"lat":114, "lon": 80},
        {"lat":570, "lon": 160},
        {"lat":798, "lon": 160},
        {"lat":342, "lon": 240},
        {"lat":684, "lon": 240},
        {"lat":570, "lon": 400},
        {"lat":912, "lon": 400},
        {"lat":114, "lon": 480},
        {"lat":228, "lon": 480},
        {"lat":342, "lon": 560},
        {"lat":684, "lon": 560},
        {"lat":0, "lon": 640},
        {"lat":798, "lon": 640}
    ],
    "num_vehicles": 4,
    "depot": 0,
    "max_distance": 3000
}
```

## Design

This is Django+DRF app, which receives problem parameters, sends them to RabbitMQ, where messages acknowleged by Celery worker(s), which run solver. Solution stored in Redis until request from author (or expiration).

1. My first assumption was that there's no need in longterm storage for problem and solution instances - it seems hardly reusable. Even if there are some patterns in delivery routes, they are distinct enough, so attempts to look for similarities would be an overhead and increased time as the result, so relationship database is used only to keep user data (I was tempted to use SQLite for this).

2. There's 1 queue where problems are published, which is consumed by Celery workers with default prefork execution pool (recommended for tasks CPU-bound task, and VRP problems seems like one that uses CPU a lot).

3. Because calculation result is relatively small and short-living (1.), I've decided to use Redis as it's final destination. Depending on RPS it can set a high toll on memory, but result lifespan is adjustable, + it's possible to switch Celery result backend if needed.


## Notes

Generating autodocs for DRF is still kinda painful and makes me miss Pydantic schemas.
