from flask import Flask, render_template, request
import os
import PyPDF2
import docx  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return ""

@app.route('/')
def resume_Match():
    return render_template('index.html')

@app.route("/matcher", methods=['GET', 'POST'])
def matcher():
    if request.method == "POST":
        job_description = request.form.get("job-description")
        resume_files = request.files.getlist('resumes')
        
        resumes = []
        for resume in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(filename)
            resumes.append(extract_text(filename))
        
        if not resumes or not job_description:
            return render_template("index.html", message="Please upload at least one resume and enter a job description.")

        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()
        job_description_vector = vectors[0]
        resume_vectors = vectors[1:]

        similarity = cosine_similarity([job_description_vector], resume_vectors)[0]

        top_match_index = similarity.argmax()
        top_match_score = similarity[top_match_index]

        return render_template('index.html', message=f"Top matching resume is Resume {top_match_index + 1} with a score of {top_match_score:.2f}")

    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
