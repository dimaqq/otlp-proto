from __future__ import annotations

import subprocess
from unittest.mock import Mock

import otlp_test_data

import pytest
from typing_extensions import reveal_type as reveal_type

import otlp_proto


@pytest.fixture
def mock_span():
    """Minimal OTEL-like API."""
    good = Mock()
    good.status_code.value = 0

    class Context:
        span_id = 42
        trace_id = 42

    class Resource:
        attributes = dict()

    class Scope:
        name = "foo"
        version = "1.2.3"

    class Span:
        name = "booya"
        context = Context()
        resource = Resource()
        instrumentation_scope = Scope()
        status = good

    return Span()


def test_encode_spans(mock_span) -> None:
    otlp_proto.encode_spans([mock_span])


def test_function_signature() -> None:
    res = otlp_proto.encode_spans(otlp_test_data.sample_spans())
    kwres: bytes = otlp_proto.encode_spans(sdk_spans=otlp_test_data.sample_spans())
    assert res == kwres


def test_equivalence() -> None:
    auth = otlp_test_data.sample_proto()
    mine = otlp_proto.encode_spans(otlp_test_data.sample_spans())
    assert text(mine) == text(auth)
    assert mine == auth


# TODO: skip tests is protoc is not in PATH
def text(data: bytes) -> str:
    return subprocess.run(
        [
            "protoc",
            "--decode=opentelemetry.proto.collector.trace.v1.ExportTraceServiceRequest",
            "opentelemetry/proto/collector/trace/v1/trace_service.proto",
        ],
        input=data,
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
