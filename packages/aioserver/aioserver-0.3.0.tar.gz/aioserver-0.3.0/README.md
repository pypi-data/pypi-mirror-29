aioserver
===

Installation
---

```
pip install aioserver
```

Usage
---

```python
from aioserver import Application

app = Application()

@app.get('/')
async def index(request):
    return {'message': 'Hello, world!'}

app.run(host='127.0.0.1', port=8080)
```

Changelog
---

### v0.2.0

- Decorator-based request handlers

### v0.3.0

* Allow handler to specify HTTP response status
* Allow handler to specify additional HTTP headers

