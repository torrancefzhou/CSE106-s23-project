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
    password_hash = db.Column(db.String, unique=True, nullable=False) # should this be unique?
    name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean)

    posts = db.relationship('Posts', backref='user')
    comments = db.relationship('Comments', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class Posts(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    title = db.Column(db.String) # e.g. "CSE 100"
    body = db.Column(db.String) # e.g. "TR 3:00PM - 4:15PM"
    likes = db.Column(db.Integer) # e.g. 4 (/10)
    dislikes = db.Column(db.Integer) # e.g. (4/) 10
    comments = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # e.g. "1001"
    # instructor = db.relationship('Account', backref=db.backref('teacher', lazy=True))

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
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    rating = db.Column(db.Integer) #0 Neutral, 1 Liked, 2 Disliked

class Followed(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])
    followed = db.relationship("User", foreign_keys=[followed_id])


with app.app_context():
    # db.drop_all() # resets tables between instances, do this if you change table models
    db.create_all()

def can_access_admin_db():
    return True  # to make new account after resetting DB
    return current_user.get_id() and current_user.is_admin

class UserModelView(sqla.ModelView):
    column_hide_backrefs = False
    # column_list = [c_attr.key for c_attr in inspect(User).mapper.column_attrs]
    column_list = ['id', 'username', 'name', 'is_admin']

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class PostModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Posts).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class CommentModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Comments).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class RatingModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Ratings).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    
class FollowedModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Followed).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()

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
admin.add_view(FollowedModelView(Followed, db.session))
admin.add_link(LoginMenuLink(name='Return to Login Page', category='', url="/login"))
admin.add_link(LogoutMenuLink(name='Return to Homepage', category='', url="/index"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def get_followed_posts():
    tempData = Followed.query.filter_by(user_id=current_user.id).all()
    data = Posts.query.filter_by(id='missing').all()
    for x in tempData:
        temp = Posts.query.filter_by(user_id=x.followed_id).all()
        for y in temp:
            data.append(y)
    return data

def post_data(item):
    return {"title": item.title,
            "id": item.id,
            "body": item.body,
            "poster": (User.query.filter_by(id=item.user_id).first()).username,
            "following": False if not current_user.is_authenticated else
                Followed.query.filter_by(user_id=current_user.id, followed_id=item.user_id).first() is not None,
            "likes": item.likes,
            "dislikes": item.dislikes,
            "comments": item.comments,
            "rating": 0 if not current_user.is_authenticated else 
                Ratings.query.filter_by(post_id=item.id, user_id=current_user.id).first()}

def post_to_json(item):
    return jsonify(post_data(item))

def posts_to_json(data):
    return jsonify([post_data(item) for item in data])

def comment_data(item):
    return {"body": item.body,
            "commentor": (User.query.filter_by(id=item.user_id).first()).username,
            "following": False if not current_user.is_authenticated else
                Followed.query.filter_by(user_id=current_user.id, followed_id=item.user_id).first() is not None,
            "id": item.id,
            "likes": item.likes,
            "dislikes": item.dislikes,
            "rating": 0 if not current_user.is_authenticated else 
            Ratings.query.filter_by(comment_id=item.id, user_id=current_user.id).first()}

@app.route('/index')
@app.route('/')
def index(): # put application's code here
    if current_user.is_authenticated and current_user.is_admin:
        return render_template('admin_index.html')
    elif current_user.is_authenticated:
        return render_template('index.html', 
                               posts=[post_data(item) for item in Posts.query.all()], 
                               followed=[post_data(item) for item in get_followed_posts()])
    else:
        return render_template('index.html', posts=[post_data(item) for item in Posts.query.all()])

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        print("already logged in")
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        print("user does not exist")
        return redirect(url_for('login'))
    login_user(user)
    print("successful login")
    return redirect(url_for('index'))

@app.route('/postsby/<username>', methods=['GET'])
def userPosts(username):
    tempData = User.query.filter_by(username=username).first()
    data = Posts.query.filter_by(user_id=tempData.id).all()
    return posts_to_json(data)

@app.route('/allposts', methods=['GET'])
# @login_required 
def allPosts():
    data = Posts.query.all()
    return posts_to_json(data)

@app.route('/page/<postID>', methods=["GET"])
def postPage(postID):
    # TODO: return data of the post for jinja template
    return render_template("post_page.html", 
                           postInfo=post_data(Posts.query.filter_by(id=postID).first()), 
                           comments=[comment_data(item) for item in Comments.query.filter_by(post_id=postID)])

@app.route("/posts", methods=['POST'])
@login_required
def addPost():
    # add Post
    body = request.form
    title = body['title']
    tempbody = body['body']
    newPost = Posts(user_id=current_user.id, title=title, body=tempbody, likes=0, dislikes=0, comments=0)
    db.session.add(newPost)
    db.session.commit()
    postID = newPost.id
    return redirect("/page/" + str(postID))


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
    
@app.route('/posts/<postID>', methods=['GET'])
def postbyID(postID):
    data = Posts.query.filter_by(id=postID).first()
    return post_to_json(data)

@app.route('/followed', methods=['GET'])
def followedPosts():
    return posts_to_json(get_followed_posts())

@app.route('/posts/<postID>/comments', methods=['GET'])
@login_required
def seeComments(postID):
    temp = Posts.query.filter_by(id=postID).first()
    data = Comments.query.filter_by(post_id=temp.id).all()
    return jsonify([{"body": item.body,
                    "id": item.id,
                    "likes": item.likes,
                    "dislikes": item.dislikes} for item in data])

@app.route("/posts/<postID>/comments", methods=['POST'])
@login_required
def addComment(postID):
    # add Comment
    body = request.form
    tempbody = body['body']
    newComment = Comments(user_id=current_user.id, post_id=postID, body=tempbody, likes=0, dislikes=0)
    Posts.query.filter_by(id=postID).first().comments += 1
    db.session.add(newComment)
    db.session.commit()
    return redirect("/page/" + str(postID))


@app.route("/posts/<postID>/comments", methods=['DELETE'])
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
    
@app.route('/posts/<postID>/rating', methods=['GET'])
def getUserRating(postID):
    data = 0 if not current_user.is_authenticated else Ratings.query.filter_by(post_id=postID, user_id=current_user.id).first()
    return jsonify({"rating": data.rating})

@app.route("/posts/<postID>/rating/<rating>", methods=['POST'])
@login_required
def addPostRating(postID, rating):
    orig_post = Posts.query.filter_by(id=postID).first()
    if rating == "1":
        orig_post.likes += 1
    elif rating == "2":
        orig_post.dislikes += 1
    newRating = Ratings(user_id=current_user.id, post_id=postID, rating=rating)
    db.session.add(newRating)
    db.session.commit()
    return 'Added new Rating'

@app.route("/posts/<postID>/rating", methods=['DELETE'])
@login_required
def deletePostRating(postID):
    orig_post = Posts.query.filter_by(id=postID).first()
    rate = Ratings.query.filter_by(user_id=current_user.id, post_id=orig_post.id).first()

    if rate.rating == 1:
        orig_post.likes -= 1
    elif rate.rating == 2:
        orig_post.dislikes -= 1

    if rate:
        db.session.delete(rate)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route("/posts/<postID>/rating", methods=['PUT'])
@login_required
def editPostRating(postID):
    body = request.get_json()
    rate= body['rating']
    post = Posts.query.filter_by(id=postID).first()
    rate_obj = Ratings.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if rate == 1:
        post.likes += 1
        post.dislikes -= 1
    elif rate == 2:
        post.likes -= 1
        post.dislikes += 1

    if rate_obj:
        rate_obj.rating = rate
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route("/posts/<postID>/<commentID>/rating/<rating>", methods=['POST'])
@login_required
def addCommentRating(postID, commentID, rating):
    orig_comment = Comments.query.filter_by(id=commentID).first()
    if rating == "1":
        orig_comment.likes += 1
    elif rating == "2":
        orig_comment.dislikes += 1
    
    newRating = Ratings(user_id=current_user.id, comment_id=commentID, rating=rating)
    db.session.add(newRating)
    db.session.commit()
    return 'Added new Rating'


@app.route("/posts/<postID>/<commentID>/rating", methods=['DELETE'])
@login_required
def deleteCommentRating(postID, commentID):
    orig_comment = Comments.query.filter_by(id=commentID).first()
    rate = Ratings.query.filter_by(user_id=current_user.id, comment_id=commentID).first()

    if rate.rating == 1:
        orig_comment.likes -= 1
    elif rate.rating == 2:
        orig_comment.dislikes -= 1

    if rate:
        db.session.delete(rate)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/posts/<postID>/<commentID>/rating", methods=['PUT'])
@login_required
def editCommentRating(postID, commentID):
    body = request.get_json()
    rate = body['rating']
    comment = Comments.query.filter_by(id=commentID).first()
    rating = Ratings.query.filter_by(user_id=current_user.id, comment_id=commentID).first()

    if rate == 1:
        comment.likes += 1
        comment.dislikes -= 1
    elif rate == 2:
        comment.likes -= 1
        comment.dislikes += 1

    if rating:
        rating.rating = rate
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    check = request.form["confirm"]
    if check != password:
        return redirect('register')
    name = request.form["name"]
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        return "Username already exists", 409
    newUser = User(username=username, password_hash="", name=name, is_admin=False)
    newUser.set_password(password)
    db.session.add(newUser)
    db.session.commit()
    return redirect('login')

@app.route("/users/<username>", methods=["GET"])
def profile_page(username):
    if User.query.filter_by(username=username).first():
        id = User.query.filter_by(username=username).first().id
        return render_template("profile_page.html", username=username, posts=[post_data(item) for item in Posts.query.filter_by(user_id=id)])
    return "User does not exist", 404

@app.route("/new_post", methods=["GET"])
def new_post_page():
    return render_template("new_post.html")

@app.route("/follow/<username>", methods=["POST"])
@login_required
def toggle_follow(username):
    desired_follow = request.json["now_following"]
    followed = User.query.filter_by(username=username).first()
    if followed:
        follow_object = Followed.query.filter_by(user_id=current_user.id, followed_id=followed.id).first()
        if follow_object and (not desired_follow):
            db.session.delete(follow_object)
            db.session.commit()
        elif (not follow_object) and desired_follow:
            follow = Followed(user_id=current_user.id, followed_id=followed.id)
            db.session.add(follow)
            db.session.commit()
        return jsonify({"now_following": desired_follow})
    else:
        return "User does not exist", 404

if __name__ == "__main__":
    app.run()