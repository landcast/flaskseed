from sqlalchemy import event
from src.models.common_models import EntityMixin
from flask import current_app
from src.services import listen_service


# standard decorator style
@event.listens_for(EntityMixin, 'after_insert', propagate=True)
def receive_after_insert(mapper, connection, target):
    print('after_insert-1', target.__tablename__, target.id)
    current_app.logger.debug('after_insert------------>'+target.__tablename__+'--------------'+str(target.id))
    listen_service.after_insert(target.__tablename__, target.id)