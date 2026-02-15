# ATS Resume Checker

This Python script is designed to evaluate whether a resume is **ATS (Applicant Tracking System)-friendly** by analyzing its content and formatting. It checks for important keywords, the presence of required sections, and common formatting elements that would make a resume compatible with ATS systems.

## Features

- **File Compatibility**: Supports `.docx` and `.pdf` file formats for reading resumes.
- **Keyword Matching**: Compares the resume text with a job description to identify matching keywords, bigrams, and trigrams.
- **Formatting Check**: Evaluates common ATS-friendly formatting such as bullet points, section headers, and required sections like "Work Experience", "Education", etc.
- **ATS-Friendliness Score**: Determines whether the resume meets certain thresholds for keyword matching and formatting to be considered ATS-friendly.

## Requirements

To run this script, you will need the following Python libraries:

- nltk - for natural language processing tasks like stopword removal.
- spacy - for semantic analysis (though the code uses a basic model).
- docx - to read `.docx` files.
- pdfplumber` - to extract text from `.pdf` files.
- sklearn - for text vectorization (not directly used in the current implementation but could be expanded for advanced matching).
- numpy - for numerical operations.

### Install Required Libraries

You can install the required libraries using pip. Run the following command in your terminal:

pip install nltk spacy python-docx pdfplumber scikit-learn numpy


Additionally, you'll need to download the stopwords for NLTK and the spaCy English model.

python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm


## How It Works

The script performs several tasks in sequence:

### 1. **Reading Resume Files**:
- For .docx files, it uses the python-docx library to extract the text.
- For .pdf files, it uses the pdfplumber library to extract the text from the pages.

### 2. **Text Cleaning**:
- Non-alphabetical characters (such as punctuation) are removed.
- Extra spaces are compressed into single spaces.
- The text is converted to lowercase to ensure uniformity during comparisons.

### 3. **Keyword Matching**:
- The script compares the resume text to the job description for keyword matches. It looks for:
  - Single word matches.
  - Bigrams (two consecutive words) and trigrams (three consecutive words).
- Stopwords (e.g., "the", "and") are removed from both the resume and job description to focus on meaningful words.

### 4. **Formatting Check**:
- The script checks for the presence of common ATS-friendly formatting elements, such as:
  - Bullet points (`-`, `*`, or `•`).
  - Required sections (e.g., "Work Experience", "Education", "Skills").
  - Bold section headers (for `.docx` files).

### 5. **ATS-Friendliness Evaluation**:
- The script computes an **ATS-friendliness score** based on:
  - **Keyword matching**: If fewer than 50% of the job description’s keywords are matched in the resume, it gives a warning.
  - **Formatting**: If the resume is missing important sections or does not have proper formatting (e.g., bullet points, section headers), it may not be considered ATS-friendly.
- The final result is displayed, along with specific warnings if any criteria are not met.

## How to Use

1. **Prepare your job description and resume file**:
   - The job description should be a plain text string.
   - The resume should be either a `.docx` or `.pdf` file.

2. **Run the Script**:

   - Set the job description and resume file path in the script as follows:

     job_description = """Senior Software Engineer with experience in Python, JavaScript, HTML, CSS, C++, SQL, Bootstrap, TailwindCSS."""
     resume_file_path = "path_to_your_resume.pdf"  # Replace with the full path to your resume file


3. **Execute the Script**:
   - Run the script in your terminal or IDE:

     python ats_resume_checker.py


4. **View the Results**:
   - The script will print:
     - **Matching Keywords**: Lists the keywords that were found in the resume that match the job description.
     - **Formatting Score**: Indicates how well the resume is formatted according to ATS-friendly standards (based on bullet points, section headers, etc.).
     - **ATS-Friendly Status**: Whether the resume is likely ATS-friendly or not.

   Example output:

   --- ATS Resume Analysis ---
   Matching keywords: python, javascript, html, css, sql
   Formatting score: 4/5 sections found (3 of 5 required sections).
   ATS Friendly: Yes


## Example

Here is a minimal example showing how the script might be used:

### `example.py`


# Import the function from the script
from ats_resume_checker import is_ats_friendly

# Sample job description text
job_description = """
    Senior Software Engineer with experience in Python, JavaScript, HTML, CSS, C++, SQL, Bootstrap, TailwindCSS.
    Expertise in creating high-performance, scalable systems.
"""

# Path to the resume file (replace with your actual file path)
resume_file_path = "path_to_resume.pdf"

# Check if the resume is ATS-friendly
is_ats_friendly(resume_file_path, job_description)


### Sample Job Description:

Senior Software Engineer with experience in Python, JavaScript, HTML, CSS, C++, SQL, Bootstrap, TailwindCSS.


### Sample Resume (Resume.pdf or Resume.docx):
You can use your own resume in `.pdf` or `.docx` format to test the script.

## Customization

### 1. **Modify Keywords/Sections**:
- The job description is passed as a string, and keywords are matched based on the resume's content. You can modify the keyword matching logic or the job description to suit your needs.
- The required sections like "Work Experience", "Education", and "Skills" are pre-defined. You can change this list to customize which sections the script looks for in the resume.

### 2. **Advanced Matching**:
- The script currently uses simple word and n-gram matching. You could enhance this by integrating more advanced NLP techniques, such as word embeddings (Word2Vec, GloVe) or transformer-based models (BERT, GPT) for better semantic understanding.

### 3. **Improving Formatting Checks**:
- The script checks for basic formatting such as bullet points and section headers. To enhance this, you could add more specific formatting checks (e.g., checking for proper font sizes, headers, etc.).

## Limitations

- **PDF Parsing**: The script may not work well with complex PDF layouts that include tables, images, or embedded fonts. The text extraction might lose some formatting, especially in scanned or OCR-based PDFs.
- **Basic Keyword Matching**: The script uses simple keyword and n-gram matching, which might not account for synonyms or variations in phrasing (e.g., "JavaScript" vs. "JS").
- **ATS Variability**: Different ATS software may have varying requirements. The script uses basic formatting and keyword checks, but some ATS systems may require more specialized formatting or keyword usage.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Conclusion

This script is a simple and effective tool for assessing the ATS-friendliness of resumes by checking for matching keywords and essential formatting. While it provides basic insights into how a resume might perform in an ATS, you can enhance and customize it further based on specific needs or ATS requirements.
