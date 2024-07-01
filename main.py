from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange
from flask_bootstrap import Bootstrap5
from database import db, Book

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class Form(FlaskForm):
    title = StringField(label='Title', validators=[InputRequired()])
    author = StringField(label='Author', validators=[InputRequired()])
    rating = StringField(label="rating", validators=[InputRequired()])
    submit = SubmitField(label="Add Book")


class NewForm(FlaskForm):
    rating = StringField(label="New Rating", validators=[InputRequired()])
    submit = SubmitField(label="Change Rating")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

with app.app_context():
    db.create_all()

app.secret_key = "dede557dfjzzd"
bootstrap = Bootstrap5(app)
all_books = []
books = []


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    books = list(result.scalars())
    print(books)
    print(result)
    return render_template('index.html', books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = Form()
    form.validate_on_submit()
    if form.validate_on_submit():
        diction = {
            "title": form.title.data,
            "author": form.author.data,
            "rating": form.rating.data
        }
        all_books.append(diction)
        with app.app_context():
            addition = Book(
                title=form.title.data,
                author=form.author.data,
                rating=form.rating.data
            )

            db.session.add(addition)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    form = NewForm()
    form.validate_on_submit()
    book_rating = db.get_or_404(Book, id)
    if form.validate_on_submit():
        new = form.rating.data
        book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        book_to_update.rating = new
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book_rating, form=form)


@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = db.get_or_404(Book, id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)

