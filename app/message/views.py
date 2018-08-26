from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from flask_babelex import _
from app import csrf
from .forms import MessageForm, ReplyForm
from ..model import db, User, Message
from ..util import email

# ...
message_blueprint = Blueprint('message_blueprint', __name__)


#
def populate_form_choices(form):
    """
    Pulls choices from the database to populate our select fields.
    """
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.email)
    #choices need to come in the form of a list comprised of enumerated lists
    #example [('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    user_choices = list(enumerate((user_list),1))
    #now that we've built our choices, we need to set them.
    form.recipient.choices = user_choices

@message_blueprint.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm(request.form)
    populate_form_choices(form)
    if form.validate_on_submit():
        user = User.query.filter_by(id =request.form['recipient']).first_or_404()
        msg = Message(sender=current_user, recipient=user, subject=request.form['subject'],\
         body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        msg.parent_id = msg.id
        db.session.commit()
        flash(_('Your message has been sent.'),'success')
        return redirect(url_for('message_blueprint.messages'))
    return render_template('/message/send_message.html', title=_('Send Message'), send_message_form=form)


@message_blueprint.route('/messages')
@login_required
def messages():
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('message_blueprint.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('message_blueprint.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('/message/index.html', messages=messages.items, next_url=next_url, prev_url=prev_url)


@message_blueprint.route('/view/<msg_id>/<parent_id>', methods=['GET', 'POST'])
@login_required
def view_message(msg_id, parent_id):
    current_user.seen_message(msg_id)
    db.session.commit()
    show_messages = Message.query.filter_by(parent_id = parent_id).order_by(Message.timestamp.desc()).all()
    form = ReplyForm(request.form)
    user_msg = Message.query.filter_by(id=msg_id).first_or_404()
    if form.validate_on_submit():
        reply_msg = Message(parent_id=user_msg.id,sender=current_user, recipient_id=user_msg.sender_id,subject=user_msg.subject,\
            body=form.message.data)
        db.session.add(reply_msg)
        db.session.commit()
        flash(_('Your message has been sent.'),'success')
        return redirect(url_for('message_blueprint.view_message', msg_id=msg_id, parent_id=parent_id))

    return render_template('/message/view.html', messages=show_messages, reply_message_form=form, msg_id=msg_id, parent_id=parent_id)



@message_blueprint.route('/send_email', methods=['POST'])
@csrf.exempt
def send_email ():
    check_filed = (request.form['subject'] != '' and request.form['body'] != '' and request.form['emailto'] != '')
    if request.method == 'POST' and check_filed:
        subject = request.form['subject']
        body = request.form['body']
        sender = current_app.config['MAIL_USERNAME']
        recipients = request.form['emailto']
        email( subject, body, sender, recipients)
        flash(_('Your message has been sent.'),'success')
        return redirect(request.referrer)
    else:
        flash(_('Feilds can not be empty'),'danger')
    return redirect(request.referrer)
