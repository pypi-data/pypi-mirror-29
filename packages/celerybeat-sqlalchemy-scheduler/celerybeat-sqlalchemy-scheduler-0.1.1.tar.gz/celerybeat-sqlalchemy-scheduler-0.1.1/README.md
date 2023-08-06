# celerybeat-sqlalchemy-scheduler

[![PyPI](https://img.shields.io/pypi/v/celerybeat-sqlalchemy-scheduler.svg)](https://pypi.python.org/pypi/celerybeat-sqlalchemy-scheduler)
[![Python Versions](https://img.shields.io/pypi/pyversions/celerybeat-sqlalchemy-scheduler.svg)](https://pypi.python.org/pypi/celerybeat-sqlalchemy-scheduler)

Celery Beat Scheduler which stores entries in a SQLAlchemy database.

## Installation

```bash
pip install celerybeat-sqlalchemy-scheduler
```

Next add the following variable to your Celery config file:

```python
ENGINE_URL = 'postgresql://postgres:password@localhost:5433/my_database'
```

Then simply tell celery beat to use celerybeat-sqlalchemy-scheduler.

```bash
celery -A app.celery beat --scheduler beatdbscheduler.DatabaseScheduler
```
