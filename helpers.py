#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import dateutil.parser
import babel
from app import db, Venue, Artist, Show

from flask import render_template, request, flash, redirect, url_for #Flask, , Response, 
from data import entity_fields, venues00, artists00, shows00
from datetime import datetime
from config import NB_LIMIT

from functools import partial

#----------------------------------------------------------------------------#
# Helpers & Filters.
#----------------------------------------------------------------------------#
#compare two start_time in they in the same day
compare_show_st = lambda p_start_time, show: show.start_time.date() == p_start_time.date()

#get_artist_shows for specific artist
get_artist_shows = lambda p_artist_id :Show.query.filter(Show.artist_id == p_artist_id).all()

#get_nb_shows_st : get number of shows in the same day as start_time
get_nb_shows_st = lambda p_artist_id, p_start_time : len(
  list(filter(partial(compare_show_st,p_start_time), get_artist_shows(p_artist_id))))
  
#format_datetime
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

#helper make key fromc ity and state
def hlp_make_key_01(city, state):
  return city.replace(' ','_') +  '_' + state.replace(' ', '_')

#helper hlp_get_num_upcoming_show
def hlp_get_num_upcoming_show(p_shows):
  l_result = 0
  l_now = datetime.utcnow() #  
  for l_show in p_shows:
    if l_show.start_time > l_now:
      l_result = l_result + 1

  #
  return l_result; 

#helper hlp_format_entity_01
def hlp_format_entity_01(entity):
  return  { 
    'id': entity.id, 
    'name':entity.name, 
    'num_upcoming_shows': hlp_get_num_upcoming_show(entity.shows) 
    }

#helper get_venues_format_01
def get_venues_format_01():
  venues = Venue.query.all()
  rsl = {}
  for venue in venues:
    keys  = rsl.keys()
    key   = hlp_make_key_01(venue.city, venue.state)
    if not key in keys:
      rsl[key] = { 
          "city":venue.city,
          "state":venue.state,
          "venues" :[] }
    rsl[key]['venues'].append(hlp_format_entity_01(venue))
  return rsl.values()

#helper hlp_do_search
def hlp_do_search(Entity,fields, search_term):
  search = "%{}%".format(search_term)
  entities = Entity.query.filter(getattr(Entity, fields[0]).ilike(search)).all()
  return entities

#--------------------------------------------------------------------------#
#artists helper
def get_artists_format_01():
  entity_list = Artist.query.all()
  return [ { 
          "id":entity.id,
          "name":entity.name
        } for entity in entity_list ]

#--------------------------------------------------------------------------#
# Helpers
#--------------------------------------------------------------------------#
#Top N recentlty listed
topN = lambda Entity: Entity.query.order_by('id desc').limit(NB_LIMIT).all()

#fill_entity_from_form: 
def fill_entity_from_form(entity, entity_id, entity_name):  
  if entity_name == 'show':
    entity.artist_id  = int(request.form['artist_id'])
    entity.venue_id   = int(request.form['venue_id'])
    entity.start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')

    entity_data       =   None if entity_id == None else  {'id':entity_id}
  else:
    keys  =  list(request.form.keys())
    for attribute in entity_fields[entity_name]:
      if attribute != 'id' and attribute in keys:
        setattr(entity, attribute , request.form[attribute])

    entity_data =  None if entity_id == None else  {'id':entity_id, 'name':entity.name}
  
  #return entity, entity_data
  return entity_data

#fill_form_from_entity
def fill_form_from_entity(EntityForm, Entity, entity_id, entity_name):
  entity_form = EntityForm()
  entity = Entity.query.get(entity_id)
  if entity:
    for attribute in entity_fields[entity_name]:
      if attribute != 'id' and hasattr(entity_form, attribute):
        entity_form[attribute].data = getattr(entity, attribute)
  return entity_form, {'id':entity.id, 'name': entity.name}

#helper get shows infos
def get_shows_infos():
  shows =  Show.query.all()   #print(shows)
  myshows = []
  for show in shows:
    venue  =  Venue.query.get(show.venue_id)
    artist =  Artist.query.get(show.artist_id)
    show_infos = {
      "id"               : show.id,
      "venue_id"         : show.venue_id,
      "venue_name"       : venue.name,
      "artist_id"        : show.artist_id,
      "artist_name"      : artist.name,
      "artist_image_link": artist.image_link,
      "start_time"       : str(show.start_time)
    }
    myshows.append(show_infos)
  return myshows

#hlp_get_show_entity : show specific entity based on its id
def hlp_get_show_entity(Entity, entity_name, entity_id):
  entity_data = Entity.query.get(entity_id)

  if entity_data and entity_name != 'show':
    setattr(entity_data, 'upcoming_shows_count', 0)
    setattr(entity_data, 'upcoming_shows', [])

    setattr(entity_data, 'past_shows_count', 0)
    setattr(entity_data, 'past_shows', [])    
    
    #
    for show in entity_data.shows:
      Child_Enity = (Artist if entity_name == 'venue' else Venue)
      child_name = ('artist' if entity_name == 'venue' else 'venue')
      artist = Child_Enity.query.get(show.artist_id)

      setattr(show, child_name + '_image_link', artist.image_link)    
      setattr(show, child_name + '_name', artist.name)    
      if show.start_time > datetime.utcnow():
        #print('UP:' + str(show))
        entity_data.upcoming_shows_count += 1
        entity_data.upcoming_shows.append(show)
      else:
        #print('Past' + str(show))
        entity_data.past_shows_count += 1
        entity_data.past_shows.append(show)

  #  
  return entity_data

#--------------------------------------------------------------------------#
# Controller delegautes
#--------------------------------------------------------------------------#
# do_search_entity : search entity using serach terms 
# Challenge: search by city and state  DONE 
def do_search_entity(Entity, entities_name): 
  field = request.form.get('search_field', '')
  results = hlp_do_search(Entity, [field], request.form.get('search_term', ''))
  response = {
    'count' : len(results),
    'data'  : list(map(hlp_format_entity_01, results))
  }

  return render_template('pages/search_' + entities_name + '.html',   #venues
          results     = response,   
          search_term = request.form.get('search_term', ''))

#show_entity : show specific entity based on its id
def show_entity(Entity, entity_name, entity_id):
  entity_data = hlp_get_show_entity(Entity, entity_name, entity_id)  # Entity.query.get(entity_id)
  if entity_data == None : return redirect(url_for('index'))
  return render_template('pages/show_' + entity_name + '.html', entity=entity_data)

# edit_entity : TODO DONE: populate form with values from venue with ID <venue_id>
def edit_entity(EntityForm, Entity, entity_name, entity_id):
  #
  entity_form, entity_data = fill_form_from_entity(EntityForm, Entity, entity_id, entity_name)  #(005)
  return render_template('forms/edit_' + entity_name + '.html', 
                          form = entity_form, 
                          data = entity_data)

# Challenge: artist avaibility  DONE 
#combine the create  + update (edit)
def create_or_edit_entity_submission(EntityForm, Entity, entity_name, entities_name,  entity_id):
  operation = 'create' if entity_id == None else 'update'  #
  entity_form = EntityForm() 
  data_entity = None
  if entity_form.validate_on_submit():

    #if show to create then check the avaibility of the artist before create it
    if entity_name == 'show':
      start_time0 = datetime.strptime(request.form['start_time'],'%Y-%m-%d %H:%M:%S')
      if get_nb_shows_st(request.form['artist_id'],start_time0 ) > 0:
        flash('The artist is not available at this time ' + request.form['start_time'] + '!')
        return render_template('forms/new_show.html', form = entity_form,data = None)

    #instanciated the entity fill its fields with values if the editing
    entity = Entity() if entity_id == None else Entity.query.get(entity_id)   
    data_entity =  fill_entity_from_form(entity, None, entity_name)  #(001)  get_new_entity 003
    
    #persiste the modification
    try:
      if entity_id == None : db.session.add(entity)
      db.session.commit()
      # on successful db insert, flash success
      flash( entity_name + ' was successfully ' + operation + 'd!')
      return redirect(url_for(entities_name))
    except:
      # TODO DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. ' + entity_name + ' could not be ' + operation + '.' + str(entity_form.errors))    
      return render_template('pages/home.html')
  else:
    #for err in form.errors:
    flash(entity_name + ' validation error when ' + operation + ' this item, errors: ' + str(entity_form.errors))    

  #
  return render_template(
      'forms/' + ('new' if entity_id == None else 'edit') + '_' + entity_name + '.html', 
      form = entity_form,
      data = data_entity)

#delete_entity : delete current entity by its id
def delete_entity(Entity, entity_name,  entity_id):
  try:
    Entity.query.filter_by(id=entity_id).delete()
    db.session.commit()
    flash(entity_name + ' Delete ok')
    return redirect(url_for('index'))
  except:
    db.session.rollback()
    flash(entity_name  + ' Delete non ok')
  finally:
    db.session.close()

#--------------------------------------------------------------------------#
# Helpers DB populate
#--------------------------------------------------------------------------#
#populate db one entity
def populate_db_entity(Entity, entity_name, dt_entities):
  entities = []
  for dt_entity in dt_entities:
    entity = Entity()
    for attribute in entity_fields[entity_name]:
      if attribute != 'id' and attribute in dt_entity.keys():
        setattr(entity, attribute , dt_entity[attribute])
    entities.append(entity)

  return entities

#populate db all entities
def populate_db():
  #
  Entity = Venue
  entity_name = 'venue'
  dt_entities = venues00
  venues = populate_db_entity(Entity, entity_name, dt_entities)

  #
  Entity = Artist
  entity_name = 'artist'
  dt_entities = artists00
  artists = populate_db_entity(Entity, entity_name, dt_entities)

  #
  Entity = Show
  entity_name = 'show'
  dt_entities = shows00
  shows = populate_db_entity(Entity, entity_name, dt_entities)

  #
  db.session.add_all(venues)
  db.session.add_all(artists)
  db.session.add_all(shows)
  db.session.commit()
#--------------------------------------------------------------------------#
