import requests, simplejson as json, tenacity
from . import exceptions



def by_method_request(method, *args, **kwargs):
    method = getattr(requests, method, None)
    if method is None:
        raise exceptions.MethodNotSupported()
    return method(*args, **kwargs)


def get_response(method, *args, **kwargs):
    try:
        response = by_method_request(method, *args, **kwargs)
    except requests.exceptions.Timeout:
        raise exceptions.Timeout()
    except requests.exceptions.ConnectionError:
        raise exceptions.ConnectionError()
    
    return response


def get_custom_get_response(max_tries, delay_between_requests):

    @tenacity.retry(
        retry = (tenacity.retry_if_exception_type(exceptions.Timeout) | tenacity.retry_if_exception_type(exceptions.ConnectionError)),
        stop = tenacity.stop_after_attempt(max_tries),
        wait = tenacity.wait_fixed(delay_between_requests)
    )
    def _get_response(method, *args, **kwargs):
        return get_response(method, *args, **kwargs)
    
    return _get_response

def get_default_headers():
    headers = {
        "User-Agent": "TEST",
    }
    return headers


def safe_request(url, method = "post", **options):
    max_tries = options.get("max_tries", 5)
    delay_between_requests = options.get("delay_between_requests", 1)
    request_timeout = options.get("request_timeout", None)
    
    return_value_on_max_tries_reached = options.get("return_value_on_max_tries_reached", None)
    


    get_response_kwargs = {}


    if request_timeout:
        get_response_kwargs["timeout"] = request_timeout
    

    headers = options.get("headers", None)
    if options.get("get_default_headers") and headers is None:
        headers = get_default_headers()


    if headers:
        get_response_kwargs["headers"] =  headers
    

    data = options.get("data", None)
    if data:
        if options.get("convert_data_to_json", False) is True:
            data = json.dumps(data)
        get_response_kwargs["data"] =  data

    try:
        response = get_custom_get_response(max_tries, delay_between_requests)(method, url, **get_response_kwargs)
    except tenacity.RetryError:
        response = return_value_on_max_tries_reached
    return response

def send_post_and_get_response(url, **options):
    return safe_request(url, "post", **options)

def send_get_and_get_response(url, **options):
    return safe_request(url, "get", **options)

def send_post(url, **options):
    response = send_post_and_get_response(url, **options)
    if response:
        if response.status_code == requests.codes.ok:
            return (True, exceptions.BadRequest())
        return (False, response.reason)
    return (False, exceptions.BadRequest())
    

def send_get(url, **options):
    response = send_get_and_get_response(url, **options)
    if response:
        if response.status_code == requests.codes.ok:
            return (True, None)
        return (False, response.reason)
    return (False, exceptions.BadRequest())