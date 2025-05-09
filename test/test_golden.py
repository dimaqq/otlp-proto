from __future__ import annotations

from unittest.mock import Mock

import otlp_proto


def test_golden(pytestconfig):
    good_status = Mock()
    good_status.status_code.value = 0
    good_status.status_code.description = "Hi!"

    context = Mock()
    context.span_id = 42
    context.trace_id = 42

    resource = Mock()
    resource.attributes = {"int": 42, "str": "oh"}
    resource.schema_url = "http://r.example"

    scope = Mock()
    scope.name = "na"
    scope.version = "42.0"
    scope.schema_url = "http://s.example"

    span1 = Mock()
    span1.name = "s1"
    span1.context = context
    span1.resource = resource
    span1.instrumentation_scope = scope
    span1.status = good_status
    span1.kind = 0
    span1.start_time = 2_123_456_789_001_002_003  # ns
    span1.end_time = 2_123_456_789_999_999_999
    span1.flags = 0

    span2 = Mock()
    span2.name = "s2"
    span2.context = context
    span2.resource = resource
    span2.instrumentation_scope = scope
    span2.status = good_status
    span2.kind = 0
    span2.start_time = 2_000_000_000_001_002_003
    span2.end_time = 2_000_000_000_999_999_999
    span2.flags = 0

    assert (
        otlp_proto.encode_spans([span1, span2])
        == (pytestconfig.rootpath / "test/data/golden1.bin").read_bytes()
    )
