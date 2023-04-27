from flask import Flask, render_template, redirect, abort, request, url_for, make_response, jsonify
from data import db_session
from data.files import Files
from data.users import User
import requests
from flask_restful import Api
from restApi import UsersResource, UsersListRes
from forms.user import RegisterForm, LoginForm, IDForm, AnecForm, TextApiForm, JustForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/owners12.db")
    db_sess = db_session.create_session()
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(UsersListRes, '/api/v2/users')

    @app.route("/", methods=['GET', 'POST'])
    def index():
        global glav, profil
        js = url_for('static', filename='lg/jquery.js')
        glavccs = url_for('static', filename='lg/Главная.css')
        jvnicepage = url_for('static', filename='lg/nicepage.js')
        nicepageccs = url_for('static', filename='lg/nicepage.css')
        str1ccs = url_for('static', filename='lg/Страница-1.css')
        str2ccs = url_for('static', filename='lg/Страница-2.css')
        css = url_for('static', filename='css/css.css')
        glav = url_for('index')
        reg = url_for('register')
        ou = url_for('login')
        form = IDForm()
        anec = AnecForm()
        db_sess = db_session.create_session()
        if current_user.is_authenticated:
            if form.validate_on_submit():
                id = form.id.data
                add_news()
                print(id)
                return redirect(f'/portfolio/{id}')
            return render_template("Главная.html", js=jvnicepage, js2=js,
                                   glav=glav, glavcss=glavccs, str1=str1ccs,
                                   str2=str1ccs, ni=nicepageccs, reg=reg,
                                   log=ou, form=form, css=css, text=TextApiForm())
        if form.validate_on_submit():
            id = form.id.data
            add_news()
            print(id)
            return redirect(f'/portfolio/{id}')
        return render_template("Страница-2.html", js=jvnicepage, js2=js, glav=glav, glavcss=glavccs, str1=str1ccs,
                               str2=str1ccs, ni=nicepageccs, reg=reg, log=ou, form=form, css=css, anec=anec)

    @app.route('/Главная.html', methods=['GET', 'POST'])
    def glav():
        form = IDForm()
        if form.validate_on_submit():
            id = form.id.data
            return redirect(f'/portfolio/{id}')

        return render_template('Главная.html', title='Регистрация',
                               form=form, text=TextApiForm())

    def generator():
        length = '10'
        api_url = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'.format(length)
        response = requests.get(api_url, headers={'X-Api-Key': 'fg4oSPFJZ1Xy+8uIlK3Csg==ViW2Xa7h9Q1MzVgN'})
        if response:
            return response.json()['random_password']
        return None

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
                email=form.email.data,
                name=form.name.data,
                place_job_study=form.place_job_study.data,
                address=form.address.data,
                age=form.age.data,
                phone_num=form.phone_num.data,
                sex=form.sex.data,
                avatar=str(url_for('static', filename=f'images/2021056-0.jpeg')),
                unic_code=str(generator())
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

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

    @app.route('/logout')
    @login_required
    def logout():
        global logout
        logout = url_for('logout')
        logout_user()
        return redirect("/")

    @app.route('/Страница-1.html', methods=['GET', 'POST'])
    def add_news():
        global profil
        profil = url_for('add_news')
        js = url_for('static', filename='lg/jquery.js')
        glavccs = url_for('static', filename='lg/Главная.css')
        jvnicepage = url_for('static', filename='lg/nicepage.js')
        nicepageccs = url_for('static', filename='lg/nicepage.css')
        str1ccs = url_for('static', filename='lg/Страница-1.css')
        str2ccs = url_for('static', filename='lg/Страница-2.css')
        glav = url_for('index')
        reg = url_for('register')
        ou = url_for('login')
        add_avatar = url_for('add_avatar')
        add_file = url_for('sample_file_upload')
        if current_user.is_authenticated:
            db_sess = db_session.create_session()
            user = current_user
            file_sport = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Спорт')
            file_malen = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Учёба')
            file_lernen = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Рисование')
            file_mysik = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Музыка')
            file_shutze = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Волонтёрство')
            file_human = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Общество')
            image = db_sess.query(Files).filter(Files.user_id == user.id, Files.type_f == 'image/jpeg')
            avatar = current_user.avatar
            if file_sport == None:
                file_sport = 'Пусто'
            if file_lernen == None:
                file_lernen = 'Пусто'
            if file_malen == None:
                file_malen = 'Пусто'
            if file_mysik == None:
                file_mysik = 'Пусто'
            if file_shutze == None:
                file_shutze = 'Пусто'
            if file_human == None:
                file_human = 'Пусто'
            return render_template('Страница-1.html', js=jvnicepage, js2=js, glav=glav, glavcss=glavccs, str1=str1ccs,
                                   str2=str2ccs, ni=nicepageccs, current_user=user, reg=reg, log=ou, add=add_file,
                                   file_sport=file_sport, file_lernen=file_lernen, file_malen=file_malen,
                                   file_mysik=file_mysik, file_shutze=file_shutze, file_human=file_human, image=image,
                                   logout=logout, ava=avatar, add_avatar=add_avatar)
        else:
            form = LoginForm()
            if form.validate_on_submit():
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.email == current_user).first()
                if user and user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect("/")
                return render_template('login.html',
                                       message="Неправильный логин или пароль",
                                       form=form)
            return render_template('login.html', title='Авторизация', form=form)

    @app.route('/sample_file_upload', methods=['POST', 'GET'])
    @login_required
    def sample_file_upload():
        if request.method == 'GET':
            return f'''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                 <link rel="stylesheet"
                                 href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                 integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                 crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                <title>Загрузить файл</title>
                              </head>
                              <body>
                                <h1 style=".block-level {{
                                                        width: 120px;
                                                        height: 120px;
                                                        margin: 20px;
                                                        position: relative;
                                                        float: left;
                                                    }};
                                                        font-family: Roboto,sans-serif;
                                                        text-align: center;
                                                        font-weight: 900;
                                                        margin: 60px auto 0;
                                                        color: #a9bcc2 !important;
                                                    ">Загрузим файл</h1>
                                <form method="post" enctype="multipart/form-data">
                                <div class="form-group">
                                        <h4 style=".block-level {{
                                                        width: 120px;
                                                        height: 120px;
                                                        margin: 20px;
                                                        position: relative;
                                                        float: left;
                                                    }};
                                                        font-family: Roboto,sans-serif;
                                                        text-align: center;
                                                        font-weight: 900;
                                                        margin: 60px auto 0;
                                                        color: #a9bcc2 !important;
                                                    ">Выбрать категорию</h4>
                                        <select class="form-control" id="classSelect" name="class" style="
                                                                                    width: 50%;
                                                                                    font-weight: 900;
                                                                                    text-align: center;
                                                                                    font-family: Roboto,sans-serif;
                                                                                    background-color: #9dafb3;
                                                                                    color: #fcfcfc !important;
                                                                                    box-shadow: 7px 7px 7px #9dafb3;
                                                                                    margin-left: 25%;
                                                                                    margin-top: 3%;
                                                                                    margin-block: 3%;
                                                                                    align-items: center;
                                                                                    border-radius: 1.2rem;
                                                                                ">
                                          <option>Спорт</option>
                                          <option>Учёба</option>
                                          <option>Рисование</option>
                                          <option>Музыка</option>
                                          <option>Волонтёрство</option>
                                          <option>Общество</option>
                                        </select>
                                     </div>
                                   <div class="form-group">
                                        <input type="file" class="form-control-file" id="photo" name="file" style="
                                                                                font-family: Roboto,sans-serif;
                                                                                text-align: center;
                                                                                font-weight: 900;
                                                                                margin-left: 25%;
                                                                                color: #ffffff !important;
                                                                                background-color: #9dafb3;
                                                                                color: #FFEFDF;
                                                                                box-shadow: 7px 7px 7px #9dafb3;
                                                                                padding: 6px 12px;
                                                                                cursor: pointer;
                                                                                -webkit-border-radius: 5px;
                                                                                border-radius: 1.2rem;
                                                                                text-decoration-color: #34b8b8;
                                                                                -moz-border-radius: 5px;
                                                                                width: 50%;
                                                                                text-align: center;
                                                                                
                                                                            ">
                                    </div>
                                    <div class="form-group">
                                    <h4 style=".block-level {{
                                                        width: 120px;
                                                        height: 120px;
                                                        margin: 20px;
                                                        position: relative;
                                                        float: left;
                                                    }};
                                                        font-family: Roboto,sans-serif;
                                                        text-align: center;
                                                        font-weight: 900;
                                                        margin: 60px auto 0;
                                                        color: #a9bcc2 !important;
                                                    ">Добавить описание</h4>
                                    <textarea class="form-control" id="about" rows="3" name="about" style="width: 50%;
                                     font-weight: 900; text-align: center; font-family: Roboto, sans-serif;
                                      background-color: rgb(157, 175, 179); box-shadow: rgb(157, 175, 179) 7px 7px 7px;
                                       margin-left: 25%; margin-top: 3%; margin-block: 3%; align-items: center;
                                        border-radius: 1.2rem; color: rgb(252, 252, 252) !important;
                                         height: 109px;"></textarea>
                                    </div>
                                    <button type="submit" class="btn btn-primary" style="
                                                                            background-color: #9dafb3;
                                                                            border-color: #9dafb3;
                                                                            box-shadow: rgb(157, 175, 179) 7px 7px 7px;
                                                                            margin-left: 47%;
                                                                            /* margin-top: 3%; */
                                                                            /* margin-block: 3%; */
                                                                            align-items: center;
                                                                            border-radius: 1.2rem;
                                                                        ">Отправить</button>
                                </form>
                              </body>
                            </html>'''
        elif request.method == 'POST':
            f = request.files['file']
            f1 = request.form['class']
            inf = request.form['about']
            db_sess = db_session.create_session()
            user = current_user
            f.save(f"static/Portfolio/{f.filename}")
            url = url_for('static', filename=f'Portfolio/{f.filename}')
            file = Files(
                owner=current_user,
                user_id=current_user.id,
                type_f=f.content_type,
                url_address=url,
                type=f1,
                info=inf
            )
            current_user.file.append(file)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/Страница-1.html')

    @app.route('/add_avatar', methods=['POST', 'GET'])
    @login_required
    def add_avatar():
        if request.method == 'GET':
            return f'''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                     <link rel="stylesheet"
                                     href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                     integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                     crossorigin="anonymous">
                                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                    <title>Изменить аватар</title>
                                  </head>
                                  <body>
                                    <h1 style=".block-level {{
                                                            width: 120px;
                                                            height: 120px;
                                                            margin: 20px;
                                                            position: relative;
                                                            float: left;
                                                        }};
                                                            font-family: Roboto,sans-serif;
                                                            text-align: center;
                                                            font-weight: 900;
                                                            margin: 60px auto 0;
                                                            color: #a9bcc2 !important;
                                                        ">Изменить аватар</h1>
                                    <form method="post" enctype="multipart/form-data">
                                    
                                       <div class="form-group">
                                            <input type="file" class="form-control-file" id="photo" name="file" style="
                                                                                    font-family: Roboto,sans-serif;
                                                                                    text-align: center;
                                                                                    font-weight: 900;
                                                                                    margin-left: 25%;
                                                                                    color: #ffffff !important;
                                                                                    background-color: #9dafb3;
                                                                                    color: #FFEFDF;
                                                                                    box-shadow: 7px 7px 7px #9dafb3;
                                                                                    padding: 6px 12px;
                                                                                    cursor: pointer;
                                                                                    -webkit-border-radius: 5px;
                                                                                    border-radius: 1.2rem;
                                                                                    text-decoration-color: #34b8b8;
                                                                                    -moz-border-radius: 5px;
                                                                                    width: 50%;
                                                                                    text-align: center;
                                                                                    margin-top: 90px;
                                                                                ">
                                        </div>
                                        
                                        <button type="submit" class="btn btn-primary" style="
                                                                                background-color: #9dafb3;
                                                                                border-color: #9dafb3;
                                                                                box-shadow: rgb(157, 175, 179) 7px 7px 7px;
                                                                                margin-left: 47%;
                                                                                /* margin-top: 3%; */
                                                                                /* margin-block: 3%; */
                                                                                align-items: center;
                                                                                border-radius: 1.2rem;
                                                                                margin-top: 30px;
                                                                            ">Отправить</button>
                                    </form>
                                  </body>
                                </html>'''
        elif request.method == 'POST':
            f = request.files['file']
            db_sess = db_session.create_session()
            user = current_user
            f.save(f"static/Аватары/{f.filename}")
            url = url_for('static', filename=f'Аватары/{f.filename}')
            current_user.avatar = url
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/Страница-1.html')

    @app.route('/all_profs', methods=['GET', 'POST'])
    def all_profs():
        form = JustForm()

        sess = db_session.create_session()
        als = sess.query(User).all()

        return render_template('all_prof.html', form=form, spis=als)

    @app.route('/portfolio/<int:id>', methods=['POST', 'GET'])
    def portfolio(id):
        global profil
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        js = url_for('static', filename='lg/jquery.js')
        glavccs = url_for('static', filename='lg/Главная.css')
        jvnicepage = url_for('static', filename='lg/nicepage.js')
        nicepageccs = url_for('static', filename='lg/nicepage.css')
        str1ccs = url_for('static', filename='lg/Страница-1.css')
        str2ccs = url_for('static', filename='lg/Страница-2.css')
        str3css = url_for('static', filename='lg/Страница-3.css')
        glav = url_for('index')
        reg = url_for('register')
        ou = url_for('login')
        im_file_sport = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Спорт', Files.type_f == 'image/jpeg')
        im_file_malen = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Учёба', Files.type_f == 'image/jpeg')
        im_file_lernen = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Рисование', Files.type_f == 'image/jpeg')
        im_file_mysik = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Музыка', Files.type_f == 'image/jpeg')
        im_file_shutze = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Волонтёрство', Files.type_f == 'image/jpeg')
        im_file_human = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Общество', Files.type_f == 'image/jpeg')
        file_sport = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Спорт')
        file_malen = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Учёба')
        file_lernen = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Рисование')
        file_mysik = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Музыка')
        file_shutze = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Волонтёрство')
        file_human = db_sess.query(Files).filter(Files.user_id == user.id, Files.type == 'Общество')
        image = db_sess.query(Files).filter(Files.user_id == user.id, Files.type_f == 'image/jpeg')
        if file_sport == None:
            file_sport = 'Пусто'
        if file_lernen == None:
            file_lernen = 'Пусто'
        if file_malen == None:
            file_malen = 'Пусто'
        if file_mysik == None:
            file_mysik = 'Пусто'
        if file_shutze == None:
            file_shutze = 'Пусто'
        if file_human == None:
            file_human = 'Пусто'
        return render_template('Страница-3.html', js=jvnicepage, js2=js, glav=glav, glavcss=glavccs, str1=str1ccs,
                                   str2=str2ccs, ni=nicepageccs, current_user=user, reg=reg, log=ou,
                                   file_sport=file_sport, file_lernen=file_lernen, file_malen=file_malen,
                                   file_mysik=file_mysik, file_shutze=file_shutze, file_human=file_human,
                                   im_file_sport=im_file_sport, im_file_lernen=im_file_lernen, im_file_malen=im_file_malen,
                                   im_file_mysik=im_file_mysik, im_file_shutze=im_file_shutze,
                               im_file_human=im_file_human, image=image, profil=profil)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(400)
    def bad_request(_):
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
