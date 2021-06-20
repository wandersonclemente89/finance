from flask import Flask

app = Flask(__name__)
app.config['SERVER_NAME'] ='stark-shore-42216.herokuapp.com'
app.config['PREFERRED_URL_SCHEME'] ='https'

from app.controllers import default
from app.controllers import return_of_investiment
from app.controllers import standard_deviation
from app.controllers import beta
from app.controllers import cashflow