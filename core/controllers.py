#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
#imports
from app import app
from core.forms import VenueForm, ArtistForm, ShowForm
from core.models import Venue, Artist, Show
from core.helpers import *
from data.data import entities_infos

#----------------------------------------------------------------------------#
#home
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
  return show_entities({'entities_infos':entities_infos['venue'], 
                        'results': get_entities_format_01('venue') })

#search_venues
@app.route('/venues/search', methods=['POST'])
def search_venues():
  return do_search_entity(Venue, 'venues')

#show_venue
@app.route('/venues/<int:entity_id>')
def show_venue(entity_id):
  return show_entity(Venue, 'venue', entity_id, 'venues')

#create_venue
@app.route('/venues/create', methods=['GET'])
def create_venue():    #
  return create_or_edit_entity(VenueForm, Venue, 'venue', None)

#create_venue_submission
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  return create_or_edit_entity_submission(VenueForm, Venue, 'venue', 'venues',None)

#edit_venue
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  return create_or_edit_entity(VenueForm, Venue, 'venue', venue_id)

#edit_venue_submission
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  return create_or_edit_entity_submission(VenueForm, Venue, 'venue', 'venues',venue_id)

#delete_venue
@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  return delete_entity(Venue, 'venue',  venue_id)

#----------------------------------------------------------------------------#
#  Artists
#----------------------------------------------------------------------------#
#artists
@app.route('/artists')
def artists():
  return show_entities({'entities_infos':entities_infos['artist'], 
                        'results': get_entities_format_01('artist')})

#search_artists
@app.route('/artists/search', methods=['POST'])
def search_artists():
  return do_search_entity(Artist, 'artists')

#show_artist
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  return show_entity(Artist, 'artist', artist_id, 'artists')

#create_artist
@app.route('/artists/create', methods=['GET'])
def create_artist(): 
  return create_or_edit_entity(ArtistForm, Artist, 'artist', None)

#create_artist_submission
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  return create_or_edit_entity_submission(ArtistForm, Artist, 'artist', 'artists', None)

#edit_artist
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  return create_or_edit_entity(ArtistForm, Artist, 'artist', artist_id)

#edit_artist_submission
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  return create_or_edit_entity_submission(ArtistForm, Artist, 'artist', 'artists', artist_id)
  
#delete_artists
@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  delete_entity(Artist, 'artist',  artist_id)
  return None  

#----------------------------------------------------------------------------#
#  Shows
#----------------------------------------------------------------------------#
#shows displays list of shows at /shows
@app.route('/shows')
def shows(): 
  return show_entities({'entities_infos':entities_infos['show'], 
                        'results':get_entities_format_01('show') })
    
#create_show 
@app.route('/shows/create')
def create_show():                                       
  return render_template('forms/form_entity.html', 
                          data={'entity':'show', 'form':ShowForm()})

#create_show_submission
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  return create_or_edit_entity_submission(ShowForm, Show, 'show', 'shows', None)

# delete show 
@app.route('/shows/<int:show_id>/delete')
def delete_show(show_id):
  delete_entity(Show, 'show',  show_id)
  return redirect(url_for('shows'))

#----------------------------------------------------------------------------#
#not_found_error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/error.html', 
      data = {'id':404, 'title':'Sorry ...','description':'There s nothing here!'}), 404

#server_error
@app.errorhandler(500)
def server_error(error):
  return render_template('errors/error.html', 
    data = {'id':500, 'title':'Oops ...','description':'Something went wrong.'}), 500
#----------------------------------------------------------------------------#
