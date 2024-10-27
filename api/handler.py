import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WorkWonders.settings")
application = get_wsgi_application()

def handler(event, context):
    environ = {
        "REQUEST_METHOD": event['httpMethod'],
        "PATH_INFO": event['path'],
        "QUERY_STRING": event['queryStringParameters'] or '',
        "wsgi.input": event['body'].encode() if event['body'] else b'',  # Encode body as bytes
        "wsgi.url_scheme": "https" if event['headers'].get('X-Forwarded-Proto', '').lower() == 'https' else 'http',
        "CONTENT_TYPE": event['headers'].get('Content-Type', ''),
        "CONTENT_LENGTH": str(len(event['body'])) if event['body'] else '0',
    }

   
    headers = []

   
    for key, value in event['headers'].items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value

   
    status_code = '200 OK'
    
    def start_response(status, response_headers):
        nonlocal status_code
        status_code = status
        headers[:] = response_headers  

    response_body = application(environ, start_response)

    
    return {
        "statusCode": int(status_code.split(' ')[0]),  
        "headers": {header[0]: header[1] for header in headers},  
        "body": b''.join(response_body).decode(),  
    }
