
# 📄 PDF Editing Tools – CS50P Final Project

## 🎥 Video Demo

**[👉 Click here to watch the demo](https://your-video-link.com)**  
*(Replace with your actual YouTube or upload link)*

---

## 👋 Introduction

This project was created as the **Final Project** for [CS50’s Introduction to Programming with Python](https://cs50.harvard.edu/python/2022/).

It is a Python-based command-line tool for manipulating PDF files.  
It allows users to:

- 🔄 **Reverse** the order of pages in a PDF
- ✂️ **Split** a PDF into a specified page range
- ➕ **Merge** multiple PDFs into one

---

## ✅ Project Features

| Feature        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| 🔄 Reverse PDF | Reverses the order of all pages in the selected PDF file                    |
| ✂️ Split PDF   | Extracts a specific range of pages from a PDF file                          |
| ➕ Merge PDFs   | Combines multiple PDF files into a single one, in the order you specify     |

Each processed PDF is saved to its respective folder under `output/`.

---

## 🛠 How to Install

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

## 🚀 How to Run the Program

### 🔄 Reverse a PDF
```bash
python project.py --option rev --files path/to/file1.pdf path/to/file2.pdf
```
→ Reversed PDF files are saved in `output/reverse/`.

---

### ✂️ Split a PDF
```bash
python project.py --option split --files path/to/file.pdf --from_ 2 --to 5
```
→ Extracted pages saved in `output/split/`.

---

### ➕ Merge Multiple PDFs
```bash
python project.py --option marge --files file1.pdf file2.pdf file3.pdf
```
→ Merged file saved in `output/marge/`.

---

## 📸 Screenshots

> 🔽 **Replace the below placeholders with actual screenshots before final submission**

### 📍 Command-line Interface Example
![CLI Screenshot Placeholder](screenshots/cli-example.png)

---

### 📍 Output Folder Example
![Output Folder Placeholder](screenshots/output-folder.png)

---

### 📍 Reversed PDF Preview
![Reversed PDF Placeholder](screenshots/reversed-pdf.png)

---

## 🧪 Testing

Run unit tests using:

```bash
pytest
```

Tests are defined in `test_project.py`.

---

## 🗂 Project Structure

```
pdfEditing/
├── project.py            # Main functionality
├── test_project.py       # Unit tests
├── README.md             # Documentation
├── requirements.txt      # Dependencies
└── output/
    ├── reverse/
    ├── split/
    └── marge/
```

---

## 📧 Contact

Created by **Mohamed Khaled**  
📩 mohamedkhaledabdelwhap@gmail.com

---

## 🙌 Final Notes

This project demonstrates my ability to:
- Work with files and file systems in Python
- Parse command-line arguments using argparse
- Use external libraries (e.g., PyPDF2)
- Write and run unit tests using Pytest
- Document and present a complete Python project

Thank you for reviewing my project! 🙏
