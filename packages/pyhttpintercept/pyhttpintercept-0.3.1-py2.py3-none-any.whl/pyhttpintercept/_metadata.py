
__module_name__ = u'PyHTTPIntercept'

__version__ = u'0.3.1'

__author__ = u'Oli Davis & Hywel Thomas'
__authorshort__ = u'OWBD_HT'
__authoremail__ = u'oli.davis@me.com, hywel.thomas@mac.com'

__copyright__ = u'Copyright (C) 2016 ' + __author__
__license__ = u'MIT'

__description__ = u'Provides a HTTP Server which can be used to intercept ' \
                  u'and modify API requests/responses for local clients.'

repo_user = u'davisowb'
repo_name = u'pyhttpintercept'
__url__ = u'https://bitbucket.org/{user}/{repo}.git'.format(user=repo_user,
                                                            repo=repo_name)  # Use the url to the git repo
__downloadurl__ = u'https://bitbucket.org/{user}/' \
                  u'{repo}.git/get/{version}.tar'.format(user=repo_user,
                                                         repo=repo_name,
                                                         version=__version__)
