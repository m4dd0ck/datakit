"""API client utilities with retry logic."""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, RequestException, Timeout


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (RequestException,),
) -> Callable:
    """Decorator for retrying a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exception types to catch

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception

        return wrapper

    return decorator


class APIClient:
    """Simple API client with retry and common patterns.

    Usage:
        with APIClient("https://api.example.com") as client:
            client.set_auth_token("my-token")
            data = client.get("/users")
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        headers: dict[str, str] | None = None,
    ):
        """Initialize API client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            headers: Default headers for all requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        """Make a request, retrying connection errors, timeouts and 5xx responses.

        A 4xx response is raised at once: sending the same request again will not fix it.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        @retry(
            max_attempts=self.max_retries,
            exceptions=(RequestsConnectionError, Timeout, HTTPError),
        )
        def send() -> requests.Response:
            response = self.session.request(method, url, **kwargs)
            # Reason: only server errors raise inside the retry; 4xx is raised below, once.
            if response.status_code >= 500:
                response.raise_for_status()
            return response

        response = send()
        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: dict | None = None, **kwargs) -> Any:
        """Make GET request and return parsed JSON response."""
        response = self._request("GET", endpoint, params=params, **kwargs)
        return response.json()

    def post(
        self, endpoint: str, data: dict | None = None, json: dict | None = None, **kwargs
    ) -> Any:
        """Make POST request and return parsed JSON response."""
        response = self._request("POST", endpoint, data=data, json=json, **kwargs)
        return response.json()

    def put(
        self, endpoint: str, data: dict | None = None, json: dict | None = None, **kwargs
    ) -> Any:
        """Make PUT request and return parsed JSON response."""
        response = self._request("PUT", endpoint, data=data, json=json, **kwargs)
        return response.json()

    def delete(self, endpoint: str, **kwargs) -> Any:
        """Make DELETE request and return parsed JSON response (if any)."""
        response = self._request("DELETE", endpoint, **kwargs)
        if response.content:
            return response.json()
        return None

    def set_auth_token(self, token: str, prefix: str = "Bearer") -> None:
        """Set Authorization header for subsequent requests."""
        self.session.headers["Authorization"] = f"{prefix} {token}"

    def set_api_key(self, key: str, header_name: str = "X-API-Key") -> None:
        """Set API key header for subsequent requests."""
        self.session.headers[header_name] = key

    def close(self) -> None:
        """Close the underlying requests session."""
        self.session.close()

    def __enter__(self) -> "APIClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args) -> None:
        """Context manager exit, closes session."""
        self.close()
