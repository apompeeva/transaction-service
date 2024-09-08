from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from jaeger_client import Config
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags
)

from app.config import JAEGER_AGENT_HOST, JAEGER_AGENT_PORT
from app.endpoints.endpoints import transaction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': JAEGER_AGENT_HOST,
                'reporting_port': JAEGER_AGENT_PORT,
            },
            'logging': True,
        },
        service_name='transaction-service-pompeeva',
        validate=True,
    )
    tracer = config.initialize_tracer()
    yield {
        'jaeger_tracer': tracer,
    }


app = FastAPI(lifespan=lifespan)


@app.middleware('http')
async def tracing_middleware(request: Request, call_next):
    path = request.url.path
    if path.startswith('/healthz/ready') or path.startswith('/metrics'):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS,
            request.headers,
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f'transaction_{request.method}_{path}',
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        response = await call_next(request)
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        return response


app.include_router(transaction_router, tags=['transaction'])
