from sqlalchemy import event
from src.models.common_models import EntityMixin,ThirdDateLog
from flask import current_app
from src.services import listen_service
from contextlib import contextmanager





@contextmanager
def session_scope(db):
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except (IOError, ValueError) as err:
        session.rollback()
        raise
    finally:
        pass


def row_dict(row):
    result = {c.name: str(getattr(row, c.name)) for c in
              row.__table__.columns}
    return result


# standard decorator style
@event.listens_for(EntityMixin, 'after_insert', propagate=True)
def receive_after_insert(mapper, connection, target):
    print('after_insert-1', target.__tablename__, target.id)
    current_app.logger.debug('------------>'+target.__tablename__+'--------------'+str(target.id))
    listen_service.after_insert(target.__tablename__, target.id)