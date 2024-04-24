from flask import Flask, render_template, redirect
from data import db_session
from data.Plans import Plans
from data.Users import User
from flask_login import LoginManager, login_user
from data.Login_form import LoginForm
from data.Register_form import RegisterForm
from data.MakePlan_form import PlanForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/share_plans.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
@app.route("/main")
def index():
    db_sess = db_session.create_session()
    plans = db_sess.query(Plans).filter(Plans.is_privated != True)
    return render_template("main.html", plans=plans)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/plans', methods=['GET', 'POST'])
def plans():
    form = PlanForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        plans = Plans(
            title=form.title.data,
            descreption=form.about.data,
            is_privated=form.private.data,
        )
        db_sess.add(plans)
        db_sess.commit()
        return redirect('/')
    return render_template('make_plan.html', title='Сделать план', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()