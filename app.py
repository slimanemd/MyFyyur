#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
#
from babel.dates      import format_datetime
from datetime         import datetime

#
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)                      #moment = Moment(app)
app.config.from_object('config')

#----------------------------------------------------------------------------#
db = SQLAlchemy(app)            #migration
migrate = Migrate(app,db)       # TODO DONE: connect to a local postgresql database DONE

#
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
from core.controllers import *
#----------------------------------------------------------------------------#
import core.handlers

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
# Default port:
if __name__ == '__main__':  
  '''
  #print ("Creating database...");   db.create_all()
  '''
  #print ("Populate database...");   populate_db()
  app.run()
#----------------------------------------------------------------------------#