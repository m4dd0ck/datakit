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


def test_cached_keeps_the_wrapped_function_name_and_docstring(tmp_path):
    @cache.cached(cache=cache.FileCache(tmp_path))
    def lookup(key: str) -> str:
        """Look a key up."""
        return key

    assert lookup.__name__ == "lookup"
    assert lookup.__doc__ == "Look a key up."
