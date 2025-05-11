<!-- font_size: 6 -->

# H1

## h2

### Foo

#### Foo

Foo
===

blablabla
---

oi `one` and ``two``.


<!-- end_slide -->
<!-- font_size: 2 -->
Python
==

```python
resource_cache: dict[Resource, tuple] = {}
scope_cache: dict[InstrumentationScope, tuple] = {}

def linearise(span: ReadableSpan):
    ...
    # use resource_cache
    # use scope_cache

spans = sorted(spans, key=linearise)
```

Rust
==

```rust
let builtins = PyModule::import(py, "builtins")?;
let resource_cache = PyDict::new(py);
let scope_cache = PyDict::new(py);

let key = m.getattr("functools")?.call_method1(
    "partial",
    (m.getattr("_linearise")?,
     resource_cache,
     scope_cache),
)?;
let kwargs = [("key", key)].into_py_dict(py)?;

let spans = builtins.call_method(
    "sorted",
    (sdk_spans.as_ref(),),
    Some(&kwargs),
)?;
```

<!-- end_slide -->

<!-- jump_to_middle -->

Farming potatoes
===

<!-- end_slide -->
