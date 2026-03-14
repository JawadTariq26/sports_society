from flask import Blueprint, render_template
from flask_login import login_required, current_user


bp = Blueprint("root", __name__)


@bp.route("/")
def public_view():
    return render_template("public_view.html")


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")