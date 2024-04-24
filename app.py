from flask import Flask, render_template
from quoteClass import Quote
from quotes import quotes

app = Flask(__name__)

quote_objects = [Quote(id=q["id"], quote=q["quote"], author=q["author"],\
                        category=q["category"], likes=q["likes"], dislikes=q["dislikes"]) \
                            for q in quotes]

def get_categories():
    categories = []
    for quote in quote_objects : 
        if not quote.category in categories : 
            categories.append(quote.category)
    return categories

@app.route("/single")
def single_page():
    return render_template('single.html')

@app.route("/")
def home():
    return render_template("index.html", quotes = quote_objects[:5], categories = get_categories()[:6])

if __name__ == "__main__" : 
    app.run(debug=True)