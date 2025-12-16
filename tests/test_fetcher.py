import types

import pytest

import pipeline.fetcher as fetcher


def test_fetch_all_data_stops_on_empty(monkeypatch):
    calls = []

    def fake_fetch_page(page, client=None):
        calls.append(page)
        if page <= 2:
            return {"products": [{"code": str(page)}]}
        return {"products": []}

    monkeypatch.setattr(fetcher, "fetch_page", fake_fetch_page)
    monkeypatch.setattr(fetcher, "MAX_PAGES", 5)
    monkeypatch.setattr(fetcher, "RATE_LIMIT_DELAY", 0)

    data = fetcher.fetch_all_data()

    assert [p["code"] for p in data] == ["1", "2"]
    # boucle doit s'arrêter dès la première page vide (page 3)
    assert calls == [1, 2, 3]


def test_fetch_page_raises_on_http_error(monkeypatch):
    # Simule un client httpx avec raise_for_status qui lève
    def fake_get(url, params=None, timeout=None):
        resp = types.SimpleNamespace()

        def raise_for_status():
            raise Exception("HTTP 500")

        resp.raise_for_status = raise_for_status
        return resp

    class FakeClient:
        def get(self, url, params=None, timeout=None):
            return fake_get(url, params, timeout)

    with pytest.raises(Exception):
        fetcher.fetch_page(1, client=FakeClient())

