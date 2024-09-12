from flask import Flask, render_template,request
import os
import PyPDF2
app = Flask(__name__)
import docx2text
app.config['UPLOAD_FOLDER']='uploads/'
def extract_text_from_pdf(file_path):

        text= ""
        with open (file_path,'rb') as file:
            reader= PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = text +page.extract_text(page)
            return text 



def extract_text_from_docx(file_path):
    return docx2tcxt.process(file_path)
    
def extract_text_from_txt(file_path):
    with open (file_path,'rb',encoding='utf-8') as file:
        reader= PyPDF2.PdfReader(file)
        return file.read
    
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif  file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
@app.route('/')
def resume_Match():
    return render_template('index.html')
@app.route("/matcher", methods=['GET','POST'])
def matcher():
    if request.methods =="POST":
        job-description=request.form.get("job-description")
        resume_file= request.form.getlist('resumes')
        resumes=[]
        for i in resume_file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'],i.filename)
            resume_file.save(filename)
            resumes.append(extract_text.filename)
            


if __name__ == "__main__":
    app.run(debug=True)
