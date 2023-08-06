from distutils.core import setup

setup(
  name = 'notifhandler',
  packages = ['notifhandler'], # this must be the same as the name above
  version = '0.2',
  description = 'GOR Notification Handler Tool',
  author = 'Ayush Agarwal',
  author_email = 'ayush.a@greyorange.sg',
  url = '', # use the URL to the github repo
  download_url = '', # I'll explain this in a second
  install_requires = ['django'],
  py_modules = ['django'],
  keywords = ['notif-handler', 'notification'], # arbitrary keywords
  classifiers = [],
)
