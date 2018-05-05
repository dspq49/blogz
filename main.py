from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:***@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'asdf8uej!'

class Blog(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id

    def __repr__(self):
        return '<Blog %r>' % self.title % self.body 


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True) 
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref='user')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.username % self.password





@app.before_request
def login_required():
    routes = ['login', 'base', 'index', 'signup', 'logout', 'all_blogs']
    if request.endpoint not in routes and 'user' not in session:
        return redirect('/login')



@app.route('/')
def index():
    #index function doesn't show anything, redirects to blogs route 
    users = User.query.all()
    return render_template('index.html', users=users)




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        error_message = ''
        if username and user.password == password:
            session ['user'] = user.id
            return redirect('/newpost')
        else:
            if username and user.password != password:
                error_message = 'Bad Password'
            elif not user:
                error_message = 'Username Does Not Exist'
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_error = ''
        password_error = ''
        verify_password_error = ''

        if username == '':
            username_error = 'Username Required'

        else:
            if len(username) < 3:
                username_error = 'Username Cannot Be Less than 3 Characters'

        if password == '':
            password_error = 'Password Required'
        else:
            if len(password) < 3: 
                password_error = 'Password Cannot Be Less than 3 Characters'
                password = ''


        if verify == '':
            verify_password_error = 'Verify Password Required'
        else:
            if verify != password:
                verify_password_error = 'Passwords Do Not Match'
                verify = ''

        if not username_error and not password_error and not verify_password_error:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['user'] = new_user.id
                return redirect('/newpost')
            else:
                username_error = 'Username Already Exists'
            
            return render_template('signup.html', username=username, username_error=username_error)
        else:
            return render_template('signup.html', username_error = username_error, password_error = password_error, 
            verify_password_error = verify_password_error, username=username, password = password, verify = verify)

    return render_template('signup.html')

@app.route('/logout')
def logout():
    if session['user']:
        del session['user']
    
    return redirect('/blogs')


@app.route('/blogs', methods=['POST', 'GET'])   
def all_blogs():
    #when people go to blogs, they should see all blogs 
    #GET requests only
    
    blog_id = request.args.get('blog_id')
    user_id = request.args.get('user_id')



    if (blog_id):
        post = Blog.query.get(blog_id)
        return render_template('onepost.html', post=post)
    
    elif user_id:
        user = User.query.get(user_id)
        return render_template('singleUser.html', blogs=user.blogs)

    
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)




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
            user = User.query.get(session['user'])
            new_blog = Blog(title, body, user.id)      
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blogs?id='+str(new_blog.id))

    user = User.query.get(session['user'])
    return render_template('newpost.html', user=user)






if __name__ == "__main__":
    app.run()