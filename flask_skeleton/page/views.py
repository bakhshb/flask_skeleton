from flask import Blueprint, render_template, url_for, abort, request
from datetime import date, datetime
from flask_login import login_required
from ..model import db, Page
import pytz

page_blueprint = Blueprint('page_blueprint', __name__)

@page_blueprint.route('/<path:path>')
@login_required
def view_flatpage (path):
    tz = pytz.timezone(request.cookies.get("time"))
    today = datetime.now(tz)
    page = Page.query.filter_by(url=path).filter(Page.publish == 1).filter((Page.publish_at <= today) | (Page.publish_at =='')).first_or_404()
    return render_template('flatpage/page_template.html',page=page)
