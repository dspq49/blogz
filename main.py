from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mom@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'asdf8uej!'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
       

    def __repr__(self):
        return '<Blog %r>' % self.title % self.body





@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        
        blog_title = request.form['title']
        blog_body = request.form['body']
        
        nobody_error = ""
        notitle_error = ""

        if blog_title == "":
            notitle_error = "Please enter a title"

        if body == "":
            nobody_error = "Please enter words in body"
            return render_template('newpost.html', blog_title =blog_title, blog_body=blog_body,
                notitle_error=notitle_error, nobody_error = nobody_error)
       
       
        else:
            new_blog = Blog(blog_title, blog_body)      
            db.session.add(new_blog)
            db.session.commit()
        
        
            return redirect('/blogs?blog_id=' + str(new_blog.blog_id))
    
    else: 
        return render_template('newpost.html', title="", body="", notitle_error="", nobody_error="")
    
    
    if request.method == 'GET':
        return render_template('blogs.html')


@app.route('/blogs', methods=['GET'])   
def mainpage():
    
    id = request.args.get('id')

    if id == '':
        blogs = Blog.query.all()
        return render_template('blogs.html', title="Build A Blog", blogs=blogs)

    else:
        id = str(id)
        blogs = Blog.query.get(id)
        return render_template('onepost.html', title="Single Entry", blogs=blogs)
        
        #, blog_title=blogs.blog_title, body=blogs.blog_body)
      

@app.route('/')
def pointtoblogs():
    return redirect('/blogs')


if __name__ == "__main__":
    app.run()