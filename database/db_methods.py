import uuid
from typing import List

from icecream import ic
from sqlalchemy import func

from .core import db_session


# region get_from_db methods

def db_error_handler(function):
    def wrapper_error_handler(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(e)
            db_session.rollback()

    return wrapper_error_handler


@db_error_handler
def get_from_db_multiple_filter(table_class, identifier_to_value: list = None, get_type='one',
                                all_objects: bool = None, open_session=None):
    """:param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute
    :param get_type - string 'many' or 'one', return object or list of objects
    :param all_objects - return all rows from table\
    :param open_session - leave session open , must be a session"""
    many = 'many'
    one = 'one'
    is_open = False
    inner_session = db_session
    if open_session:
        inner_session = open_session
    objects = None
    if all_objects is True:
        objects = inner_session.query(table_class).all()

        return objects
    if get_type == one:
        obj = inner_session.query(table_class).filter(*identifier_to_value).first()

        return obj
    elif get_type == many:
        objects = inner_session.query(table_class).filter(*identifier_to_value).all()

    return objects


@db_error_handler
def get_from_db_multiple_filter(table_class, open_session, identifier_to_value: list = None, get_type='one',
                                all_objects: bool = None, ):
    """:param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute
    :param get_type - string 'many' or 'one', return object or list of objects
    :param all_objects - return all rows from table\
    :param open_session - leave session open , must be a session"""
    many = 'many'
    one = 'one'
    is_open = False
    objects = None
    if all_objects is True:
        objects = open_session.query(table_class).all()

        return objects
    if get_type == one:
        obj = open_session.query(table_class).filter(*identifier_to_value).first()

        return obj
    elif get_type == many:
        objects = open_session.query(table_class).filter(*identifier_to_value).all()

    return objects


# endregion


# region abstract write

@db_error_handler
def write_obj_to_table(open_session, table_class, identifier_to_value: List = None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    assert isinstance(identifier_to_value, List)
    is_new = False
    if identifier_to_value:
        tab_obj = open_session.query(table_class).filter(*identifier_to_value).first()
    else:
        tab_obj = table_class()
        is_new = True
    # is obj not exist in db, we create them
    if not tab_obj:
        tab_obj = table_class()
        is_new = True
    for col_name, val in column_name_to_value.items():
        tab_obj.__setattr__(col_name, val)
    # if obj created jet, we add his to db
    if is_new:
        open_session.add(tab_obj)
    # else just update
    print('commit {0}'.format(tab_obj))
    open_session.commit()
    return tab_obj


@db_error_handler
def write_objects_to_table(table_class, object_list: List[dict], params_to_dict: list, params_to_db: list,
                           identifier_to_value: List, open_session):
    """column name to value must be exist in table class in columns write objects to db without close connection
    :param table_class - table class
    :param object_list
    :param params_to_dict - keys in object in objects_list
    :param params_to_db - names of attributes in database object
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    :param open_session - leave session open , must be a session
    note that UserStatements.statement is instrumented attribute """
    # get obj

    for dict_obj in object_list:
        is_new = False
        tab_obj = get_from_db_multiple_filter(table_class=table_class, identifier_to_value=identifier_to_value)
        if not tab_obj:
            is_new = True
            tab_obj = table_class()
        for d_value, column in zip(params_to_dict, params_to_db):
            value = dict_obj[d_value]
            tab_obj.__setattr__(column, value)

        # if obj created jet, we add his to db
        if is_new:
            open_session.add(tab_obj)
            open_session.commit()
        else:
            # else just update
            open_session.commit()


# endregion
# region abstract first
@db_error_handler
def first(open_session, table_class) -> object:
    tab_obj = open_session.query(table_class).first()
    return tab_obj


# endregion

# region abstract edit
@db_error_handler
def edit_obj_in_table(open_session, table_class, identifier_to_value: list, **column_name_to_value):
    """edit object in selected table
    :param table_class: select table
    :param column_name_to_value: to value must be exist in table class in columns
    :param open_session: connection to database
    :param identifier_to_value: select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute"""
    # get obj
    tab_obj = open_session.query(table_class).filter(*identifier_to_value).first()

    if tab_obj:
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
    open_session.commit()


# endregion


# region abstract delete from db
@db_error_handler
def delete_obj_from_table(open_session, table_class, identifier_to_value: list):
    """edit object in selected table
    :param table_class: select table
    :param open_session: connection to database
    :param identifier_to_value:  select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements. statement is instrumented attribute"""
    result = open_session.query(table_class).filter(*identifier_to_value).delete()
    ic('affected {} rows'.format(result))
    open_session.commit()
    return True


# endregion


# region arithmetics
@db_error_handler
def get_count(table_class, open_session, identifier_to_value: list = None):
    """get count of objects from custom table using filter (optional)
       :param table_class - select table
       :param open_session - leave session open , must be a session
       :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
       note that UserStatements. statement is instrumented attribute"""
    if identifier_to_value:
        rows = open_session.query(table_class).filter(*identifier_to_value).count()
    else:
        rows = open_session.query(table_class).count()

    return rows


@db_error_handler
def get_by_max(table_class, column, open_session):
    # work on func min
    max_id = open_session.query(func.max(column)).scalar()
    if not isinstance(max_id, int):
        max_id = 0
    assert isinstance(max_id, int)
    row = open_session.query(table_class).filter(column == max_id).first()
    # row = session.query(table_class).filter(func.max(column)).first()
    return row

# endregion
