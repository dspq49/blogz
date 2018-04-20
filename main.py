from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mom@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
       

    def __repr__(self):
        return '<Blog %r>' % self.title % self.body




@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        
        blog_title = request.form['title']
        new_title = Blog(blog_title)
        blog_body = request.form['body']
        new_body = Blog(blog_body)
        new_blog = Blog(new_title, new_body)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('newpost.html',title="Build A Blog!", body=body) 
       
    blogs = Blog.query.all()
    id = request.args.get('id')
    
    if request.method == 'GET':
        return render_template('blogs.html')


@app.route('/', methods=['POST'])   
def new_posting(title, body):

    new_post = ""

    if len(title) > 0 and len(body) > 0:
        #new_post = 
        return render_template('newpost.html', new_post)
        #i need to render template with the new information of title and body
       


        #blogs.append(blog)
        
        #posted_name = request.form['posted']
        #new_post = Blog(posted_name)
           
    #blogs.query.filter_by(completed=False).all()
    #completed_posts = Blog.query.filter_by(completed=True).all()
    


#app.secret_key = 'asdf8uej!'

if __name__ == "__main__":
    app.run()