from flask import Flask, render_template, request
import pymongo
from datetime import datetime
from werkzeug.utils import redirect

app=Flask(__name__)

#app.config["MONGO_URI"] = "mongodb+srv://thiru:thirusibi@irttmemories-aegwt.mongodb.net/irttmemories?retryWrites=true&w=majority"
#mongo = PyMongo(app)

#client =pymongo.MongoClient("mongodb+srv://thiru:thirusibi@irttmemories-aegwt.mongodb.net/irttmemories?retryWrites=true&w=majority")
#db = client['irttmemories']
#collection = db['post']

client=pymongo.MongoClient("mongodb+srv://thiru:thiru@irttmemories-aegwt.mongodb.net/irttmemories?retryWrites=true&w=majority")
db = client['irttmemories']
collection = db['post']


@app.route('/')
def home():
    return render_template('head.html')

@app.route('/post',methods=['POST','GET'])
def post():
    if request.method=='POST':
        now = datetime.now()
        dict={}
        pname=request.form['PostName']
        dict['name']=pname
        pdept = request.form['PostDept']
        dict['dept'] = pdept
        pyear = request.form['PostYear']
        dict['year'] = str(pyear)
        ptitle = request.form['PostTitle']
        dict['title']=ptitle
        pmemories = request.form['PostMemories']
        dict['memories']=pmemories
        dict['time'] = now

        collection.insert_one(dict)
        return redirect('/read')
    else:
        return render_template('post.html')



@app.route('/read',methods=['POST','GET'])
def read():
    if request.method == 'POST':
        year=request.form['Search']
        url='/read/'+str(year)
        return redirect(url)
    else:
        names=collection.find().sort([("time", -1)])
        return render_template('read.html',names=names)

@app.route('/read/<value>')
def readYear(value):
    names=collection.find({ 'year' : value })
    return render_template('Search.html',names=names)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)