# 📄 PDF Editing Tools – Final Project (CS50P)

## 🎥 Video Demo
[🔗 Click here to watch the video](https://your-video-url.com) *(Replace this with your actual link)*

---

## 📌 Overview

This project provides a set of tools for manipulating PDF files through the command line using Python.  
It was developed as the **final project** for Harvard’s [CS50’s Introduction to Programming with Python](https://cs50.harvard.edu/python/2022/).

The tool includes the following features:

- 🔄 **Reverse PDF**: Reverse the order of PDF pages.
- ✂️ **Split PDF**: Extract a range of pages from a PDF file.
- ➕ **Merge PDFs**: Merge multiple PDF files into one document.

---

## ✨ Features

| Feature       | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| 🔄 PDF Reverse | Reverses the order of pages in the PDF. Pages 1,2,3 → 3,2,1                |
| ✂️ PDF Split   | Extracts a specific range of pages from the PDF (e.g., pages 2–5)          |
| ➕ PDF Merge   | Combines multiple PDF files into a single file in the order you specify     |

Each output is saved to its corresponding folder in the `output/` directory.

---

## 🛠 Installation

To install and run the project locally, follow these steps:

```bash
# 1. Clone the repository
git clone https://github.com/Mohamed1khaled2/pdfEditing.git

# 2. Navigate to the project directory
cd pdfEditing

# 3. Install required dependencies
pip install -r requirements.txt
