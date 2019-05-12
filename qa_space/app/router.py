from aiohttp import web
from views.index import *
from views.auth_users.login import *
from views.auth_users.sign_up import *
from views.auth_users.edit_profile import *

from views.projects.overview import *
from views.projects.new_project import *
from views.projects.edit_project import *

from views.suites.overview import *
from views.suites.new_suite import *
from views.suites.edit_suite import *

from views.cases.overview import *
from views.cases.new_case import *
from views.cases.edit_case import *
from views.cases.view_case import *

from views.runs.overview import *

from views.results.overview import *

from views.issues.overview import *

from views.integrations.overview import *

from views.config import *

config = Config()
# Define all routes and views here

path_to_static_folder = './static'
routes = [
    # Login
    web.view('/login', LoginView),
    web.view('/sign_up', SignUpView),
    web.view('/edit_profile', EditProfileView),

    # Projects
    web.view('/projects', ProjectsOverviewView),
    web.view('/new_project', NewProjectView),
    web.view('/edit_project', EditProjectView),

    # Suites
    web.view('/suites', SuitesOverviewView),
    web.view('/new_suite', NewSuiteView),
    web.view('/edit_suite', EditSuiteView),

    # Cases
    web.view('/cases', CasesOverviewView),
    web.view('/new_case', NewCaseView),
    web.view('/edit_case', EditCaseView),
    web.view('/view_case', ViewCaseView),

    # Runs
    web.view('/runs', RunsOverviewView),

    # Results
    web.view('/results', ResultsOverviewView),

    # Issues
    web.view('/issues', IssuesOverviewView),

    # Integrations
    web.view('/integrations', IntegrationsOverviewView),

    # Promo
    web.view('/', IndexView),
]

if config.IS_DEBUG:
    # routes.append(web.view('/doc', DocsView)),
    routes.append(web.view('/config', ConfigsView)),
    web.static('/static', path_to_static_folder, show_index=True),
