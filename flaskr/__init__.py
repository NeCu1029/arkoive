from flask import abort, Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import os
from .prob import prob_bp
from .user import user_bp
from .util import bc, db, manager, User

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.register_blueprint(user_bp)
app.register_blueprint(prob_bp)

bc.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()
manager.init_app(app)
manager.login_view = "user_bp.login"  # type: ignore
manager.login_message = "로그인 상태가 아닙니다."


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == "arkoive"

    def inaccessible_callback(self):
        abort(403)


admin = Admin(app, name="내 관리자 페이지")
admin.add_view(SecureModelView(User, db.session))


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "아직 로그인을 하지 않았어요!"
    return render_template("index.html", username=username)


if __name__ == "__main__":
    app.run()
