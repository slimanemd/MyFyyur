#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
#
from babel.dates      import format_datetime
from datetime         import datetime

#
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm   import relationship, backref
from flask_migrate    import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)                      #moment = Moment(app)
app.config.from_object('config')

#----------------------------------------------------------------------------#
db = SQLAlchemy(app)

#migration
migrate = Migrate(app,db)
# TODO DONE: connect to a local postgresql database DONE

#----------------------------------------------------------------------------#
# Models.
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
class Venue(db.Model):
    __tablename__ = 'tvenue'

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
    address             = db.Column(db.String(120), nullable=False)    

    shows = relationship('Show' , backref=backref("venue", lazy=True))

    def __repr__(self):
      return "[" + self.name + ";" + self.city + ";" + self.state + "]"

#----------------------------------------------------------------------------#
# TODO DONE: implement any missing fields, as a database migration using Flask-Migrate DONE
#ARTIST
class Artist(db.Model):
    __tablename__ = 'tartist'

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

    #
    shows = relationship('Show' , backref=backref("artist", lazy=True))

    #
    def __repr__(self):
      return "[" + self.name + ";" + self.city + ";" + self.state + "]"

#----------------------------------------------------------------------------#
from forms import *

#----------------------------------------------------------------------------#
from helpers import *

#
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#home  Challenge of displing Venues & Artist sorted in DESC limit to 10 DONE
@app.route('/')
def index():
  recent_venues  = topN(Venue) 
  recent_artists = topN(Artist)
  return render_template('pages/home.html', 
                         data= { 'venues':recent_venues, 'artists': recent_artists})

#----------------------------------------------------------------------------#
#  Venues
#----------------------------------------------------------------------------#
#venues
@app.route('/venues')
def venues():
  # TODO DONE : replace with real venues data.
  data= get_venues_format_01()              
  return render_template('pages/venues.html', areas=data);

#
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO DONE: implement search on artists with partial string search.
  return do_search_entity(Venue, 'venues')

# shows the venue page with the given venue_id
@app.route('/venues/<int:entity_id>')
def show_venue(entity_id):
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  return show_entity(Venue, 'venue', entity_id)

#  Create Venue
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO DONE: insert form data as a new Venue record in the db, instead
  # TODO DONE: modify data to be the data object returned from db insertion
   
  #return create_entity_submission(VenueForm, Venue, 'venue', 'venues')
  return create_or_edit_entity_submission(VenueForm, Venue, 'venue', 'venues',None)

#
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO DONE: populate form with values from venue with ID <venue_id>
  return edit_entity(VenueForm, Venue, 'venue', venue_id)

#
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO DONE: take values from the form submitted, and update existing
  #return edit_entity_submission(VenueForm, Venue, 'venue', 'venues', venue_id)
  return create_or_edit_entity_submission(VenueForm, Venue, 'venue', 'venues',venue_id)

#
@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO DONE: Complete this endpoint for taking a venue_id, and using
  delete_entity(Venue, 'venue',  venue_id)
  return None  

#----------------------------------------------------------------------------#
#  Artists
#----------------------------------------------------------------------------#
@app.route('/artists')
def artists():
  # TODO DONE: replace with real data returned from querying the database
  data= get_artists_format_01()              #artists_data
  return render_template('pages/artists.html', artists=data)

#
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO DONE: implement search on artists with partial string search.
  return do_search_entity(Artist, 'artists')

# shows the venue page with the given venue_id
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  return show_entity(Artist, 'artist', artist_id)

#  Create Artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

# called upon submitting the new artist listing form
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # TODO DONE: insert form data as a new Venue record in the db, instead
  # TODO DONE: modify data to be the data object returned from db insertion
  # TODO DONE: on unsuccessful db insert, flash an error instead.
  return create_or_edit_entity_submission(ArtistForm, Artist, 'artist', 'artists', None)

#  Update
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO DONE: populate form with fields from artist with ID <artist_id>
  return edit_entity(ArtistForm, Artist, 'artist', artist_id)

#
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO DONE: take values from the form submitted, and update existing
  return create_or_edit_entity_submission(ArtistForm, Artist, 'artist', 'artists', artist_id)
  
#
@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO DONE: Complete this endpoint for taking a artist_id, and using
  delete_entity(Artist, 'artist',  artist_id)
  return None  

#----------------------------------------------------------------------------#
#  Shows
#----------------------------------------------------------------------------#
# displays list of shows at /shows
@app.route('/shows')
def shows():
  # TODO DONE: replace with real venues data.
  data = get_shows_infos()
  return render_template('pages/shows.html', shows=data)

# renders form. do not touch.
@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  #form.cartist_id.choices = db.session.query(Artist.id, Artist.name).all()
  #form.cvenue_id.choices = db.session.query(Venue.id, Venue.name).all()
  return render_template('forms/new_show.html', form=form)

# called to create new shows in the db, upon submitting new show listing form
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # TODO DONE: on successful db insert, flash success flash('Show was successfully listed!')
  # TODO DONE: on unsuccessful db insert, flash an error instead.
  return create_or_edit_entity_submission(ShowForm, Show, 'show', 'shows', None)

# displays list of shows at /shows
@app.route('/shows/<int:show_id>/delete')
def delete_show(show_id):
  # TODO DONE: replace with real venues data.
  delete_entity(Show, 'show',  show_id)
  return redirect(url_for('shows'))
#----------------------------------------------------------------------------#
#
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#
@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

#----------------------------------------------------------------------------#
import handlers

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