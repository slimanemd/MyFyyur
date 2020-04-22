from app import db
from core.models import Venue, Artist, Show
from data.data import entity_fields, venues00, artists00, shows00

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
