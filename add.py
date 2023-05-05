from app_copy import db, User, Posts, Comments, Ratings

# Account
user1 = User(username = "user1", name = "Connor", is_admin=False)
user1.set_password("user1")
user2 = User(username = "user2", name = "Cameron", is_admin=False)
user2.set_password("user2")
user3 = User(username = "user3", name = "Torrence", is_admin=False)
user3.set_password("user3")
admin = User(username = "admin", name = "admin", is_admin=True)
admin.set_password("admin")


# Posts
post1 = Posts(title = "My First Post",
                  body = "show me the money",
                  likes = 1,
                  dislikes = 1,
                  comments = 2,
                  user_id = (User.query.filter_by(username = "user1").first()).id)

post2 = Posts(title = "My Second Post",
                  body = "Is it working",
                  likes = 0,
                  dislikes = 1,
                  comments = 1,
                  user_id = (User.query.filter_by(username = "user1").first()).id)

post3 = Posts(title = "Test post",
                  body = "yo",
                  likes = 0,
                  dislikes = 0,
                  comments = 0,
                  user_id = (User.query.filter_by(username = "user2").first()).id)


# Comments
comment1 = Comments(body = "bad",
                  likes = 0,
                  dislikes = 0,
                  user_id = (User.query.filter_by(username = "user3").first()).id,
                  post_id = (Posts.query.filter_by(title = "My Second Post").first()).id)

comment2 = Comments(body = "good",
                  likes = 0,
                  dislikes = 0,
                  user_id = (User.query.filter_by(username = "user3").first()).id,
                  post_id = (Posts.query.filter_by(title = "My First Post").first()).id)

comment3 = Comments(body = "meh",
                  likes = 0,
                  dislikes = 1,
                  user_id = (User.query.filter_by(username = "user2").first()).id,
                  post_id = (Posts.query.filter_by(title = "My First Post").first()).id)


# Ratings
rating1 = Ratings(rating = 1,
                  user_id = (User.query.filter_by(username = "user3").first()).id,
                  post_id = (Posts.query.filter_by(title = "My First Post").first()).id)

rating2 = Ratings(rating = 2,
                  user_id = (User.query.filter_by(username = "user3").first()).id,
                  post_id = (Posts.query.filter_by(title = "My Second Post").first()).id)

rating3 = Ratings(rating = 2,
                  user_id = (User.query.filter_by(username = "user3").first()).id,
                  comment_id = (Comments.query.filter_by(body = "meh").first()).id)

rating4 = Ratings(rating = 2,
                  user_id = (User.query.filter_by(username = "user2").first()).id,
                  post_id = (Posts.query.filter_by(title = "My First Post").first()).id)


# add
#db.session.add(user1)
#db.session.add(user2)
#db.session.add(user3)
#db.session.add(admin)

#db.session.add(post1)
#db.session.add(post2)
#db.session.add(post3)

#db.session.add(comment1)
#db.session.add(comment2)
#db.session.add(comment3)

db.session.add(rating1)
db.session.add(rating2)
db.session.add(rating3)
db.session.add(rating4)


# delete
# User.query.filter_by(username = "test").delete()
# Course.query.filter_by(name = "Exploratory Computing").delete()
# Enrollment.query.filter_by(studentid = 123).delete()
# Instruction.query.filter_by(classid = 456).delete()

db.session.commit()