from flask import Flask

app = Flask(__name__)

from app.controllers import default
from app.controllers import return_of_investiment
from app.controllers import standard_deviation
from app.controllers import beta
from app.controllers import cashflow