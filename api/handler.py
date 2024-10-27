import os
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WorkWonders.settings")
application = get_wsgi_application()

def handler(event, context):
    environ = {
        "REQUEST_METHOD": event['httpMethod'],
        "PATH_INFO": event['path'],
        "QUERY_STRING": event['queryStringParameters'] or '',
        "wsgi.input": event['body'] or '',
        "wsgi.url_scheme": "https" if event['headers'].get('X-Forwarded-Proto', '').lower() == 'https' else 'http',
        "CONTENT_TYPE": event['headers'].get('Content-Type', ''),
        "CONTENT_LENGTH": str(len(event['body'])) if event['body'] else '0',
    }

    # Add other headers if necessary
    for key, value in event['headers'].items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value

    status, headers = application(environ, lambda status, headers: (status, headers))

    response_body = JsonResponse(status, safe=False).content
    return {
        "statusCode": status,
        "headers": {header[0]: header[1] for header in headers},
        "body": response_body.decode(),
    }
