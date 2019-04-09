from flask import Flask,render_template,request,flash
from ScoreRecorder import Data

# 上传文件用
import os
from flask import redirect,url_for
from werkzeug.utils import secure_filename

# request can deal post.
# flash 可以动态传递消息 --> 需要对内容加密，设置scret_key

app=Flask(__name__)
app.secret_key="akjdf89u2389rinfaj __kjasdf89--"
db=Data()

def showScores(p):
    scores={}
    for key in p.scores:
        if p.scores[key]!=None:
            if key[0]=='w':
                scores['第%s周' % key[1]]=p.scores[key]
            if key[0]=='t':
                scores['小测%s' % key[1]]=p.scores[key]
            if key[0]=='m':
                scores['期中  ']=p.scores[key]
            if key[0]=='f':
                scores['期末  ']=p.scores[key]
    return scores

# Need to explicitly specify the method
@app.route('/', methods=['GET','POST'])
def index():
    if request.method=="POST":
        userID=request.form.get('userID')
        userName=request.form.get('userName')
        try:
            p=db.getPerson(userID)
            if p.name != userName:
                raise KeyError
        except KeyError:
            flash("错误的学号或姓名")
        else:
            return render_template('index.html',person=p,scores=showScores(p))
        
    return render_template('index.html',person=None,scores=None)

# 准备上传文件
# UPLOAD_FOLDER='/home/ubuntu/project/scoreFlask'
UPLOAD_FOLDER='C:\\Users\\56256\\Documents\\GitHub\\Tools\\ScoreRecorder'
ALLOWED_FILE=set(['Data.bak','Data.dat','Data.dir'])
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "no push files"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file.filename in ALLOWED_FILE:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "upload success"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__=="__main__":
    app.config['DEBUG']=True
    app.run()