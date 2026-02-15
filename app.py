from flask import Flask, request, render_template
import os
import tempfile
from ATSFreindly import is_ats_friendly

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    jobdesc = ''
    if request.method == 'POST':
        jobdesc = request.form.get('jobdesc', '')
        file = request.files.get('resume')
        if not file or not jobdesc:
            result = 'Please provide both a job description and a resume file.'
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as tmp:
                file.save(tmp.name)
                tmp_path = tmp.name
            try:
                ats_friendly = is_ats_friendly(tmp_path, jobdesc)
                result = f'<h3>ATS Friendly: {"Yes" if ats_friendly else "No"}</h3>'
            except Exception as e:
                result = f'<b>Error:</b> {str(e)}'
            finally:
                os.remove(tmp_path)
    return render_template('index.html', result=result, jobdesc=jobdesc)

if __name__ == '__main__':
    app.run(debug=True)
