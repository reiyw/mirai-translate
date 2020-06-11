# mirai-translate

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mirai-translate)
![PyPI](https://img.shields.io/pypi/v/mirai-translate)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/reiyw/mirai-translate/Tests)

mirai-translate is an unofficial [Mirai Translate](https://miraitranslate.com/en/) API for Python.

```
pip install mirai-translate
```

```python
>>> from mirai_translate import Client
>>> cli = Client()
>>> cli.translate('テスト', 'ja', 'en')
'Test'
```

## Disclaimer

mirai-translate simply accesses [Translation Demo](https://miraitranslate.com/en/trial/) and requests to the behind API server.
I believe there is no illegality in using this library.
However, you might want to read the [Terms of Use for Mirai Translate](https://miraitranslate.com/en/trial/pdf/kiyaku.pdf).
