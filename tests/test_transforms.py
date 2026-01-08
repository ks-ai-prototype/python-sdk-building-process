from demo_elt_framework.transforms import clean_columns, dedupe, trim_strings, drop_nulls, rename_keys

def test_clean_columns():
    assert clean_columns(["First Name", " City "]) == ["first_name", "city"]

def test_dedupe():
    data = [{"id": 1, "x": "a"}, {"id": 1, "x": "b"}, {"id": 2, "x": "c"}]
    assert dedupe(data, ["id"]) == [{"id": 1, "x": "a"}, {"id": 2, "x": "c"}]

def test_trim_strings():
    data = [{"a": " x ", "b": 1}]
    assert trim_strings(data) == [{"a": "x", "b": 1}]

def test_drop_nulls():
    data = [{"a": "x"}, {"a": ""}, {"a": None}, {"a": "y"}]
    assert drop_nulls(data, ["a"]) == [{"a": "x"}, {"a": "y"}]

def test_rename_keys():
    r = {"First Name": "Kunal", "Age": 40}
    assert rename_keys(r, {"First Name": "first_name"}) == {"first_name": "Kunal", "Age": 40}
