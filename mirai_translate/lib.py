import re
from dataclasses import dataclass, field
from time import sleep, time
from typing import Optional

import httpx


class MiraiTranslateError(Exception):
    pass


@dataclass
class Client:
    """Mirai Translate Client.

    Attributes
    ----------
    delay_sec : int
        Minimum request interval (the default is 6 because we can only request up to
        10 per minute).
    """

    delay_sec: Optional[int] = 6
    _cli: httpx.Client = field(
        default=httpx.Client(base_url="https://miraitranslate.com"), init=False,
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
        try:
            res = self._cli.get("/trial")
        except httpx.ReadTimeout:
            raise MiraiTranslateError("Response from Mirai Translate timed out")
        self._prev_req_time = time()
        self._tran = (
            re.search(rb'var tran = "(.+?)";', res.content).group(1).decode("utf-8")
        )

    def _translate(self, text: str, source: str, target: str) -> str:
        payload = dict(
            input=text,
            source=source,
            target=target,
            profile="inmt",
            filter_profile="nmt",
            tran=self._tran,
        )
        self._assure_deley()
        try:
            res = self._cli.post("/trial/api/translate.php", json=payload,)
        except httpx.ReadTimeout:
            raise MiraiTranslateError("Response from Mirai Translate timed out")
        self._prev_req_time = time()
        j = res.json()

        status = j["status"]
        if status == "failed" or status == "limit":
            raise MiraiTranslateError(j["error_msg"])

        if status != "success":
            raise MiraiTranslateError(
                '"status" should be either "failed", "limit", '
                f'or "success" but got {status}'
            )

        return j["outputs"][0]["output"][0]["translation"]

    def translate(self, text: str, source: str, target: str) -> str:
        """Translate `text` from `source` to `target`.

        Parameters
        ----------
        text : str
            Source text.
        source : str
            Source language ("en", "ja", ...).
        target : str
            Target language ("en", "ja", ...).

        Raises
        ------
        MiraiTranslateError

        Returns
        -------
        str
            Translated text.
        """
        try:
            return self._translate(text, source, target)
        except MiraiTranslateError:
            self._refresh_tran()
            return self._translate(text, source, target)
