from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Article %r>' % self.id

'''@app.route('/create_article')
def create_article():
    # Создаем экземпляр модели Article
    article = Article(title='Заголовок статьи', intro='Вступительный текст', text='Текст статьи')

    # Добавляем экземпляр в сессию SQLAlchemy
    db.session.add(article)

    # Фиксируем изменения, чтобы они были сохранены в базе данных
    db.session.commit()

    return 'Статья успешно создана и сохранена в базе данных!'
'''
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Something wrong"


@app.route('/posts/<int:id>/update', methods=["POST","GET"])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        article =Article(title=title, intro=intro,text=text)

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Something went wrong"

    else:
        article = Article.query.get(id)
        return render_template("post_update.html",article=article)




@app.route('/create-article', methods=["POST","GET"])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article =Article(title=title, intro=intro,text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Something went wrong"

    else:
        return render_template("create-article.html")



if __name__ == "__main__":
    # Создаем контекст приложения Flask
    with app.app_context():
        # Создаем все таблицы в базе данных
        db.create_all()

    # Запускаем приложение Flask
    app.run(debug=True)

    """My first time work with flask"""