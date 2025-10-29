# PDF Editing Tools – CS50P Final Project

## Video Demo

👉 [Watch the demo video](https://youtu.be/I7-o5Cb2-xk)  
*(Replace with your actual YouTube or upload link)*

---

## Introduction

This project is my submission for [CS50’s Introduction to Programming with Python](https://cs50.harvard.edu/python/project/).

It is a Python-based tool (CLI and GUI) for manipulating PDF files. You can:

- Reverse the order of pages in a PDF
- Split a PDF into a specified page range
- Merge multiple PDFs into one

---

## Features

- **Reverse PDF**: Reverses the order of all pages in the selected PDF file(s)
- **Split PDF**: Extracts a specific range of pages from a PDF file
- **Merge PDFs**: Combines multiple PDF files into a single one, in the order you specify
- **GUI**: User-friendly graphical interface (run with `project.py`)
- **CLI**: Command-line interface for advanced users
- **Unit Tests**: Comprehensive test suite using pytest

All processed PDFs are saved in the `output/` subfolders: `reverse/`, `split/`, `marge/` (or in your custom output directory).

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/pdfEditing.git
    ```
2. Navigate into the project directory:
    ```bash
    cd pdfEditing
    ```
3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### Command-Line Interface (CLI)

**Reverse a PDF:**
```bash
python project.py --option rev --files path/to/file1.pdf path/to/file2.pdf
```
Output: reversed PDFs in `output/reverse/`

**Split a PDF:**
```bash
python project.py --option split --files path/to/file.pdf --from_ 2 --to 5
```
Output: split PDF in `output/split/`

**Merge PDFs:**
```bash
python project.py --option marge --files file1.pdf file2.pdf file3.pdf
```
Output: merged PDF in `output/marge/`

### Graphical User Interface (GUI)

Run the GUI with:
```bash
python project.py
```
You can select files, choose operations, and see error messages in a user-friendly window.

---

## Testing

Run all unit tests using:
```bash
pytest
```
Tests are defined in `test_project.py` and cover all core features and edge cases.

---

## File Structure

```
pdfEditing/
├── pdf_edit.py        # Core PDF logic (reverse, split, merge)
├── gui_.py            # GUI interface (CustomTkinter)
├── project.py         # GUI entry point
├── test_project.py    # Unit tests (pytest)
├── requirements.txt   # Dependencies
├── README.md          # Documentation
└── output/            # Output folders (created automatically)
     ├── reverse/
     ├── split/
     └── marge/
```

---

## Contact

Created by **Mohamed Khaled**  
📩 mohamed.k.code@gmail.com

---

## Notes

- This project demonstrates file handling, argument parsing, GUI programming, and unit testing in Python.
- All code is original and written for CS50P.
- For any questions or issues, please contact me at the email above.

Thank you for reviewing my project!

---

## Special Thanks

I would like to express my sincere gratitude to Harvard University and all the professors and staff behind the CS50 course for making this high-quality education available for free to learners around the world. Your efforts and generosity are truly appreciated!
