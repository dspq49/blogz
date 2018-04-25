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
def validate_blog():
    #client should see form for a new blog post
    #form should have 2 fields (title/body) and submit button
    #if fields are blank then client should receive error message
    #if valid, information should be accepting in database,and client should be redirected to
    #main page
    #submit is post request 
    #if get req client should see form for new post

    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']
        
        notitle_error = ""
        nobody_error = ""
        

        if title == "":
            notitle_error = "Please enter a title"
        if body == "":
            nobody_error = "Please enter words in body"
        
        if notitle_error or nobody_error:
         
            return render_template('newpost.html', title=title, body=body, notitle_error=notitle_error, nobody_error=nobody_error)
       
        else:
            new_blog = Blog(title, body)      
            db.session.add(new_blog)
            db.session.commit()
        
            return redirect('/blogs') 

    return render_template('newpost.html')

#First, set up the blog so that the "add a new post" form and the blog listings are on the same page, 
# as with Get It Done!, 
# and then separate those portions into separate routes, handler classes, and templates. 
# For the moment, when a user submits a new post, redirect them to the main blog page.
@app.route('/blogs', methods=['GET'])   
def all_blogs():
    #when people go to blogs, they should see all blogs 
    #GET requests only
    #id = request.args.get('id')

    #if not id :
    blogs = Blog.query.all()
    return render_template('blogs.html', title="Build A Blog", blogs=blogs)

    #else:
     #   id = str(id)
      #  blogs = Blog.query.get(id)
       #return render_template('onepost.html', title="Single Entry", blogs=blogs)
        


@app.route('/')
def index():
    #index function doesn't show anything, redirects to blogs route 
    return redirect('/blogs')


if __name__ == "__main__":
    app.run()