from dataclasses import dataclass, field
from time import sleep, time
from typing import Optional

from bs4 import BeautifulSoup
import httpx


class MiraiTranslateError(Exception):
    pass


@dataclass
class Client:
    delay_sec: Optional[int] = 3
    _cli: httpx.Client = field(
        default=httpx.Client(base_url="https://miraitranslate.com"), init=False
    )
    # Key required to access `translate.php`
    _tran: Optional[str] = field(default=None, init=False)
    _prev_req_time: Optional[float] = field(default=None, init=False)

    def __post_init__(self):
        self._refresh_tran()

    def _assure_deley(self):
        if self._prev_req_time is not None and self.delay_sec is not None:
            now = time()
            wait_secs = max(0.0, self.delay_sec - (now - self._prev_req_time))
            sleep(wait_secs)

    def _refresh_tran(self):
        self._assure_deley()
        res = self._cli.get("/trial")
        self._prev_req_time = time()
        soup = BeautifulSoup(res.content, "html.parser")
        self._tran = soup.find(id="tranInput")["value"]

    def _translate(self, text: str, source: str, target: str) -> str:
        payload = dict(
            input=text,
            source=source,
            target=target,
            profile="nmt",
            kind="nmt",
            bt=False,
            tran=self._tran,
        )
        self._assure_deley()
        res = self._cli.post("/trial/translate.php", data=payload)
        self._prev_req_time = time()
        j = res.json()

        if j["status"] == "failed":
            raise MiraiTranslateError(j["error_msg"])

        return j["outputs"][0]["output"]

    def translate(self, text: str, source: str, target: str) -> str:
        try:
            return self._translate(text, source, target)
        except MiraiTranslateError:
            self._refresh_tran()
            return self._translate(text, source, target)
