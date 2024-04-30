from flask import Flask, render_template,redirect,url_for, request, jsonify
from quoteClass import Quote
from quotes import quotes
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'

# ------------ CREATE DATABASE SCHEMA ----------------------   
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Quote(db.Model) :
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    quote : Mapped[str] = mapped_column(String, unique=True, nullable=False) 
    author : Mapped[str] = mapped_column(String, nullable=False) 
    category : Mapped[str] = mapped_column(String, nullable=False) 
    likes : Mapped[int] = mapped_column(Integer, nullable=False)
    dislikes : Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {column.name : getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

def populate_database():
    for quote in quotes :
        with app.app_context():
            new_quote = Quote(quote = quote["quote"], author = quote["author"], category = quote["category"], likes = quote["likes"], dislikes = quote["dislikes"])
            db.session.add(new_quote)
            db.session.commit()

# # This is used initally to populate the database. 
# populate_database()

def get_categories():
    categories = []
    categories = db.session.execute(db.select(Quote.category).distinct().order_by(Quote.category)).scalars().all()
    return categories

def get_quotes():
    quote_objects = db.session.execute(db.select(Quote)).scalars().all()
    return quote_objects

@app.route("/add-like/<id>")
def add_like(id):
    requested_quote = db.get_or_404(Quote, id)
    requested_quote.likes += 1
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add-dislike/<id>")
def add_dislike(id):
    requested_quote = db.get_or_404(Quote, id)
    requested_quote.dislikes += 1
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods = ['GET', 'POST'])
def add_quote():
    if request.method == 'GET' :
        return render_template('add.html', categories = get_categories())
    else : 
        quote = request.form.get("quote")
        author = request.form.get("author")
        category = request.form.get("category")
        db.session.add(Quote(quote=quote, author = author, category=category, likes=0, dislikes=0))
        db.session.commit()
        return "Added"

@app.route("/category/<category>")
def list_by_category(category):
    quote_objects = db.session.execute(db.select(Quote).where(Quote.category == category)).scalars().all()
    return render_template('list.html', quotes = quote_objects[:5])

@app.route("/author/<athour>")
def list_by_author(author):
    quote_objects = db.session.execute(db.select(Quote).where(Quote.author == author)).scalars().all()
    return render_template('list.html', quotes = quote_objects[:5])

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/all")
def all():
    return jsonify(quotes = [quote.to_dict() for quote in get_quotes()])

@app.route("/")
def home():
    # return render_template('dummy.html')
    return render_template("index.html", quotes = get_quotes()[:5], categories = get_categories()[:6])

if __name__ == "__main__" : 
    app.run(debug=True)