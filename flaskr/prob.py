# 문제 검색

from flask import Blueprint, render_template, request
from .util import Prob

prob_bp = Blueprint("prob_bp", __name__)


@prob_bp.route("/problems")
def problems():
    page = request.args.get("page", default=1, type=int)
    if page < 1:
        page = 1

    problems = Prob.query.order_by(Prob.id).offset((page - 1) * 25).limit(25).all()
    output = [(prob.id, prob.title, "%.2f" % prob.diff) for prob in problems]
    return render_template("problems.html", probs=output)
