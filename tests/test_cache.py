import cache


def test_cached_stores_a_none_result_instead_of_recomputing(tmp_path):
    calls = []

    @cache.cached(cache=cache.FileCache(tmp_path))
    def lookup(key: str) -> None:
        calls.append(key)
        return None

    assert lookup("a") is None
    assert lookup("a") is None
    assert calls == ["a"]
