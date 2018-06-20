from flask import current_app
from src.models import db, session_scope


def do_query(params, generate_sql):
    current_app.logger.debug(params)
    with session_scope(db) as session:
        columns, sql = generate_sql(params)
        current_app.logger.debug(sql)
        result = session.execute(sql, params)
        # default page_no to 1
        page_no = 1
        if params['page_no']:
            page_no = params['page_no']
        # default page_limit to 10 records per page
        page_limit = 10
        if params['page_limit']:
            page_limit = params['page_limit']
        # calculate offset
        offset = (page_no - 1) * page_limit
        rows = result.fetchall()
        row_count = len(rows)
        total_pages = row_count // page_limit
        if row_count % page_limit != 0:
            total_pages = total_pages + 1
        final_result = {
            'objects': [], 'num_results': row_count, 'page': page_no,
            'total_pages': total_pages
        }
        for index, row in enumerate(rows):
            current_app.logger.debug('row ' + str(index) + ' = ' + str(row))
            if (offset + page_limit) > index >= offset:
                final_result['objects'].append(dict((c, v) for c, v in
                                                    zip(columns, row)))
        return final_result


def datetime_param_sql_format(params, datetime_keys):
    for key in datetime_keys:
        if key in params.keys():
            params[key] = params[key].replace('T', ' ').replace('Z', '')
    return params
