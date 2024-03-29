from datetime import datetime
from flask_login import UserMixin

from blog import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False) # 64
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)

    articles = db.relationship('Article', backref='owner')

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True, nullable=False)

    categories = db.relationship('Article', backref='category')

    def __repr__(self):
        return f"Category('{self.title}')"

class Article(db.Model):
    __tablename__ = 'article'
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    @staticmethod
    def marshmallow_data(article):
        article_data = {}

        article_data['article_id'] = article.id
        article_data['user_id'] = article.owner.id
        article_data['title'] = article.title
        article_data['content'] = article.content
        article_data['category'] = article.category.title
        article_data['first_name'] = article.owner.first_name
        article_data['last_name'] = article.owner.first_name
        article_data['created_at'] = article.created_at
        article_data['updated_at'] = article.updated_at

        return article_data

    def __repr__(self):
        return f"Article('{self.title}', '{self.content}')"