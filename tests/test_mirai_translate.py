from mirai_translate import Client

def test_client():
    cli = Client()
    assert cli.translate("これはテスト", "ja", "en") == "This is a test."
    assert cli.translate("This is a test.", "en", "ja") == "これはテストです。"
