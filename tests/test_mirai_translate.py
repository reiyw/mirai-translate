import pytest
import respx

from mirai_translate import Client


@respx.mock
def test_client():
    trial = respx.get(
        "https://miraitranslate.com/trial",
        content=open("tests/fixtures/index.html", "rb").read(),
    )
    cli = Client(delay_sec=0)
    assert trial.called
    assert (
        cli._tran == "xx3At5tG4vPwk3VCwKfXOq43RqCBEzScNvCgRWNvrCH2fDf2yk0m1UGtktVOINQ5"
    )

    translate = respx.post(
        "https://miraitranslate.com/trial/translate.php",
        content={"status": "success", "outputs": [{"output": "This is a test."}]},
    )
    assert cli.translate("これはテスト", "ja", "en") == "This is a test."
    assert translate.called


@pytest.mark.slow
def test_repeated():
    cli = Client()
    for _ in range(11):
        assert cli.translate("test", "en", "ja") == "試験"
