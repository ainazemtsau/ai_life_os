# Public Surface — backend.core
Version: 0.1.0

## Purpose
Общий модуль для бэкенда (без доменной логики). Поставляет:
- единый формат ошибок **Problem Details (RFC 7807)**;
- глобальные exception handlers;
- обёртку для FastAPI роутеров, автоматически подключающую problem-ответы;
- (опционально) вспомогательные хелперы для OpenAPI (servers/security/теги), если решим вынести их из `app.py`.

## Exports (in-process only)
### `ai_life_backend.core.httpkit`
- `PROBLEM_RESPONSES: dict[int, dict]` — готовые описания ошибок (400/404/422/500) c `content: application/problem+json`.
- `make_public_router(internal: APIRouter) -> APIRouter` — оборачивает модульный `APIRouter`, добавляя `PROBLEM_RESPONSES` ко всем операциям.

### `ai_life_backend.core.errors`
- `Problem` — Pydantic-модель problem-деталей (`type?`, `title`, `status`, `detail?`, `instance?`).
- `http_exception_handler`, `validation_exception_handler` — возвращают `application/problem+json` для `HTTPException` и `RequestValidationError`.

> Примечание: модель `Problem` задокументирована в OpenAPI и **реально используется** в ответах (через обёртку роутера), что удовлетворяет линтеру Redocly и стандарту RFC 7807. :contentReference[oaicite:1]{index=1}

## Usage
```py
# public/__init__.py в модуле фичи
from fastapi import APIRouter
from ai_life_backend.core.httpkit import make_public_router
from ..api.routes import router as _internal

router: APIRouter = make_public_router(_internal)  # добавит Problem-ответы ко всем операциям

__all__ = ["router"]
