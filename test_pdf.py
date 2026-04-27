from utils.file_extractor import extract_pdf_text


def test_extract_pdf_text_missing_file_returns_empty(tmp_path):
    missing_pdf = tmp_path / "missing.pdf"
    assert extract_pdf_text(str(missing_pdf)) == ""
