#----------------------------------------------------------------------------#
# Forms.
#----------------------------------------------------------------------------#
#imports
from app import db
from core.models import Venue, Artist
from data.data import data_state, data_genres

#
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL

#----------------------------------------------------------------------------#
# Show
#----------------------------------------------------------------------------#
class ShowForm(Form):
    artist_id     = StringField  ( 'artist_id')
    venue_id      = StringField  ( 'venue_id' )
    start_time    = DateTimeField( 'start_time', validators=[DataRequired()], default= datetime.today())

    def getFields(self):
        my_iter = iter(self)
        print(next(my_iter).name)

#----------------------------------------------------------------------------#
# Artist  
#----------------------------------------------------------------------------#
class ArtistForm(Form):
    name          = StringField( 'name', validators=[DataRequired()])
    city          = StringField( 'city', validators=[DataRequired()])
    state         = SelectField( 'state', validators=[DataRequired()], choices= data_state )
    genres        = SelectMultipleField( 'genres', validators=[DataRequired()],  choices=data_genres )    
    phone         = StringField( 'phone' )
    image_link    = StringField( 'image_link' )
    facebook_link = StringField( 'facebook_link')  #, validators=[URL()] )

#----------------------------------------------------------------------------#
# Venue # TODO implement enum restriction in genres
#----------------------------------------------------------------------------#
class VenueForm(ArtistForm):
    address       = StringField        ( 'address'      , validators=[DataRequired()])    
#----------------------------------------------------------------------------#
