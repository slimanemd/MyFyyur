#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# imorts
from app import db

#
from datetime         import datetime
from sqlalchemy.orm   import relationship, backref

#----------------------------------------------------------------------------#
# Models core.
#----------------------------------------------------------------------------#
# TODO DONE: implement any missing fields, as a database migration using Flask-Migrate DONE
# TODO DONE: Implement Show and Artist models, and complete all model relationships and properties, as a database migration. DONE

#SHOW
class Show(db.Model):
  __tablename__ = 'tshow'
  id            = db.Column(db.Integer, primary_key=True)
  start_time    = db.Column(db.DateTime, default=datetime.utcnow)

  venue_id      = db.Column(db.Integer, db.ForeignKey('tvenue.id'), nullable=False)
  artist_id     = db.Column(db.Integer, db.ForeignKey('tartist.id'), nullable=False)

  #
  def __repr__(self):
      return "[" + str(self.venue_id) + ";" + str(self.artist_id) + ";" + str(self.start_time) + "]"


#----------------------------------------------------------------------------#
#VENUE
class Venar:
    id                  = db.Column(db.Integer,     primary_key=True)
    name                = db.Column(db.String(),    nullable=False, unique=True)
    city                = db.Column(db.String(120), nullable=False)
    state               = db.Column(db.String(120), nullable=False)
    phone               = db.Column(db.String(120), nullable=False)
    genres              = db.Column(db.String(120), nullable=False)    
    image_link          = db.Column(db.String(500))      #, nullable=False)
    facebook_link       = db.Column(db.String(120))      #, nullable=False)
    website             = db.Column(db.String(120))      #, nullable=False)    
    seeking_talent      = db.Column(db.String(120))      #, nullable=False)    
    seeking_description = db.Column(db.String(500))      #, nullable=False
    
    def __repr__(self):
      return "[" + self.name + ";" + self.city + ";" + self.state + "]"



#VENUE
class Venue(db.Model, Venar):
    __tablename__ = 'tvenue'
    '''
    id                  = db.Column(db.Integer,     primary_key=True)
    name                = db.Column(db.String(),    nullable=False, unique=True)
    city                = db.Column(db.String(120), nullable=False)
    state               = db.Column(db.String(120), nullable=False)
    phone               = db.Column(db.String(120), nullable=False)
    genres              = db.Column(db.String(120), nullable=False)    
    image_link          = db.Column(db.String(500))      #, nullable=False)
    facebook_link       = db.Column(db.String(120))      #, nullable=False)
    website             = db.Column(db.String(120))      #, nullable=False)    
    seeking_talent      = db.Column(db.String(120))      #, nullable=False)    
    seeking_description = db.Column(db.String(500))      #, nullable=False
    '''
    address             = db.Column(db.String(120), nullable=False)    

    shows = relationship('Show' , backref=backref("venue", lazy=True))

    '''
    def __repr__(self):
      return "[" + self.name + ";" + self.city + ";" + self.state + "]"
    '''
#----------------------------------------------------------------------------#
# TODO DONE: implement any missing fields, as a database migration using Flask-Migrate DONE
#ARTIST
class Artist(db.Model, Venar):
    __tablename__ = 'tartist'
    '''
    id                  = db.Column(db.Integer,     primary_key=True)
    name                = db.Column(db.String(),    nullable=False, unique=True)
    city                = db.Column(db.String(120), nullable=False)
    state               = db.Column(db.String(120), nullable=False)
    phone               = db.Column(db.String(120), nullable=False)
    genres              = db.Column(db.String(120), nullable=False)        
    image_link          = db.Column(db.String(500))      #, nullable=False)
    facebook_link       = db.Column(db.String(120))      #, nullable=False)
    website             = db.Column(db.String(120))      #, nullable=False)    
    seeking_talent      = db.Column(db.String(120))      #, nullable=False)    
    seeking_description = db.Column(db.String(500))      #, nullable=False
    '''
    #
    shows = relationship('Show' , backref=backref("artist", lazy=True))

    '''
    #
    def __repr__(self):
      return "[" + self.name + ";" + self.city + ";" + self.state + "]"
    '''
#----------------------------------------------------------------------------#
