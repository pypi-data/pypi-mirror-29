class QueryPageGenerator(object):
    def __init__(self, method):
        self.method = method

    def paginate(self, *args, **kargs):
        while True:
            request = self.method(*args, **kargs)
            response = request.execute()
            yield response

            if 'nextPageToken' not in response:
                break

            kargs['pageToken'] = response['nextPageToken']


class BodyPageGenerator(object):
    def __init__(self, method):
        self.method = method

    def paginate(self, *args, **kargs):
        if 'body' not in kargs:
            kargs['body'] = {}

        if not isinstance(kargs['body'], dict):
            raise ValueError('The supplied body field must be a dictionary')

        while True:
            request = self.method(*args, **kargs)
            response = request.execute()
            yield response

            if 'nextPageToken' not in response:
                break

            kargs['body']['pageToken'] = response['nextPageToken']


def _get_body_schema(client, parameters):
    schema_name = parameters.get('body', {}).get('$ref')
    schemas = client._rootDesc.get('schemas', {})
    return schemas.get(schema_name)


def get_paginator(client, method_name):
    '''Request a paginator for the given client & method.

    '''
    methods = client._resourceDesc.get('methods', {})
    if method_name not in methods:
        raise ValueError('The provided client has no method %s' % method_name)

    method = methods[method_name]
    parameters = method.get('parmeters', {})
    if method['httpMethod'] == 'GET':
        return _get_query_paginator(client, method_name, method, parameters)
    else:
        return _get_body_paginator(client, method_name, method, parameters)


def _get_query_paginator(client, method_name, method, parameters):
    if method['httpMethod'] == 'GET' and 'pageToken' not in parameters:
        raise ValueError('%s does not accept a pageToken parameter' % method_name)

    return QueryPageGenerator(getattr(client, method))


def _get_body_paginator(client, method_name, method, parameters):
    schema = _get_body_schema(client, parameters)
    schema_properties = schema.get('properties', {})
    if 'pageToken' not in schema_properties:
        raise ValueError('%s does not accept a pageToken parameter' % method_name)
    return BodyPageGenerator(getattr(client, method))
