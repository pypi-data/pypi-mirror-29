import os
import requests
from requests_cache import CachedSession
from prometheus_client import Counter, Histogram
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


# Settings
global_timeout = int(os.environ.get('REQUESTS_TIMEOUT')) or 2
cache_expiry = int(os.environ.get('REQUESTS_CACHE_EXPIRY')) or 300
prometheus_buckets = [timeout]

# Add some intervals for the request delay metrics Histogram
for threshold in [0.25, 0.5, 0.75, 1, 2, 5, 10]:
    if threshold < timeout:
        prometheus_buckets.insert(0, threshold)

# Prometheus metric exporters
requested_from_cache_counter = Counter(
    'http_request_from_cache',
    'A counter of requests retrieved from the cache',
    ['method', 'domain'],
)
failed_requests = Counter(
    'http_request_failed',
    'A counter of requests retrieved from the cache',
    ['method', 'domain', 'error_name'],
)
request_latency_seconds = Histogram(
    'http_request_latency_seconds',
    'Feed requests retrieved',
    ['method', 'domain', 'code'],
    buckets=prometheus_buckets,
)

cached_request = CachedSession(expire_after=expiry)


def get(url, headers=None, timeout=global_timeout, session=requests):
    """
    Get a URL's response, without using any caching.

    Use the globally configured timeout (REQUESTS_TIMEOUT or 2 seconds)
    and report Prometheus metrics
    """

    domain = urlparse(url).netloc

    try:
        response = session.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
    except Exception as request_error:
        error = type(request_error).__name__
        failed_requests.labels(
            method="get", domain=domain, error_name=error
        ).inc()
        raise request_error

    if hasattr(response, 'from_cache') and response.from_cache:
        requested_from_cache_counter.labels(
            method="get", domain=domain,
        ).inc()
    else:
        request_latency_seconds.labels(
            method="get", domain=domain, code=response.status_code,
        ).observe(response.elapsed.total_seconds())

    return response


def post(
    url,
    headers=None, json=None, data=None, files=None,
    timeout=global_timeout, session=requests
):
    """
    Get a URL's response, without using any caching.

    Use the globally configured timeout (REQUESTS_TIMEOUT or 2 seconds)
    and report Prometheus metrics
    """

    domain = urlparse(url).netloc

    try:
        response = requests.post(
            url,
            timeout=timeout,
            headers=headers,
            json=json,
            data=data,
            files=files
        )
        response.raise_for_status()
    except Exception as request_error:
        failed_requests.labels(
            method="post",
            domain=domain,
            error_name=type(request_error).__name__,
        ).inc()
        raise request_error

    request_latency_seconds.labels(
        method="post",
        domain=domain,
        code=response.status_code,
    ).observe(response.elapsed.total_seconds())

    return response


def get_through_cache(url, headers=None, timeout=global_timeout):
    """
    Get a URL's response, using caching.

    Use the globally configured cache expiry time (REQUESTS_EXPIRY or 300)
    """

    return get(url, headers=headers, timeout=timeout, session=cached_request)
