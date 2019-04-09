from flask import Flask,render_template,request,flash
from ScoreRecorder import Data

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
            flash("错误的学号或姓名.")
        else:
            return render_template('index.html',person=p,scores=showScores(p))
        
    return render_template('index.html',person=None,scores=None)

if __name__=="__main__":
    app.config['DEBUG']=True
    app.run()