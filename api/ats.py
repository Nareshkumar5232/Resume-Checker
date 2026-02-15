import os
import tempfile
import re
from docx import Document
from pypdf import PdfReader

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.lower()

def generate_ngrams(text, n=2):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

def read_docx(file_path):
    doc = Document(file_path)
    return '\n'.join(p.text for p in doc.paragraphs)

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text() or ''
        text += '\n' + page_text
    return text

def score_resume(resume_text, jobdesc_text):
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(jobdesc_text)

    resume_words = set(resume_clean.split())
    job_words = set(job_clean.split())

    resume_bigrams = set(generate_ngrams(resume_clean, 2))
    job_bigrams = set(generate_ngrams(job_clean, 2))

    matches = resume_words.intersection(job_words)
    matches.update(resume_bigrams.intersection(job_bigrams))

    matched = len(matches)
    total = max(1, len(job_words))
    keyword_ratio = matched / total

    formatting_score = 0
    if '-' in resume_text or '*' in resume_text or '•' in resume_text:
        formatting_score += 1
    sections = ['work experience', 'education', 'skills', 'certifications', 'summary']
    sections_found = sum(1 for s in sections if s in resume_clean)
    formatting_score += sections_found

    ats = (keyword_ratio >= 0.5) and (formatting_score >= 3)
    return {
        'matched_keywords_count': matched,
        'total_job_keywords': total,
        'keyword_ratio': keyword_ratio,
        'formatting_score': formatting_score,
        'sections_found': sections_found,
        'ats_friendly': ats,
        'matches': list(matches)[:100]
    }

def handler(request):
    try:
        jobdesc = request.form.get('jobdesc', '')
        file = request.files.get('resume')
        if not jobdesc or not file:
            return ('<b>Please provide both a job description and a resume file.</b>', 400, {'Content-Type': 'text/html'})

        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        if suffix.lower() == '.pdf':
            resume_text = read_pdf(tmp_path)
        elif suffix.lower() == '.docx':
            resume_text = read_docx(tmp_path)
        else:
            os.unlink(tmp_path)
            return ('<b>Unsupported file type. Use .pdf or .docx</b>', 400, {'Content-Type': 'text/html'})

        result = score_resume(resume_text, jobdesc)
        os.unlink(tmp_path)

        html = f"""
        <h3>ATS Friendly: {'Yes' if result['ats_friendly'] else 'No'}</h3>
        <p>Matched keywords: {result['matched_keywords_count']} / {result['total_job_keywords']} (ratio: {result['keyword_ratio']:.2f})</p>
        <p>Formatting score: {result['formatting_score']} (sections found: {result['sections_found']})</p>
        <p>Top matches: {', '.join(result['matches'][:20])}</p>
        <p><a href="/">Back</a></p>
        """
        return (html, 200, {'Content-Type': 'text/html'})

    except Exception as e:
        return (f'<b>Error:</b> {str(e)}', 500, {'Content-Type': 'text/html'})
