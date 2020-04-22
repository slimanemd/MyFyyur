#
from app import db, Venue, Artist

#
from data import data_state, data_genres
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL

# Show
class ShowForm(Form):
    artist_id     = StringField  ( 'artist_id')
    venue_id      = StringField  ( 'venue_id' )
    start_time    = DateTimeField( 'start_time', validators=[DataRequired()], default= datetime.today())

    def getFields(self):
        my_iter = iter(self)
        print(next(my_iter).name)
    
# Venue # TODO implement enum restriction in genres
class VenueForm(Form):
    name          = StringField        ( 'name'         , validators=[DataRequired()])
    city          = StringField        ( 'city'         , validators=[DataRequired()])
    state         = SelectField        ( 'state'        , validators=[DataRequired()], choices = data_state)
    address       = StringField        ( 'address'      , validators=[DataRequired()])
    genres        = SelectMultipleField( 'genres'       , validators=[DataRequired()], choices= data_genres )
    facebook_link = StringField        ( 'facebook_link')  #, validators=[URL("Plz enter a corrrect URL")])
    phone         = StringField        ( 'phone')
    image_link    = StringField        ( 'image_link')

# Artist  
# # TODO implement validation logic for state phone, 
# # TODO implement enum restriction genres
# # TODO implement enum restriction face
class ArtistForm(Form):
    name          = StringField( 'name', validators=[DataRequired()])
    city          = StringField( 'city', validators=[DataRequired()])
    state         = SelectField( 'state', validators=[DataRequired()], choices= data_state )
    phone         = StringField( 'phone' )
    image_link    = StringField( 'image_link' )
    genres        = SelectMultipleField( 'genres', validators=[DataRequired()],  choices=data_genres )
    facebook_link = StringField( 'facebook_link')  #, validators=[URL()] )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
