import hmac
from contextlib import asynccontextmanager

from autumn_contracts import (
    Command,
    CompleteCommand,
    DiagnosticRequest,
    EdgeRegistration,
    Task,
    TaskEvent,
)
from autumn_control.infrastructure import Store
from autumn_control.migrate import migrate
from autumn_control.settings import Settings
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def create_app(settings=None):
    settings = settings or Settings.from_env()
    store = Store(settings.database_url)

    @asynccontextmanager
    async def lifespan(app):
        migrate(settings.database_url)
        yield
        store.engine.dispose()

    app = FastAPI(title="Autumn Print Bootstrap", version="0.1.0", lifespan=lifespan)
    bearer = HTTPBearer(auto_error=False)

    def auth(expected):
        def check(
            request: Request, credential: HTTPAuthorizationCredentials | None = Depends(bearer)
        ):
            if request.headers.get("origin") not in (None, "app://autumn"):
                raise HTTPException(403, "origin denied")
            if not credential or not hmac.compare_digest(credential.credentials, expected):
                raise HTTPException(401, "invalid credential")

        return check

    desktop = Depends(auth(settings.desktop_token))
    edge = Depends(auth(settings.edge_token))

    @app.exception_handler(KeyError)
    async def missing(request, exc):
        from fastapi.responses import JSONResponse

        return JSONResponse({"detail": "task not found"}, status_code=404)

    @app.exception_handler(PermissionError)
    async def forbidden(request, exc):
        from fastapi.responses import JSONResponse

        return JSONResponse({"detail": str(exc)}, status_code=403)

    @app.get("/health", operation_id="health")
    def health():
        return {"status": "ok", "mode": settings.mode, "protocol_version": "1"}

    @app.get("/tasks", response_model=list[Task], dependencies=[desktop], operation_id="list_tasks")
    def list_tasks():
        return store.list_tasks(settings.workspace)

    @app.post(
        "/tasks/diagnostic",
        response_model=Task,
        dependencies=[desktop],
        operation_id="submit_diagnostic",
    )
    def submit(body: DiagnosticRequest):
        return store.submit(settings.workspace, body.idempotency_key)

    @app.get(
        "/tasks/{task_id}", response_model=Task, dependencies=[desktop], operation_id="get_task"
    )
    def get(task_id: str):
        return store.get(settings.workspace, task_id)

    @app.get(
        "/tasks/{task_id}/events",
        response_model=list[TaskEvent],
        dependencies=[desktop],
        operation_id="task_events",
    )
    def task_events(task_id: str, after: int = Query(0, ge=0)):
        # Cursor polling supports reconnect/replay; SSE transport is a later increment.
        return store.task_events(settings.workspace, task_id, after)

    @app.post("/edge/register", dependencies=[edge], operation_id="register_edge")
    def register(body: EdgeRegistration):
        store.register(settings.workspace, body.edge_id)
        return {"registered": True}

    @app.post(
        "/edge/{edge_id}/claim",
        response_model=Command | None,
        dependencies=[edge],
        operation_id="claim_command",
    )
    def claim(edge_id: str):
        return store.claim(settings.workspace, edge_id)

    @app.post(
        "/edge/{edge_id}/commands/{command_id}/complete",
        dependencies=[edge],
        operation_id="complete_command",
    )
    def complete(edge_id: str, command_id: str, body: CompleteCommand):
        store.complete(settings.workspace, edge_id, command_id, body.lease_token, body.receipt)
        return {"accepted": True}

    return app
