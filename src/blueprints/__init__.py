from functools import wraps


def transactional(db):
    """ Decorator factory. """
    # session injector
    def session_injector(func):
        @wraps(func)
        def add_global_session(*args, **kwargs):
            g = func.__globals__
            if not hasattr(g, 'db_session'):
                session = db.session()
                g['db_session'] = session
            else:
                session = g['db_session']
            try:
                result = func(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
            finally:
                pass
        return add_global_session
    return session_injector


