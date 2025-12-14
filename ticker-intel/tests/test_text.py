from ticker_intel.text import normalize_text


def test_collapses_multiple_spaces():
    inp = "a   b"
    out = normalize_text(inp)
    assert out == "a b"


def test_collapses_multiple_blank_lines():
    inp = "a\n\n\nb"
    out = normalize_text(inp)
    assert out == "a\n\nb"


def test_idempotent_when_already_clean():
    inp = "a b\n\nc"
    out = normalize_text(inp)
    assert out == inp
