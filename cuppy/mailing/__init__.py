__author__ = 'ephraim'
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


class EmailMessageText(object):
    """ Default email message text class
    """

    def forgot(self):
        """
In the message body, %_url_% is replaced with:
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
In the message body, %_url_% is replaced with:
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


def generic_email_sender(request, recipients,subject,body,sender=None):
    """Generic email sender"""
    mailer = get_mailer(request)
    if not sender:
        sender = 'Contractors Nigeria <info@nairabricks.com>' #Change this email later
    message = Message(subject=subject,
                      sender=sender,
                      recipients=[recipients],
                      html=body)
    mailer.send_to_queue(message)



