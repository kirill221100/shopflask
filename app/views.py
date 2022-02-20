from flask import abort, flash, session, redirect, request, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required
import random
from app import app, db

from app.models import Category, Meal, Order, User

from app.forms import OrderForm, RegisterForm, AuthForm

@app.route('/')
def index():
    category = db.session.query(Category).all()
    c_meals = {}
    for i in category:
        c_meals[i] = random.sample(i.meals, 3)
    return render_template('main.html', c_meals=c_meals, meal=db.session.query(Meal).filter(Meal.id.in_(session.get('cart'))).all() if session.get('cart') else [])

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    #if form.validate_on_submit():
    message = None
    if session.get('del'):
        message = session.get('del')
        session.pop('del')
    if form.validate_on_submit():
        order = Order(price=sum([i.price for i in db.session.query(Meal).filter(Meal.id.in_(session.get('cart'))).all()]), status='Не доставлен', mail=form.mail.data, phone=form.phone.data, address=form.address.data, user=db.session.query(User).filter(User.id == current_user.id).first())
        for i in session.get("cart"):
            order.meals.append(db.session.query(Meal).filter(Meal.id == i).first())
        db.session.add(order)
        db.session.commit()
        return render_template('ordered.html')

    return render_template('cart.html', meal=db.session.query(Meal).filter(Meal.id.in_(session.get('cart'))).all() if session.get('cart') else [], message=message, form=form)


@app.route('/add/<int:item>/')
def add_to_cart(item):
    cart = session.get("cart", [])
    if int(item) not in cart:
        cart.append(int(item))
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/delete/<int:item>/')
def delete_from_cart(item):
    cart = session.get("cart", [])
    if int(item) in cart:
        cart.remove(int(item))
        session['cart'] = cart
        session['del'] = 'Блюдо удалено из корзины'
    return redirect(url_for('cart'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', orders=current_user.orders)

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    form = AuthForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.mail == form.mail.data).first()
        if user is not None and user.validate_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Неправильная электропочта или пароль')
            return redirect(url_for('auth'))
    return render_template('auth.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(mail=form.mail.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
