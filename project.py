from pypdf import PdfWriter, PdfReader
import argparse
import sys
import os

def check_pdf_exstention(name_files: list[str])-> bool:
    """
    Check if the provided files have a PDF extension and is exists.

    :param name_files: List of file names to check.
    :return: True if all files have a PDF extension, raises ValueError otherwise.
    """


    for file in name_files:
        if not file.split(".")[1] in ["pdf", "PDF"]:
            raise ValueError("Erorr: mime_type wrong")
    return True


def pdf_reverse(original_files: list[str]):
    """
    Reverse the pages of PDF files.

    :param original_files: List of original PDF file names.
    :param reverse_names: List of new PDF file names.
    """

    check_pdf_exstention(original_files)

    reverse_names = [f"reverse-{file}" for file in original_files]

    for index in range(len(original_files)):
        # Read the original PDF file
        try:
            reader = PdfReader(original_files[index])
        except FileNotFoundError:
            sys.exit(f"Not found the file {original_files[index]}")

        writer = PdfWriter()

        # Copy metadata from the original PDF
        writer.add_metadata(reader.metadata)

        # Reverse the pages and add table of contents
        page_number = 0
        num_pages = len(reader.pages)

        for page in range(num_pages - 1, -1, -1):
            # Get the page object
            page_opj = reader.pages[page]
            # Add the page to the writer
            writer.add_page(page_opj)

            # Add the outline item (bookmark) to the writer
            if len(reader.outline) != 0:
                writer.add_outline_item(
                    reader.outline[page].title, page_number=page_number
                )
                page_number += 1

        # Define the output directory and file path
        output_dir = "output/reverse"
        file_output = os.path.join(output_dir, reverse_names[index])

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Write the reversed pages to a new file
        with open(file_output, "wb") as new_file:
            writer.write(new_file)

    return writer


def pdf_split(original_file: str, from_: int, to: int):
    """
    Split a PDF file into a new PDF file containing pages from 'from_' to 'to'.

    :param original_file: The original PDF file name.
    :param from_: The starting page number (1-based index).
    :param to: The ending page number (1-based index).
    """

    # Check PDF Extension
    check_pdf_exstention([original_file])

    # Validate Page Range
    if from_ > to:
        raise ValueError("'from_' must be less than 'to'")

    # Read PDF File
    try:
        reader = PdfReader(original_file)
    except FileNotFoundError:
        sys.exit(f"Not found the file {original_file}")

    # Initialize PDF Writer
    writer = PdfWriter()

    # Add Pages to Writer
    for i in range(from_ - 1, to):
        try:
            writer.add_page(reader.pages[i])
        except IndexError:
            sys.exit(f"Your pdf pages mixmum equal {len(reader.pages)}")
    
    # Check Page Count
    if len(reader.pages) == len(writer.pages):
        sys.exit("This equal")    
    
    # Define Output Directory
    output_dir = "output/split"
    file_output = os.path.join(output_dir, f"split-{from_}-{to}.pdf")
    
    # Create Output Directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Write Split PDF
    with open(file_output, "wb") as new_file:
        writer.write(new_file)

    return writer


def pdf_marge(pdfs: list[str]):
    """
    Merge multiple PDF files into one.

    :param pdfs: List of PDF file names to be merged.
    :return: PdfWriter object containing the merged PDF.
    """

    check_pdf_exstention(pdfs)
    
    if len(pdfs) < 2:
        raise ValueError("less than two file")

    # Create a PdfWriter object to write the merged PDF
    marger = PdfWriter()

    # Iterate over the list of PDF files
    for pdf in pdfs:
        # check if the file exists
        try:
            # Append each PDF file to the PdfWriter object
            marger.append(open(pdf, "rb"))
        except FileNotFoundError:
            sys.exit(f"This is File Not found {pdf}")
    
    # Define the output directory and file path
    output_dir = "output/marge"
    file_output = os.path.join(output_dir, f"output.pdf")
    os.makedirs(output_dir, exist_ok=True)

    # Write the merged PDF to the output file
    with open(file_output, "wb") as new_file:
        marger.write(new_file)
        new_file.close()

    # Close the PdfWriter and output file
    marger.close()

    # Return the PdfWriter object containing the merged PDF
    return marger


def main():
    """
    Main function to reverse the pages of example PDF files, split PDF files, or merge PDF files.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Reverse the pages of PDF files, split pages, or merge PDF files",
        usage="""
            You can split pdf, You can reverse pdf, You can merge pdf
            
            Running like this:
            for reverse: python project.py --option rev --files path/to/your/file.pdf
            for split: python project.py --option split --files path/to/your/file.pdf --from_ num1 --to num2
            for merge: python project.py --option marge --files path/to/your/file1.pdf path/to/your/file2.pdf
        """,
    )

    parser.add_argument(
        "--option",
        required=True,
        choices=["rev", "split", "marge"],
        help="Choice [rev, split, marge]",
    )
    parser.add_argument("--files", help="Path to the PDF file(s)", nargs="+")
    parser.add_argument(
        "--from_", type=int, help="Starting page number for split (1-based index)"
    )
    parser.add_argument(
        "--to", type=int, help="Ending page number for split (1-based index)"
    )

    args = parser.parse_args()

    files_name: list = args.files

    if args.option == "rev":
        # Reverse the PDF
        try:
            pdf_reverse(files_name)
        except ValueError as e:
            sys.exit(f"Error: {e}")

    elif args.option == "split":
        # Split the PDF
        if args.from_ is None or args.to is None:
            sys.exit("Error: --from and --to arguments are required for split option")

        try:
            if len(files_name) == 1:
                pdf_split(files_name[0], args.from_, args.to)
            else:
                sys.exit("Error: Must be one file")
        except ValueError as e:
            sys.exit(f"Error: {e}")

    elif args.option == "marge":
        # Merge the PDFs
        pdf_marge(files_name)


if __name__ == "__main__":
    # Call the main function
    main()
