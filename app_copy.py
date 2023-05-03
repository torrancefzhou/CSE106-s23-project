from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_login import current_user, login_user, login_required, LoginManager, UserMixin, logout_user
import bcrypt

from sqlalchemy import inspect

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.secret_key = 'super secret key'
app.app_context().push()
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    posts = db.relationship('Posts', backref='user')
    comments = db.relationship('Comments', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    # def check_password(self, password):
    #     return self.password == password


class Posts(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    title = db.Column(db.String) # e.g. "CSE 100"
    body = db.Column(db.String) # e.g. "TR 3:00PM - 4:15PM"
    likes = db.Column(db.Integer) # e.g. 4 (/10)
    dislikes = db.Column(db.Integer) # e.g. (4/) 10
    comments = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # e.g. "1001"
    #instructor = db.relationship('Account', backref=db.backref('teacher', lazy=True))

    comment = db.relationship('Comments', backref='posts')
    rating = db.relationship('Ratings', backref='posts')

    def __repr__(self):
        return '<Posts %r>' % self.title


class Comments(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    body = db.Column(db.String)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    

    rating = db.relationship('Ratings', backref='post')

    def __repr__(self):
        return '<Comments %r>' % self.body

class Ratings(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    rating = db.Column(db.Integer) #0 Neutral, 1 Liked, 2 Disliked


with app.app_context():
    # db.drop_all() # resets tables between instances, do this if you change table models
    db.create_all()


class UserModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = ['id', 'username', 'name', 'is_admin']

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class PostModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Posts).mapper.column_attrs]

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class CommentModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Comments).mapper.column_attrs]

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class RatingModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Ratings).mapper.column_attrs]

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated

admin = Admin(app, name='gradebook', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))
admin.add_view(PostModelView(Posts, db.session))
admin.add_view(CommentModelView(Comments, db.session))
admin.add_view(RatingModelView(Ratings, db.session))
admin.add_link(LoginMenuLink(name='Return to Login Page', category='', url="/login"))
admin.add_link(LogoutMenuLink(name='Return to Homepage', category='', url="/index"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/index')
@app.route('/')
@login_required
def index(): # put application's code here
    if current_user.is_admin:
        return render_template('admin_index.html')
    else:
        return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))


@app.route('/posts', methods=['GET'])
@login_required
def myPosts():
        data = Posts.query.filter_by(user_id=current_user.id).all()

        return jsonify([{"title": item.title,
                     "id": item.id,
                     "body": item.body,
                     "likes": item.likes,
                     "dislikes": item.dislikes,
                     "comments": item.comments} for item in data])


@app.route("/posts", methods=['POST'])
@login_required
def addPost():
    # add Post
    body = request.get_json()
    title = body['title']
    tempbody = body['body']
    newPost = Posts(user_id=current_user.id, title=title, body=tempbody, likes=0, dislikes=0, comments=0)
    db.session.add(newPost)
    db.session.commit()
    return 'Created new Post'


@app.route("/posts", methods=['DELETE'])
@login_required
def deletePost():
    # Delete Post
    body = request.get_json()
    postID = body['postID']
    post = Posts.query.filter_by(id=postID).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/allposts', methods=['GET'])
@login_required
def allPosts():
        data = Posts.query.all()

        return jsonify([{"title": item.title,
                     "id": item.id,
                     "body": item.body,
                     "likes": item.likes,
                     "dislikes": item.dislikes,
                     "comments": item.comments} for item in data])


@app.route('/posts/<postID>', methods=['GET'])
@login_required
def postComments(postID):
        temp = Posts.query.filter_by(id=postID).first()
        data = Comments.query.filter_by(post_id=temp.id).all()

        return jsonify([{"body": item.body,
                     "likes": item.likes,
                     "dislikes": item.dislikes} for item in data])


@app.route("/posts/<postID>", methods=['POST'])
@login_required
def addComment(postID):
    # add Comment
    body = request.get_json()
    tempbody = body['body']
    newComment = Comments(user_id=current_user.id, post_id=postID, body=tempbody, likes=0, dislikes=0, comments=0)
    db.session.add(newComment)
    db.session.commit()
    return 'Created new Post'


@app.route("/posts/<postID>", methods=['DELETE'])
@login_required
def deleteComment(postID):
    # delete Comment
    comment = Comments.query.filter_by(user_id=current_user.id, post_id=postID)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/posts/<postID>/rating", methods=['POST'])
@login_required
def addPostRating(postID):
    body = request.get_json()
    rating = body['rating']

    newRating = Ratings(user_id=current_user.id, post_id=postID, rating=rating)
    db.session.add(newRating)
    db.session.commit()
    return 'Added new Rating'


@app.route("/posts/<postID>/rating", methods=['DELETE'])
@login_required
def deletePostRating(postID):
    post = Posts.query.filter_by(id=postID).first()
    rating = Ratings.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if rating:
        db.session.delete(rating)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/posts/<postID>/rating", methods=['PUT'])
@login_required
def editPostRating(postID):
    body = request.get_json()
    rating = body['rating']
    post = Posts.query.filter_by(id=postID).first()
    rate_obj = Ratings.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if rate_obj:
        rate_obj.rating = rating
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/posts/<postID>/<commentID>/rating", methods=['POST'])
@login_required
def addCommentRating(postID, commentID):
    body = request.get_json()
    rating = body['rating']

    newRating = Ratings(user_id=current_user.id, comment_id=commentID, rating=rating)
    db.session.add(newRating)
    db.session.commit()
    return 'Added new Rating'


@app.route("/posts/<postID>/<commentID>/rating", methods=['DELETE'])
@login_required
def deleteCommentRating(postID, commentID):
    comment = Comments.query.filter_by(post_id=postID, id=commentID).first()
    rating = Ratings.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    if rating:
        db.session.delete(rating)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/posts/<postID>/<commentID>/rating", methods=['PUT'])
@login_required
def editCommentRating(postID, commentID):
    body = request.get_json()
    rating = body['rating']
    comment = Comments.query.filter_by(post_id=postID, id=commentID).first()
    rate_obj = Ratings.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    if rate_obj:
        rate_obj.rating = rating
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route("/profile")
@login_required
def profile():
    return render_template('profile_page.html')

@app.route('/profile/<username>', methods=['GET'])
@login_required
def myProfile():
        data = User.query.filter_by(id=current_user.id).all()

        return jsonify([{"username": item.username,
                     "name": item.name} for item in data])


if __name__ == "__main__":
    app.run()