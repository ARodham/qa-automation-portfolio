from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiClient:
    base_url: str
    timeout_seconds: int = 5

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return requests.get(
            self._url(path),
            timeout=self.timeout_seconds,
            **kwargs,
        )

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return requests.post(
            self._url(path),
            timeout=self.timeout_seconds,
            **kwargs,
        )
