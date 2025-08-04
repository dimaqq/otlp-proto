<!-- font_size: 6 -->
<!-- new_lines: 1 -->
### Test slide
<!-- font_size: 1 -->
<!-- column_layout: [1, 1] -->
<!-- column: 0 -->
```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
<!-- column: 1 -->

```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 4 -->
## Python fangs to Rusty nails

<!-- new_lines: 1 -->
re-coding a simple lib
===
Dima Tisnek
---

<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 1 -->
## otlp-json

<!-- font_size: 4 -->
Pure Python, data to JSON

![image:width:80%](otlp-libs.png)

<!-- font_size: 6 -->
### otlp-proto

<!-- font_size: 4 -->
Rust extension, data to protobuf


<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 1 -->
## Python
<!-- font_size: 2 -->
```python
tuple(arg)
```

<!-- font_size: 6 -->
<!-- new_lines: 1 -->
### Rust
<!-- font_size: 2 -->
```rust
let builtins = PyModule::import(py, "builtins")?;
let rv = builtins.call_method1("tuple", (arg.as_ref(),))?;
Ok(rv)
```
<!-- end_slide -->
<!-- font_size: 2 -->
<!-- new_lines: 2 -->

<!-- font_size: 6 -->
## Python
<!-- font_size: 2 -->
```python
  def _ensure_homogeneous(value: Sequence[_LEAF_VALUE]) -> Sequence[_LEAF_VALUE]:
      if len(types := {type(v) for v in value}) > 1:
          raise ValueError(f"Value arrays must be homogeneous, got {types=}")
      return value
```
<!-- new_lines: 2 -->

<!-- font_size: 6 -->
### C-like Rust
<!-- font_size: 2 -->
```rust
#[pyfunction]
#[pyo3(signature = (value))]
fn _ensure_homogeneous(value: &Bound<'_, PyAny>) -> PyResult<()> {
    let mut last: *mut ffi::PyObject = ptr::null_mut();
    for v in value.try_iter()? {
        let class = v?.get_type().as_ptr();
        if !last.is_null() && last != class {
            return Err(PyValueError::new_err(
                "Value arrays must be homogeneous",
            ));
        }
        last = class;
    }
    Ok(())
}
```



<!-- end_slide -->
<!-- font_size: 6 -->
## Python
<!-- font_size: 2 -->

```python
resource_cache: dict[Resource, tuple] = {}
scope_cache: dict[InstrumentationScope, tuple] = {}

def linearise(span: ReadableSpan):
    ...
    # use resource_cache
    # use scope_cache

spans = sorted(spans, key=linearise)
```

<!-- new_lines: 2 -->
<!-- font_size: 6 -->
### Rust
<!-- font_size: 2 -->

```rust
let resource_cache = PyDict::new(py);
let scope_cache = PyDict::new(py);

let key = m.getattr("functools")?.call_method1(
    "partial", (m.getattr("_linearise")?, resource_cache, scope_cache),
)?;

let spans = m.getattr("builtins")?.call_method(
    "sorted", (sdk_spans.as_ref(),), Some(&[("key", key)].into_py_dict(py)?),
)?;
```

<!-- end_slide -->

<!-- font_size: 6 -->
<!-- new_lines: 1 -->
## Python
<!-- font_size: 4 -->
20 years, 2 days
===
<!-- font_size: 6 -->
<!-- new_lines: 1 -->
### Rust
<!-- font_size: 4 -->
2 months, 2 weeks...
==
<!-- end_slide -->

<!-- font_size: 6 -->
<!-- new_lines: 1 -->
## Python
<!-- font_size: 4 -->
```
otlp_json-1.0.0-py3-none-any.whl
```
<!-- font_size: 6 -->
<!-- new_lines: 1 -->
### Rust
<!-- font_size: 4 -->

```
...-pypy311_..._x86_64.whl
...-pypy311_..._i686.whl
...-pypy311_..._armv7l.whl
...-pypy311_..._aarch64.whl
...-cp313-..._x86_64.whl
...-cp313-..._i686.whl
...-cp313-..._armv7l.whl
...-pypy311_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-win_amd64.whl
otlp_proto-0.10.1-cp313-cp313-win32.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp313-cp313-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp313-cp313-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-win_amd64.whl
otlp_proto-0.10.1-cp312-cp312-win32.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp312-cp312-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp312-cp312-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-win_amd64.whl
otlp_proto-0.10.1-cp311-cp311-win32.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp311-cp311-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp311-cp311-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-win_amd64.whl
otlp_proto-0.10.1-cp310-cp310-win32.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp39-cp39-win_amd64.whl
otlp_proto-0.10.1-cp39-cp39-win32.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp38-cp38-win_amd64.whl
otlp_proto-0.10.1-cp38-cp38-win32.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_5_i686.manylinux1_i686.whl
```

<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 1 -->
## Python
<!-- font_size: 2 -->
```
otlp_json-1.0.0-py3-none-any.whl
```

<!-- font_size: 6 -->
<!-- new_lines: 1 -->
### Rust
<!-- font_size: 2 -->

```
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_x86_64.....whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_s390x.....whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_ppc64le.....whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_armv7l.....whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_aarch64.....whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_x86_64.....whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_s390x.....whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_ppc64le.....whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_armv7l.....whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_aarch64.....whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-win_amd64.whl
otlp_proto-0.10.1-cp313-cp313-win32.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp313-cp313-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp313-cp313-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-win_amd64.whl
otlp_proto-0.10.1-cp312-cp312-win32.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp312-cp312-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp312-cp312-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-win_amd64.whl
otlp_proto-0.10.1-cp311-cp311-win32.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp311-cp311-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp311-cp311-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-win_amd64.whl
otlp_proto-0.10.1-cp310-cp310-win32.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp39-cp39-win_amd64.whl
otlp_proto-0.10.1-cp39-cp39-win32.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp38-cp38-win_amd64.whl
otlp_proto-0.10.1-cp38-cp38-win32.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_5_i686.manylinux1_i686.whl
```

<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 1 -->
### Rust
<!-- font_size: 1 -->
<!-- column_layout: [1, 1] -->
<!-- column: 0 -->
```
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_x86_64....2014.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_s390x....2014.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_ppc64le....2014.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_armv7l....2014.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_17_aarch64....2014.whl
otlp_proto-0.10.1-pp311-pypy311_pp73-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_x86_64....2014.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_s390x....2014.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_ppc64le....2014.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_armv7l....2014.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_17_aarch64....2014.whl
otlp_proto-0.10.1-pp310-pypy310_pp73-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_i686.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_s390x....2014.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_ppc64le....2014.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_armv7l....2014.whl
otlp_proto-0.10.1-pp39-pypy39_pp73-manylinux_2_17_aarch64....2014.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp313-cp313t-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_s390x....2014.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_ppc64le....2014.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_armv7l....2014.whl
otlp_proto-0.10.1-cp313-cp313t-manylinux_2_17_aarch64....2014.whl
otlp_proto-0.10.1-cp313-cp313-win_amd64.whl
otlp_proto-0.10.1-cp313-cp313-win32.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp313-cp313-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_x86_64....2014.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_s390x....2014.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_ppc64le....2014.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_armv7l....2014.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_17_aarch64....2014.whl
otlp_proto-0.10.1-cp313-cp313-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp313-cp313-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp313-cp313-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-win_amd64.whl
otlp_proto-0.10.1-cp312-cp312-win32.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp312-cp312-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```
<!-- column: 1 -->

```
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp312-cp312-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp312-cp312-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp312-cp312-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-win_amd64.whl
otlp_proto-0.10.1-cp311-cp311-win32.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp311-cp311-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp311-cp311-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp311-cp311-macosx_11_0_arm64.whl
otlp_proto-0.10.1-cp311-cp311-macosx_10_12_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-win_amd64.whl
otlp_proto-0.10.1-cp310-cp310-win32.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp310-cp310-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp310-cp310-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp39-cp39-win_amd64.whl
otlp_proto-0.10.1-cp39-cp39-win32.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp39-cp39-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp39-cp39-manylinux_2_5_i686.manylinux1_i686.whl
otlp_proto-0.10.1-cp38-cp38-win_amd64.whl
otlp_proto-0.10.1-cp38-cp38-win32.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_x86_64.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_i686.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_armv7l.whl
otlp_proto-0.10.1-cp38-cp38-musllinux_1_2_aarch64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_s390x.manylinux2014_s390x.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_armv7l.manylinux2014_armv7l.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
otlp_proto-0.10.1-cp38-cp38-manylinux_2_5_i686.manylinux1_i686.whl
```

<!-- end_slide -->
<!-- jump_to_middle -->
<!-- font_size: 6 -->
100x Engineer
===
<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 4 -->
✨ Kudos ✨
===
Canonical
===
@nhutsko
===
`presenterm`
===
<!-- end_slide -->
<!-- font_size: 6 -->
<!-- new_lines: 4 -->
Thank you!
===
```bash +exec_replace +no_background
cat crab.bin
```
