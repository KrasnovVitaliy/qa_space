from aiohttp import web
# from views.index import *
# from views.auth_users.login import *
# from views.auth_users.sign_up import *
from views.users.profile import *

from views.projects import *
from views.suites import *
from views.cases import *
from views.tags import *

from views.docs import *
from views.config import *

# Define all routes and views here

# path_to_static_folder = './static'
routes = [
    web.view('/projects', ProjectsView),
    web.view('/suites', SuitesView),
    web.view('/cases', CasesView),
    web.view('/tags', TagsView),

    # System
    web.view('/doc', DocsView),
    web.view('/config', ConfigsView),
]

# c8dbb370a340538342e1771b7b288931
