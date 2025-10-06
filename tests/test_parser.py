from app.prompt_utils import extract_first_json
import pytest
import json

def test_extract_json_simple():
    text = '{"goal":"g","nodes":[]}'
    assert json.loads(extract_first_json(text))["goal"] == "g"

def test_extract_json_wrapped():
    text = "Here is the result:\n```json\n{\"goal\":\"steal\",\"nodes\":[]}\n```"
    assert json.loads(extract_first_json(text))["goal"] == "steal"

def test_extract_json_no_json():
    with pytest.raises(ValueError):
        extract_first_json("no json here")
