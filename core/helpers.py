#----------------------------------------------------------------------------#
# Helpers
#----------------------------------------------------------------------------#
#imports
import dateutil.parser
import babel
from app import db
from core.models import Venue, Artist, Show

from config import NB_LIMIT

from flask import render_template, request, flash, redirect, url_for #Flask, , Response, 
from data.data import entity_fields, venues00, artists00, shows00
from datetime import datetime
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
  
#Top N recentlty listed
topN = lambda Entity: Entity.query.order_by('id desc').limit(NB_LIMIT).all()

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

#--------------------------------------------------------------------------#
#artists helper
def get_entities_format_01(p_entity):
  if p_entity == 'artist': return get_artists_format_01()
  if p_entity == 'venue' : return get_venues_format_01()
  if p_entity == 'show'  : return get_shows_format_01()

#get_shows_format_01 helper get shows infos
def get_shows_format_01():
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

#get_artists_format_01 artists helper
def get_artists_format_01():
  entity_list = Artist.query.all()
  return [ { 
          "id":entity.id,
          "name":entity.name
        } for entity in entity_list ]

#helper get_venues_format_01
def get_venues_format_01():
  entity_list = Venue.query.all()
  rsl = {}
  for venue in entity_list:
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
# Helpers
#--------------------------------------------------------------------------#
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
  
  #
  return entity_data

#fill_form_from_entity
def fill_form_from_entity(EntityForm, Entity, entity_id, entity_name):
  entity_form = EntityForm(); data = {'entity_name':entity_name }
  if entity_id != None:
    entity = Entity.query.get(entity_id)
    if entity:
      for attribute in entity_fields[entity_name]:
        if attribute != 'id' and hasattr(entity_form, attribute):
          entity_form[attribute].data = getattr(entity, attribute)
    data = {'id':entity.id, 'name': entity.name, 'entity_name':entity_name}
  
  #
  return entity_form, data

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
#venues
def show_entities(p_entity_infos):
  return render_template('pages/entities.html', data = p_entity_infos );

# do_search_entity : search entity using serach terms Challenge: search by city and state  DONE 
def do_search_entity(Entity, entities_name): 
  field = request.form.get('search_field', '')
  results = hlp_do_search(Entity, [field], request.form.get('search_term', ''))
  search_infos = {
    'results' : {
      'count' : len(results),
      'data'  : list(map(hlp_format_entity_01, results))
    }, 
    'search_term': request.form.get('search_term', '')
  } 

  return render_template('pages/search_entities.html', data = search_infos )

#show_entity : show specific entity based on its id
def show_entity(Entity, entity_name, entity_id, entities_name):
  entity_data = hlp_get_show_entity(Entity, entity_name, entity_id)
  if entity_data == None : return redirect(url_for('index'))
  return render_template('pages/show_entity.html', data={'entity': entity_data, 'entities_name':entities_name})

#create_or_edit_entity
def create_or_edit_entity(EntityForm, Entity, entity_name, entity_id):
  entity_form, entity_data = fill_form_from_entity(EntityForm, Entity, entity_id, entity_name)  #(005)
  return render_template('forms/form_entity.html', data = {'form':entity_form, 'entity':entity_name})

# create_or_edit_entity_submission
def create_or_edit_entity_submission(EntityForm, Entity, entity_name, entities_name,  entity_id):
  operation = 'create' if entity_id == None else 'update'  #
  entity_form = EntityForm();   data_entity = None
  if entity_form.validate_on_submit():

    #if show to create then check the avaibility of the artist before create it
    if entity_name == 'show':
      start_time0 = datetime.strptime(request.form['start_time'],'%Y-%m-%d %H:%M:%S')
      if get_nb_shows_st(request.form['artist_id'],start_time0 ) > 0:
        flash('The artist is not available at this time ' + request.form['start_time'] + '!')
        return render_template('forms/form_entity.html',  data = {'form':entity_form, 'data':None})

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
  return render_template('forms/form_entity.html',  data = {'form':entity_form, 'data':data_entity})

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
  return None
