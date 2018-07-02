from functools import wraps


def transactional(db):
    """ Decorator factory. """
    # session injector
    def session_injector(func):
        @wraps(func)
        def add_global_session(*args, **kwargs):
            g = func.__globals__
            need_commit = True
            if not hasattr(g, 'db_session'):
                session = db.session()
                g['db_session'] = session
            else:
                session = g['db_session']
                need_commit = False
            try:
                result = func(*args, **kwargs)
                if need_commit:
                    session.commit()
                return result
            except Exception as e:
                if need_commit:
                    session.rollback()
                raise e
            finally:
                pass
        add_global_session.__name__ = func.__name__
        add_global_session.__doc__ = func.__doc__
        return add_global_session
    return session_injector


# just do place holder, if one function without @transactional and refer
# to db_session, it will get None and raise error immediately
db_session = None