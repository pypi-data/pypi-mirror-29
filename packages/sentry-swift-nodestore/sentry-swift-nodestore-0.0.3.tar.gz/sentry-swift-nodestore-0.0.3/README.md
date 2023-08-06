
Currently only support swauth right now.

# Configuration

```python
SENTRY_NODESTORE = 'sentry_swift_nodestore.backend.SwiftNodeStorage'
SENTRY_NODESTORE_OPTIONS = {
    'container_name': 'my-sentry-bucket',
    'auth_url': 'https://example/auth/v1.0',
    'user': 'test:user',
    'key': 'some key',
    'ttl': 'seconds object valid for after delete',
    'cacert': 'path/to/ca/cert'
}
```