import os
import pytest
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pdf_edit import PDFEdit


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


@pytest.fixture(scope="module")
def sample_pdfs(tmp_path_factory):
    """ينشئ ملفين PDF مؤقتين لاستخدامهم في كل الاختبارات."""
    temp_dir = tmp_path_factory.mktemp("pdfs")

    file1 = temp_dir / "sample1.pdf"
    file2 = temp_dir / "sample2.pdf"

    writer1 = PdfWriter()
    for _ in range(10):
        writer1.add_blank_page(width=300, height=300)
    with open(file1, "wb") as f:
        writer1.write(f)

    writer2 = PdfWriter()
    for _ in range(5):
        writer2.add_blank_page(width=300, height=300)
    with open(file2, "wb") as f:
        writer2.write(f)

    return [file1, file2]


@pytest.fixture(scope="module")
def pdf_instance(tmp_path_factory):
    """ينشئ نسخة من PDFEdit داخل فولدر مؤقت."""
    out_dir = tmp_path_factory.mktemp("output")
    return PDFEdit(output_dir=out_dir)


# ---------------------------------------------------------------------
# ✅ 1. check_pdf_extension
# ---------------------------------------------------------------------
def test_check_pdf_extension_valid(pdf_instance, sample_pdfs):
    assert pdf_instance.check_pdf_extension([str(sample_pdfs[0])]) == (True, "")


def test_check_pdf_extension_invalid_ext(pdf_instance, tmp_path):
    bad_file = tmp_path / "file.txt"
    bad_file.write_text("not a pdf")

    assert pdf_instance.check_pdf_extension([str(bad_file)]) == (
        False,
        f"The file '{bad_file}' does not have a .pdf extension.",
    )


def test_check_pdf_extension_missing_file(pdf_instance):
    assert pdf_instance.check_pdf_extension(["not_found.pdf"]) == (
        False,
        f"The file 'not_found.pdf' does not exist.",
    )


# ---------------------------------------------------------------------
# ✅ 2. __search_is_name_valid
# ---------------------------------------------------------------------
def test_search_is_name_valid(pdf_instance, tmp_path):
    file_name = "test.pdf"
    # create existing file
    existing = tmp_path / file_name
    existing.write_text("dummy")
    new_name = pdf_instance._PDFEdit__search_is_name_valid(file_name, str(tmp_path))
    assert new_name != file_name
    assert "copy-" in new_name


# ---------------------------------------------------------------------
# ✅ 3. __save_file_as_pdf
# ---------------------------------------------------------------------
def test_save_file_as_pdf(pdf_instance, tmp_path):
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    pdf_instance._PDFEdit__save_file_as_pdf(
        process="split", name="unit-test.pdf", writer=writer
    )
    output_file = pdf_instance.output_dir / "split" / "unit-test.pdf"
    assert output_file.exists()
    assert PdfReader(output_file)


# ---------------------------------------------------------------------
# ✅ 4. pdf_reverse
# ---------------------------------------------------------------------
def test_pdf_reverse(pdf_instance, sample_pdfs):
    pdf_instance.pdf_reverse([str(sample_pdfs[0])])
    output_file = pdf_instance.output_dir / "reverse" / f"reverse-{sample_pdfs[0].name}"
    assert output_file.exists()
    reader = PdfReader(output_file)
    assert len(reader.pages) == 10


# ---------------------------------------------------------------------
# ✅ 5. pdf_split
# ---------------------------------------------------------------------
def test_pdf_split_valid(pdf_instance, sample_pdfs):
    pdf_instance.pdf_split([str(sample_pdfs[0])], from_=2, to=5)
    output_dir = pdf_instance.output_dir / "split"
    files = list(output_dir.glob("split-*.pdf"))
    assert len(files) > 0
    reader = PdfReader(files[-1])
    assert len(reader.pages) == 4  # pages 2 to 5 inclusive


def test_pdf_split_invalid_range(pdf_instance, sample_pdfs, capsys):
    pdf_instance.pdf_split([str(sample_pdfs[0])], from_=7, to=3)
    out = capsys.readouterr().out
    assert "Invalid range" in out or "⚠️" in out


def test_pdf_split_out_of_bounds(pdf_instance, sample_pdfs, capsys):
    pdf_instance.pdf_split([str(sample_pdfs[0])], from_=50, to=100)
    out = capsys.readouterr().out
    assert "Invalid 'from_'" in out or "⚠️" in out


def test_pdf_split_multiple_files(pdf_instance, sample_pdfs):
    pdf_instance.pdf_split([str(sample_pdfs[0]), str(sample_pdfs[1])], from_=1, to=3)
    out_dir = pdf_instance.output_dir / "split"
    files = list(out_dir.glob("split-*.pdf"))
    assert len(files) >= 2


# ---------------------------------------------------------------------
# ✅ 6. pdf_marge
# ---------------------------------------------------------------------
def test_pdf_marge_valid(pdf_instance, sample_pdfs):
    merged = pdf_instance.pdf_marge([str(sample_pdfs[0]), str(sample_pdfs[1])])
    assert merged.get_num_pages() == 15

    output_file = pdf_instance.output_dir / "marge" / "merger-output.pdf"
    assert output_file.exists()
    reader = PdfReader(output_file)
    assert len(reader.pages) == 15


def test_pdf_marge_invalid_ext(pdf_instance, sample_pdfs):
    bad_file = str(sample_pdfs[0]).replace(".pdf", ".txt")

    assert pdf_instance.pdf_marge([bad_file, str(sample_pdfs[1])]) == (
        False,
        f"The file '{bad_file}' does not have a .pdf extension.",
    )


def test_pdf_marge_one_file(pdf_instance, sample_pdfs):
    with pytest.raises(ValueError):
        pdf_instance.pdf_marge([str(sample_pdfs[0])])
