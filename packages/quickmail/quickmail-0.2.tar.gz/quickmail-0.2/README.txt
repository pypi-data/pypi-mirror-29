send email with one line, currently just sending with gmail
you need a local_settings.py in the root of the virtualenv with this:

#gmail settings
gmail_user='you@yourdomain.com'
gmail_pass='yourpass'
error_recipient='you@somedomain.com, friend@anotherdomain.com'

