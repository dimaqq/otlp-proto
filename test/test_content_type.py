from __future__ import annotations

import otlp_proto


def test_content_type():
    assert otlp_proto.CONTENT_TYPE == "application/x-protobuf"
