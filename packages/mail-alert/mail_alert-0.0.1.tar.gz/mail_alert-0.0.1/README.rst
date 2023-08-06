
mailer
======
moniter project and send email when error occur (for python >3)

Installation
============
pip3 install mailer

useage
======
first create a config file named 'mail_settings.py' in your project root path
and add the project root path to your sys.path or PYTHONPATH

*config example*

.. code-block:: py

    server = {
        'name': 'smtp.163.com', # smtp server addr
        'port': 465, # smtp server port
        'user': 'XXXX.com', # email 
        'password': '', # passwd【for 163/qq email this password is not equal to web login       password, it's set by customer in the email config page】
        'ssl': True, # set False if port is not 25
    }

    default = ('y1150264176@163.com', 'yaolu0405@gmail.com') # send to email addr group

    cc = ('y1150264176@163.com', ) # carbon copy addr group


**decorate class**:

monitor all functions in this class and send email when error occur

.. code-block:: pycon

    >>> from mailer import MailAlert
    >>> @MailAlert(to="default", cc="cc")
    >>> class A:
    >>>    def hello(self):
    >>>        1 / 0
    >>>        return 'ss'


**decorate function**:

monitor this decorated function and send email when error occur

.. code-block:: pycon

    >>> from mailer import MailAlert
    >>> class A:
    >>>    @MailAlert(to="default", cc="cc")
    >>>    def hello(self):
    >>>        1 / 0
    >>>        return 'ss'


arguments
=========
the arguments will read from config file mail_settings.py

1、to : sendto email list

2、cc : carbon copy addr group 
