import pytest
import respx
from httpx import Response

from mirai_translate import Client


@respx.mock
def test_client():
    trial = respx.get("https://miraitranslate.com/trial",).mock(
        return_value=Response(
            200, content=open("tests/fixtures/index.html", "rb").read()
        )
    )
    cli = Client(delay_sec=0)
    assert trial.called
    assert (
        cli._tran == "xx3At5tG4vPwk3VCwKfXOq43RqCBEzScNvCgRWNvrCH2fDf2yk0m1UGtktVOINQ5"
    )

    translate = respx.post("https://miraitranslate.com/trial/api/translate.php",).mock(
        return_value=Response(
            200,
            json={
                "status": "success",
                "outputs": [
                    {
                        "output": [
                            {
                                "translation": "This is a test.",
                                "sentences": [
                                    {
                                        "original": "これはテスト",
                                        "originalPosition": 0,
                                        "originalLength": 6,
                                        "translation": "This is a test.",
                                        "translationPosition": 0,
                                        "translationLength": 15,
                                        "type": "mt",
                                        "target": "",
                                        "prefix": "",
                                        "boundary": [0, 4, 7, 9],
                                        "originalDelimiter": "",
                                        "delimiter": "",
                                        "words": [],
                                        "sentences": [],
                                    }
                                ],
                            }
                        ]
                    }
                ],
            },
        )
    )
    assert cli.translate("これはテスト", "ja", "en") == "This is a test."
    assert translate.called


@pytest.mark.slow
def test_repeated():
    cli = Client()
    for _ in range(11):
        assert cli.translate("test", "en", "ja") == "試験"
