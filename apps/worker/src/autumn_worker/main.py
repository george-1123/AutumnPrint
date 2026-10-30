import logging
import time

from autumn_control.infrastructure import Store
from autumn_control.settings import Settings


def main():
    settings = Settings.from_env()
    if settings.mode != "personal":
        raise SystemExit("enterprise mode: use celery -A autumn_worker.server worker -B")
    store = Store(settings.database_url)
    logging.basicConfig(level=logging.INFO)
    try:
        while True:
            store.dispatch(settings.workspace)
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        store.engine.dispose()


if __name__ == "__main__":
    main()
