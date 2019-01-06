from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.url import route_url


class EmailMessageText(object):
    """ Default email message text class
    """

    def forgot(self):
        """
        In the message body, %_url_% is replaced with:
        """
        return {
            'subject': 'Password reset request received:',
            'body': """
                <!DOCTYPE html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width" />
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <title>Account activation. Please activate your account.</title>
                </head>
                <body>

                <p>Hello {name},</p>
                <p>We have sent you a request to reset your password. Please go to
                the following URL to change your password:</p>

                <a href='{url}'>{url}</a>

                <p>If you did not make this request, you can safely ignore it.</p>

                </body>
                </html>
            """
        }

    def activate(self):
        """
        In the message body, url is replaced with:
        """
        return {
            'subject': 'Verify your email: domore.ng.',
            'body': """
                <!DOCTYPE html>
            <html>
             <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Verify your email address</title>
            </head>
            <body>

                    <p>Hello {name},</p>
                <p>Congratulations and welcome to domore.ng! We are connecting homeowners with professional home service contractors</p>

                <p>Please <a href='{url}'>CLICK HERE</a> to verify your email. If the link above is not opening,
                    please copy and paste the following into your browser:</p>

                        <a href='{url}'>{url}</a>


                    <p><b>Need help?</b><br/>
                    <a href="mailto:help@domore.ng">help@domore.ng</a>
                    </p>

                </body>
            </html>
            """
        }

    def activated(self):
        """
        This email is sent when a user verifies the email
        """
        return {
            'subject': 'Hello from domore.ng',
            'body': """
                <!DOCTYPE html>
            <html>
             <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Hello from domore.ng</title>
            </head>
            <body>

                    <p>Hello {name},</p>
                <p>Welcome to domore.ng, your account has been activated</p>
                <p>Thank you for joining us</p>

                We help you do your home projects by connecting you with the right professionals
                <p>Should you loose access to your account, send an email to help@domore.ng to enable us lock the account pending resolution.</p>

                    <p><b>Support Services</b><br/>
                    <a href="mailto:help@domore.ng">help@domore.ng</a>
                    </p>

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

def mass_email_sender(request, recipients,subject,body,sender=None,extra_headers=None):
    """Generic html email sender"""
    mailer = get_mailer(request)
    message = Message(subject=subject,
                      sender=sender,
                      recipients=recipients,
                      html=body,extra_headers=extra_headers)
    mailer.send(message)


def send_email(request, recipients, subject, body, sender=None):
    """ Sends email message
    """
    mailer = get_mailer(request)
    message = Message(subject=subject,
                      sender=sender,
                      recipients=[recipients],
                      html=body)
    mailer.send(message)

    report_recipients = 'Domore.ng <help@domore.ng>'
    if not report_recipients:
        return

    report_recipients = [s.strip() for s in report_recipients.split(',')]

    # since the config options are interpreted (not raw)
    # the report_subject variable is not easily customizable.
    report_subject = "Registration activity for '%(recipients)s' : %(subject)s"

    report_prefix = 'Attention:'
    if report_prefix:
        report_subject = report_prefix + ' ' + report_subject

    d = { 'recipients': recipients, 'subject': subject }
    report_subject = report_subject % d

    body = "The following registration-related activity occurred: \r\n" + \
        "--------------------------------------------\r\n" + body
    message = Message(subject=report_subject,
                      sender=sender,
                      recipients=report_recipients,
                      html=body)
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
    send_email(request, email, message_text['subject'], message_body)


def welcome(request,user):
    message_class = EmailMessageText()
    message_text = getattr(message_class,'activated')()
    message_body = message_text['body'].format(name = user.name)
    html_email_sender(request, user.login.email, message_text['subject'], message_body)
