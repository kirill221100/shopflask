from app import app, db
from app.models import Category, Meal
import csv

with app.app_context():
    with open('delivery_categories.csv', 'r', encoding='utf-8') as f:
        deliv = csv.reader(f)
        print(deliv)
        for i in deliv:
            if 'title' not in i:
                cat = Category(title=i[1])
                db.session.add(cat)

    db.session.commit()

    with open('delivery_items.csv', 'r', encoding='utf-8') as f:
        deliv = csv.reader(f)
        for i in deliv:
            if 'title' not in i:
                it = Meal(title=i[1], price=i[2], description=i[3], picture=i[4], category=db.session.query(Category).filter(Category.id==i[5]).first())
                # cat = db.session.query(Category).filter(Category.id==i[5]).first()
                # cat.meals
                db.session.add(cat)

    db.session.commit()

    print(db.session.query(Category).first().meals)
