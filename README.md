# Final Project 📄

## Project Overview
This project is designed to provide a set of tools for manipulating PDF files. It aims to simplify common PDF operations such as reversing the order of pages, splitting a PDF into smaller parts, and merging multiple PDFs into a single document.

#### Video Demo: [Add your video URL here] 🎥
#### Description:
This project includes three main functionalities:

1. **PDF Reverse** 🔄: This feature allows users to reverse the order of pages in a PDF file. For example, if a PDF has pages 1, 2, 3, and 4, the reversed PDF will have pages 4, 3, 2, and 1. This can be useful for creating mirrored versions of documents or for specific printing requirements. The resulting PDF will be saved in the `output/reverse` folder.

2. **PDF Split** ✂️: This feature enables users to split a PDF file into smaller parts based on a specified range of pages. For instance, if a user wants to extract pages 1 to 5 from a 10-page PDF, this tool will create a new PDF containing only those pages. This is particularly useful for extracting specific sections of a document for sharing or printing. The resulting PDF will be saved in the `output/split` folder.

3. **PDF Merge** ➕: This feature allows users to merge multiple PDF files into a single document. Users can specify a list of PDF files, and the tool will combine them in the specified order. This is useful for consolidating multiple documents into one for easier management and distribution. The resulting PDF will be saved in the `output/marge` folder.

## Features ✨
- **PDF Reverse** 🔄: Reverse the pages of a PDF file.
- **PDF Split** ✂️: Split a PDF file into a new PDF file containing pages from a specified range.
- **PDF Merge** ➕: Merge multiple PDF files into one.

## Installation 🛠️
To install and run this project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/Mohamed1khaled2/pdfEditing.git
    ```
3. Navigate to the project directory:
    ```sh
    cd pdfEditing
    ```
4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage 🚀
To use the functionalities provided by this project, you can run the following commands:

### Reverse PDF 🔄
- `hint 💡`: You can add alot of file not only one.

```sh
python project.py --option rev --files path/to/your/file.pdf
```

### Split PDF ✂️
```sh
python project.py --option split --files path/to/your/file.pdf --from_ num1 --to num2
```

### Merge PDF ➕
```sh
python project.py --option marge --files path/to/your/file1.pdf path/to/your/file2.pdf
```

## Testing 🧪
To run the tests for this project, use the following command:
```sh
pytest
```

## Project Structure 📁
- `project.py`: Contains the main functionality for reversing, splitting, and merging PDF files.
- `test_project.py`: Contains the test cases for the functionalities provided in `project.py`.
- `README.md`: This file, providing an overview and instructions for the project.

## Contact 📧
For any questions or feedback, please contact [your email address].
