from excel_to_json.column import Column, parse_column
from excel_to_json.decorator import Decorator, parse_decorator


class WorkSheet:
    def __init__(self, name):
        self._name = name
        self._is_object = False
        self._json_data = []
        self._hooks = {}
        self._ref = {}

    @property
    def json_data(self):
        return self._json_data

    @property
    def name(self):
        return self._name

    @property
    def short_name(self):
        return self._name[self._name.rindex('#')+1:] if '#' in self._name else self._name

    @property
    def parent_sheet_name(self):
        return self._name[:self._name.rindex('#')]

    @property
    def refs(self):
        return self._ref

    @property
    def hooks(self):
        return self._hooks

    @property
    def is_object(self):
        return self._is_object

    @property
    def is_root_sheet(self):
        return '#' not in self.name and self.name.endswith('.json')

    def is_child_of(self, parent_name):
        return self.name != parent_name and \
               self.name.startswith(parent_name) and \
               ('#' not in self.name[len(parent_name) + 1:])

    def add_object(self, row_index, object_name, attr_name, value):
        while len(self._json_data) <= row_index:
            self._json_data.append({})
        if object_name not in self._json_data[row_index]:
            self._json_data[row_index][object_name] = {}
        self._json_data[row_index][object_name][attr_name] = value

    def add_attribute(self, row_index, key, value):
        while len(self._json_data) <= row_index:
            self._json_data.append({})
        self._json_data[row_index][key] = value

    def add_array(self, row_index, array_name, array):
        array = list(filter(lambda e: e, array))
        assert type(array) is list
        self.add_attribute(row_index, array_name, array)

    def add_object_array(self, row_index, array_name, attr_name, value):
        while len(self._json_data) <= row_index:
            self._json_data.append({})
        obj = self._json_data[row_index]
        if array_name not in obj:
            obj[array_name] = []
        array = obj[array_name]
        elem = None
        if len(array) == 0:
            elem = {}
            array.append(elem)
        else:
            elem = array[-1]
            if attr_name in elem:
                elem = {}
                array.append(elem)
        elem[attr_name] = value

    def add_hook(self, row_index, hook_name):
        if hook_name in self._hooks:
            print('warning: exist same hook name: %s, in sheet: %s' % (hook_name, self.name))
        self._hooks[hook_name] = row_index

    def add_ref(self, row_index, ref_name):
        if ref_name not in self._ref:
            self._ref[ref_name] = []
        ref_rows = self._ref[ref_name]
        if row_index not in ref_rows:
            ref_rows.append(row_index)

    def parse(self, sheet):
        first_row = next(sheet.rows, None)
        if first_row:
            tag_object = filter(lambda r: parse_decorator(r.value) == Decorator.Object, first_row)
            self._is_object = next(tag_object, None) is not None

            for column in sheet.columns:
                column_define = column[0]
                column_type = parse_column(column_define.value)
                if column_type == Column.Empty:
                    continue
                row_index = 0
                for data_cell in column[1:]:
                    # can not skip empty value cell, object_array data need column to check whether add new object.
                    data_value = "" if data_cell.value is None else data_cell.value;
                    if column_type is Column.Attribute:
                        self.add_attribute(row_index, column_define.value, data_value)
                    elif column_type == Column.Object:
                        # todo: check validation format
                        object_define = column_define.value.split('.')
                        object_name = object_define[0]
                        attr_name = object_define[1]
                        self.add_object(row_index, object_name, attr_name, data_value)
                    elif column_type == Column.Array:
                        # todo: check validation format
                        index_of_tag = column_define.value.index('@')
                        array_name = column_define.value[:index_of_tag]
                        array_separator = column_define.value[index_of_tag + 1:]
                        if not array_separator:
                            array_separator = ','
                        data_array = map(lambda e: int(e) if e.isdigit() else e, data_value.split(array_separator))
                        self.add_array(row_index, array_name, data_array)
                    elif column_type == Column.ObjectArray:
                        # todo: check validation format
                        index_of_tag = column_define.value.index('@.')
                        array_name = column_define.value[:index_of_tag]
                        attr_name = column_define.value[index_of_tag + 2:]
                        self.add_object_array(row_index, array_name, attr_name, data_value)
                    elif column_type == Column.Decorator:
                        decorator_type = parse_decorator(column_define.value)
                        if decorator_type == Decorator.Hook:
                            self.add_hook(row_index, data_value)
                        elif decorator_type == Decorator.Ref:
                            self.add_ref(row_index, data_value)
                    row_index = row_index + 1
