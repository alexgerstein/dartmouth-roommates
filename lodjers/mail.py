from flask import render_template
from flask.ext.mail import Mail, Message

import logging

mail = Mail()
logger = logging.getLogger('lodjers')

ADMINS = ['support@lodjers.com']


def create_message(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    return msg


def welcome_notification(user):
    logger.info("NEW USER %s" % user.nickname)
    message = create_message("%s, Welcome to lodjers!" % user.nickname.split(" ")[0],
                             ADMINS[0],
                             [user.email],
                             render_template("emails/welcome.txt", user=user),
                             render_template("emails/welcome.html", user=user))

    mail.send(message)


def new_matches_notification(user, recipient):
    logger.info("NEW MATCH %s and %s" % (user.nickname, recipient.nickname))
    message = create_message("%s, You have new potential roommate matches on lodjers!" % recipient.nickname.split(" ")[0],
                             ADMINS[0], [recipient.email],
                             render_template("emails/new_matches.txt",
                                             user=user,
                                             recipient=recipient),
                             render_template("emails/new_matches.html",
                                             user=user,
                                             recipient=recipient))

    mail.send(message)
