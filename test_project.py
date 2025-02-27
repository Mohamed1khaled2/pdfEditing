import pytest
from pypdf import PdfReader, PdfWriter
from project import pdf_reverse, pdf_split, check_pdf_exstention, pdf_marge
import os


@pytest.fixture
def create_sample_pdfs():
    """
    Fixture to create sample PDF files for testing.
    """
    # Create PdfWriter objects to create sample PDFs
    writer1 = PdfWriter()
    writer2 = PdfWriter()

    # Add blank pages to the first sample PDF
    for _ in range(15):
        writer1.add_blank_page(width=350, height=350)

    # Add blank pages to the second sample PDF
    for _ in range(5):
        writer2.add_blank_page(width=350, height=350)

    # Write the first sample PDF to a file
    with open("sample1.pdf", "wb") as f:
        writer1.write(f)

    # Write the second sample PDF to a file
    with open("sample2.pdf", "wb") as w:
        writer2.write(w)

    yield

    # Teardown: Remove the sample PDF files
    os.remove("sample1.pdf")
    os.remove("sample2.pdf")
    
    if os.path.exists("output/reverse/reverse-sample1.pdf"):
        os.remove("output/reverse/reverse-sample1.pdf")
    if os.path.exists("output/split/split-1-5.pdf"):
        os.remove("output/split/split-1-5.pdf")
    if os.path.exists("output/marge/output.pdf"):
        os.remove("output/marge/output.pdf")


def test_pdf_reverse(create_sample_pdfs):
    """
    Test the pdf_reverse function to ensure it correctly reverses the pages of a PDF.
    """
    name_file = "sample1.pdf"

    # Read the sample PDF
    reader = PdfReader(name_file)

    # Reverse the pages of the sample PDF
    pdf_reverse([name_file])

    # Read the reversed PDF
    reversed_reader = PdfReader(f"output/reverse/reverse-{name_file}")

    # Check that the number of pages in the reversed PDF is the same as the original
    assert len(reversed_reader.pages) == 15

    # Check that the order of pages in the reversed PDF is correct
    for i in range(15):
        assert (
            reversed_reader.pages[i].extract_text()
            == reader.pages[14 - i].extract_text()
        )

    # Test with an invalid file
    with pytest.raises(SystemExit):
        pdf_reverse(["test.pdf"])

         


def test_pdf_split(create_sample_pdfs):
    """
    Test the pdf_split function to ensure it correctly splits the pages of a PDF.
    """
    name_file = "sample1.pdf"

    # Split the sample PDF
    splited_pdf = pdf_split(name_file, from_=1, to=5)

    # Read the second sample PDF
    PdfReader("sample2.pdf")

    # Check that the number of pages in the split PDF matches the expected number of pages
    assert splited_pdf.get_num_pages() == 5

    # Test with an invalid range (from_ > to)
    with pytest.raises(ValueError):
        pdf_split(name_file, from_=9, to=5)

    # Test with an invalid file
    with pytest.raises(ValueError):
        pdf_split("test.pkk", from_=9, to=5)


def test_check_pdf_exstention(create_sample_pdfs):
    """
    Test the check_pdf_exstention function to ensure it correctly identifies PDF files.
    """
    with pytest.raises(ValueError):
        check_pdf_exstention(["file.txt"])
    with pytest.raises(ValueError):
        check_pdf_exstention(["file.txt", "file.pdf"])


def test_pdf_marge(create_sample_pdfs):
    """
    Test the pdf_marge function to ensure it correctly merges multiple PDF files into one.
    """
    # Merge the two sample PDFs
    merged_pdf = pdf_marge(["sample1.pdf", "sample2.pdf"])

    # Check that the number of pages in the merged PDF matches the expected number of pages
    assert merged_pdf.get_num_pages() == 20

    # Test with an invalid file
    with pytest.raises(ValueError):
        merged_pdf = pdf_marge(["sample1.pf", "sample2.pdf"])
        
    with pytest.raises(Exception):
        merged_pdf = pdf_marge(["sample1.pf"])


if __name__ == "__main__":
    pytest.main()
