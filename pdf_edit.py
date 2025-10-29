from pathlib import Path
import argparse
import os
import sys

from pypdf import PdfReader, PdfWriter


class PDFEdit:
    def __init__(self, output_dir: str | None = None):
        """
        Initialize a PDFEdit instance.
        If output_dir is provided, use it as the output directory for processed files.
        Otherwise, use the user's Documents/PDFEdit_output directory.
        """
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Works correctly when running as an executable or as a .py file
            # Path to the user's Documents folder
            documents_dir = Path.home() / "Documents"
            # Directory where the program will save output files
            self.output_dir = documents_dir / "PDFEdit_output"
        # Create the folder if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def check_pdf_extension(self, name_files: list[str]) -> tuple:
        """
        Check that all files in the list exist and have a .pdf extension.
        Raises ValueError if a file does not have a .pdf extension.
        Raises FileNotFoundError if a file does not exist.
        Returns True if all files are valid.
        """
        for file in name_files:
            _, ext = os.path.splitext(file)
            if ext.lower() != ".pdf":
                return (False, f"The file '{file}' does not have a .pdf extension.")
            if not os.path.exists(file):
                return (False, f"The file '{file}' does not exist.")
        return (True, "")

    def __search_is_name_valid(self, name: str, path: str) -> str:
        """
        Check if a file name already exists in the given path.
        If it does, append 'copy-<n>' to the file name to avoid overwriting.
        Returns a valid file name as a string.
        """
        count = 0
        for file in os.listdir(path):
            if name == file or name.replace(".pdf", f"copy-{count}.pdf") == file:
                count += 1
        if count == 0:
            return name
        return name.replace(".pdf", f"copy-{count}.pdf")

    def __save_file_as_pdf(self, process: str, name: str, writer: PdfWriter) -> None:
        """
        Save a PDF file using the provided PdfWriter object.
        The output directory is determined by the process type ('rev', 'split', 'marge').
        The file name is made unique if needed to avoid overwriting.
        """
        match process:
            case "rev":
                output_dir = os.path.join(self.output_dir, "reverse")
                os.makedirs(output_dir, exist_ok=True)
            case "split":
                output_dir = os.path.join(self.output_dir, "split")
                os.makedirs(output_dir, exist_ok=True)
            case "marge":
                output_dir = os.path.join(self.output_dir, "marge")
                os.makedirs(output_dir, exist_ok=True)
            case _:
                output_dir = os.path.join(self.output_dir, "")
        name_file_saved = self.__search_is_name_valid(name, output_dir)
        with open(os.path.join(output_dir, name_file_saved), "wb") as new_file:
            writer.write(new_file)
            writer.close()

    def pdf_reverse(self, original_files: list[str]) -> bool:
        """
        Reverse the pages of one or more PDF files.
        For each file, creates a new PDF with pages in reverse order and saves it to the output directory.
        Returns True if successful. Raises FileNotFoundError if a file is missing.
        """
        if self.check_pdf_extension(original_files)[0]:
            reverse_names = [f"reverse-{os.path.basename(f)}" for f in original_files]
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
                    page_obj = reader.pages[page]
                    # Add the page to the writer
                    writer.add_page(page_obj)
                    # Add the outline item (bookmark) to the writer
                    if len(reader.outline) != 0:
                        writer.add_outline_item(
                            reader.outline[page].title, page_number=page_number
                        )
                        page_number += 1
                # Write the reversed pages to a new file
                self.__save_file_as_pdf(
                    name=reverse_names[index], process="rev", writer=writer
                )
            return True
        else:
            return self.check_pdf_extension(original_files)

    def pdf_split(self, original_files: list[str], from_: int, to: int) -> None:
        """
        Split multiple PDF files into new PDFs containing pages from 'from_' to 'to' (inclusive).
        GUI-friendly version: handles all files separately, skips invalid ones, and never raises exceptions.
        """
        # ✅ Check extensions first

        if self.check_pdf_extension(original_files)[0]:

            # ✅ Validate range
            if from_ > to:
                print("⚠️ Invalid range: 'from_' must be less than or equal to 'to'")
                return

            writer = None
            # ✅ Loop through all files independently
            for file in original_files:
                try:
                    reader = PdfReader(file)
                except Exception as e:
                    print(f"❌ Cannot open file '{file}': {e}")
                    continue  # Skip this file, go to next one

                total_pages = len(reader.pages)
                if total_pages == 0:
                    print(f"⚠️ Skipping empty file: {file}")
                    continue

                # ✅ Adjust 'to' if it's bigger than total pages
                actual_to = min(to, total_pages)

                # ✅ Skip if from_ is out of range
                if from_ < 1 or from_ > total_pages:
                    print(
                        f"⚠️ Invalid 'from_' value for '{file}'. It has only {total_pages} pages."
                    )
                    continue

                # ✅ Create a fresh writer for each file
                writer = PdfWriter()
                for i in range(from_ - 1, actual_to):
                    try:
                        writer.add_page(reader.pages[i])
                    except IndexError:
                        print(f"⚠️ Page {i+1} is out of range for file: {file}")
                        break

                # ✅ Save file safely
                new_name = f"split-{from_}-{actual_to}-{os.path.basename(file)}"
                self.__save_file_as_pdf(name=new_name, writer=writer, process="split")
                print(f"✅ Split file saved as: {new_name}")
            return writer
        else:
            return self.check_pdf_extension(original_files)

    def pdf_marge(self, pdfs: list[str]) -> PdfWriter:
        """
        Merge multiple PDF files into one output PDF.
        The merged file is saved to the output directory as 'merger-output.pdf'.
        Returns a PdfWriter object for the merged PDF.
        Raises ValueError if fewer than two files are provided or a file is missing.
        """
        if self.check_pdf_extension(pdfs)[0]:
            if len(pdfs) < 2:
                raise ValueError("less than two file")
            # Create a PdfWriter object to write the merged PDF
            merger = PdfWriter()
            # Iterate over the list of PDF files
            for pdf in pdfs:
                # check if the file exists
                try:
                    # Append each PDF file to the PdfWriter object
                    merger.append(open(pdf, "rb"))
                except FileNotFoundError:
                    sys.exit(f"This is File Not found {pdf}")
            # Define the output directory and file path
            self.__save_file_as_pdf(
                process="marge", name="merger-output.pdf", writer=merger
            )
            # Return the PdfWriter object containing the merged PDF
            return merger
        else:
            return self.check_pdf_extension(pdfs)


def main() -> None:
    """Main function to reverse the pages of example PDF files, split PDF files, or merge PDF files."""

    parser = argparse.ArgumentParser(
        description="Reverse the pages of PDF files, split pages, or merge PDF files",
        usage=(
            "You can split pdf, You can reverse pdf, You can merge pdf\n"
            "Running like this:\n"
            "for reverse: python project.py --option rev --files path/to/your/file.pdf\n"
            "for split: python project.py --option split --files path/to/your/file.pdf --from_ num1 --to num2\n"
            "for merge: python project.py --option marge --files path/to/your/file1.pdf path/to/your/file2.pdf"
        ),
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

    pdf_editing = PDFEdit()

    if args.option == "rev":
        # Reverse the PDF
        try:
            pdf_editing.pdf_reverse(files_name)
        except ValueError as e:
            sys.exit(f"Error: {e}")

    elif args.option == "split":
        # Split the PDF
        if args.from_ is None or args.to is None:
            sys.exit("Error: --from and --to arguments are required for split option")

        try:
            print(files_name)
            if len(files_name) == 1:
                pdf_editing.pdf_split(files_name, args.from_, args.to)
            else:
                sys.exit("Error: Must be one file")

        except ValueError as e:
            sys.exit(f"Error: {e}")

    elif args.option == "marge":
        # Merge the PDFs
        pdf_editing.pdf_marge(files_name)


if __name__ == "__main__":
    main()
