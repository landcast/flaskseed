from functools import wraps


def transactional(db):
    """ Decorator factory. """
    # session injector
    def session_injector(func):
        @wraps(func)
        def add_global_session(*args, **kwargs):
            session = db.session()
            g = func.__globals__
            g['db_session'] = session
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


