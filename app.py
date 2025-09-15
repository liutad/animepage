from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 上传目录
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# 评论表
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()  # 第一次运行会建表


@app.route('/')
def animepage():
    return render_template('animepage.html')

@app.route('/secondpage')
def secondpage():
    return render_template('secondpage.html')

@app.route('/roleplay')
def roleplay():
    return render_template('roleplay.html')

@app.route('/animeplot')
def animeplot():
    return render_template('animeplot.html')

@app.route('/productpage')
def productpage():
    return render_template('productpage.html')

@app.route('/commentpage')
def commentpage():
    comments = Comment.query.order_by(Comment.id.desc()).all()
    for c in comments:
        if c.avatar:
            c.avatar_url = url_for("static", filename=c.avatar)
        else:
            c.avatar_url = url_for("static", filename="pic/default_avatar.png")

    return render_template('commentpage.html', comments=comments)

@app.route("/submit_comment", methods=["POST"])
def submit_comment():
    nickname = request.form.get("nickname")
    comment = request.form.get("comment")
    avatar_file = request.files.get("avatar")

    avatar_filename = None
   

    if avatar_file and avatar_file.filename:
        ext = os.path.splitext(avatar_file.filename)[1]  # 保留原扩展名
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        avatar_file.save(filepath)
        avatar_filename = f"uploads/{filename}"


    new_comment = Comment(nickname=nickname, comment=comment, avatar=avatar_filename)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for("commentpage"))

@app.route('/producerpage')
def producerpage():
    return render_template('producerpage.html')


@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("commentpage"))


if __name__ == '__main__':
    app.run(debug=True)
