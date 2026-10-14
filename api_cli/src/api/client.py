import json
from pathlib import Path
from typing import Any
import requests
from requests.exceptions import HTTPError, RequestException
from api.exceptions import ApiError, NetworkError
from api.http_metod import HTTPMethod
from config.models import ApiArgs


class ApiClient:
    def __init__(self, args: ApiArgs):
        self.base_url = args.api_url.rstrip("/")
        self.timeout = args.timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {args.token}"})

    def _request(self, method: HTTPMethod, endpoint: str, **kwargs) -> Any:
        try:
            kwargs.setdefault("timeout", self.timeout)
            resp = self.session.request(
                method.value, f"{self.base_url}{endpoint}", **kwargs
            )
            resp.raise_for_status()

            if resp.status_code == 204:
                return None
            try:
                return resp.json()
            except json.JSONDecodeError:
                return resp.text

        except HTTPError as e:
            error_detail = resp.text if resp.text else str(e)
            raise ApiError(resp.status_code, error_detail) from e
        except RequestException as e:
            raise NetworkError(f"Request failed: {e}") from e

    def upload_file(self, file_path: Path, duration: float, plugins: list[str]) -> dict:
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}
            data = {"duration": duration, "plugins": plugins}
            return self._request(HTTPMethod.POST, "/upload", files=files, data=data)

    def list_tasks(self) -> list[str] | None:
        return self._request(HTTPMethod.GET, "/list")

    def get_status(self, task_uid: str) -> dict:
        return self._request(HTTPMethod.GET, f"/status/{task_uid}")

    def get_files(self, task_uid: str) -> list[str]:
        return self._request(HTTPMethod.GET, f"/files/{task_uid}")

    def get_analysis(self, task_uid: str) -> dict:
        return self._request(HTTPMethod.GET, f"/analysis/{task_uid}")

    def get_download_stream(
        self, task_uid: str, filename: str, start_byte: int = 0
    ) -> requests.Response:
        headers = {}
        if start_byte > 0:
            headers["Range"] = f"bytes={start_byte}-"

        try:
            return self.session.get(
                f"{self.base_url}/files/{task_uid}/download",
                params={"filename": filename},
                stream=True,
                headers=headers,
                timeout=(self.timeout, 300.0),
            )
        except RequestException as e:
            raise NetworkError(f"Request failed: {e}") from e
