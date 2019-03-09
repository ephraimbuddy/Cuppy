from pyramid.url import route_url
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


class EmailMessageText(object):
    """ Default email message text class
    """

    def forgot(self):
        """
In the message body, %_url_% is replaced with link:
        """
        return {
                'subject': 'Password reset request received',
                'body': """
A request to reset your password has been received. Please go to
the following URL to change your password:

%_url_%

If you did not make this request, you can safely ignore it.
"""
        }

    def activate(self):
        """
In the message body, %_url_% is replaced with link:
        """
        return {
                'subject': 'Account activation. Please activate your account.',
                'body': """
This site requires account validation. Please follow the link below to
activate your account:

%_url_%

If you did not make this request, you can safely ignore it.
"""
        }

    def activated(self):
        """
        This email is sent when a user verifies the email
        """
        return {
            'subject': 'Account Activated',
            'body': """
                <!DOCTYPE html>
            <html>
             <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Account Activated</title>
            </head>
            <body>
                    <p>Hello {name},</p>
                <p>Your account has been activated</p>
                <p>Thank you for joining us</p>
                </body>
            </html>
            """
        }



def html_email_sender(request, recipients,subject,body,sender=None,extra_headers=None):
    """Generic html email sender"""
    mailer = get_mailer(request)
    message = Message(subject=subject,
                      sender=sender,
                      recipients=[recipients],
                      html=body,extra_headers=extra_headers)
    mailer.send(message)


def non_html_email_sender(request, recipients,subject,body,sender=None,extra_headers=None):
    """Generic Non html email sender"""
    mailer = get_mailer(request)
    message = Message(subject=subject,
                      sender=sender,
                      recipients=[recipients],
                      body=body,extra_headers=extra_headers)
    mailer.send(message)


def email_forgot(request, user, email, token):

    message_class = EmailMessageText()
    message_text = getattr(message_class, 'forgot')()

    message_body = message_text['body'].format(url=route_url('reset_password', request, token=token),
        name=user.name)
    html_email_sender(request, email, message_text['subject'], message_body)


def confirm_email(request, user, email, token):
    message_class = EmailMessageText()
    message_text = getattr(message_class,'activate')()
    message_body = message_text['body'].format(url=route_url('email_activate',request,token =token),
        name = user.name)
    html_email_sender(request, email, message_text['subject'], message_body)


def user_regmail(request, user, email, token):
    message_class = EmailMessageText()
    message_text = getattr(message_class,'activate')()
    message_body = message_text['body'].format(url=route_url('email_activate',request,token=token),
        name = user.name)
    html_email_sender(request, email, message_text['subject'], message_body)


def welcome(request,user):
    message_class = EmailMessageText()
    message_text = getattr(message_class,'activated')()
    message_body = message_text['body'].format(name = user.name)
    html_email_sender(request, user.login.email, message_text['subject'], message_body)


