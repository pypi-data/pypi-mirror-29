from enum import Enum


class Column(Enum):
    Empty = 1
    Decorator = 2
    Attribute = 3
    Object = 4
    Array  = 5
    ObjectArray = 6


def parse_column(column_define):
    column_type = Column.Attribute
    if not column_define:
        column_type = Column.Empty
    elif column_define.startswith('#'):
        column_type = Column.Decorator
    elif '@.' in column_define:
        column_type = Column.ObjectArray
    elif '.' in column_define:
        column_type = Column.Object
    elif '@' in column_define:
        column_type = Column.Array
    return column_type
