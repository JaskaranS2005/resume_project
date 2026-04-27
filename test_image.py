from utils.file_extractor import extract_image_text


def test_extract_image_text_missing_file_returns_empty(tmp_path):
    missing_image = tmp_path / "missing.png"
    assert extract_image_text(str(missing_image)) == ""
