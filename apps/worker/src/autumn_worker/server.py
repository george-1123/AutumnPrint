"""Redis is a wakeup transport; durable queued rows are the outbox of record."""

from autumn_control.infrastructure import Store
from autumn_control.settings import Settings
from celery import Celery

settings = Settings.from_env()
if settings.mode != "enterprise":
    raise ValueError("Celery entry requires enterprise mode")
app = Celery("autumn", broker=settings.broker_url)
app.conf.update(
    task_ignore_result=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={"dispatch-durable-outbox": {"task": "autumn.dispatch", "schedule": 1.0}},
)


@app.task(name="autumn.dispatch")
def dispatch():
    store = Store(settings.database_url)
    try:
        return store.dispatch(settings.workspace)
    finally:
        store.engine.dispose()
