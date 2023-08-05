# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import

from .cell_link import CellLink
from .hyperlink import Hyperlink
from .image import Image
from .object_value import *
from .duration import Duration
from .predecessor_list import PredecessorList
from .contact_object_value import ContactObjectValue
from .date_object_value import DateObjectValue
from .string_object_value import StringObjectValue
from .number_object_value import NumberObjectValue
from .boolean_object_value import BooleanObjectValue
from ..types import TypedList
from ..util import prep
import json
import logging
import six

class Cell(object):

    """Smartsheet Cell data model."""

    def __init__(self, props=None, base_obj=None):
        """Initialize the Cell model."""
        self._base = None
        if base_obj is not None:
            self._base = base_obj
        self._pre_request_filter = None
        self._log = logging.getLogger(__name__)

        self._column_id = None
        self._column_type = None
        self._conditional_format = None
        self._display_value = None
        self.__format = None
        self._formula = None
        self._hyperlink = None
        self._image = None
        self._link_in_from_cell = None
        self._links_out_to_cells = TypedList(CellLink)
        self._object_value = None
        self._strict = True
        self._value = None
        self._override_validation = False

        if props:
            # account for alternate variable names from raw API response
            if 'columnId' in props:
                self.column_id = props['columnId']
            if 'column_id' in props:
                self.column_id = props['column_id']
            # read only
            if 'columnType' in props:
                self.column_type = props['columnType']
            # read only
            if 'conditionalFormat' in props:
                self.conditional_format = props[
                    'conditionalFormat']
            # read only
            if 'displayValue' in props:
                self.display_value = props['displayValue']
            if 'format' in props:
                self._format = props['format']
            if '_format' in props:
                self._format = props['_format']
            if 'formula' in props:
                self.formula = props['formula']
            if 'hyperlink' in props:
                self.hyperlink = props['hyperlink']
            if 'image' in props:
                self.image = props['image']
            if 'linkInFromCell' in props:
                self.link_in_from_cell = props['linkInFromCell']
            if 'link_in_from_cell' in props:
                self.link_in_from_cell = props[
                    'link_in_from_cell']
            if 'linksOutToCells' in props:
                self.links_out_to_cells = props[
                    'linksOutToCells']
            if 'links_out_to_cells' in props:
                self.links_out_to_cells = props[
                    'links_out_to_cells']
            if 'objectValue' in props:
                self.object_value = props['objectValue']
            if 'object_value' in props:
                self.object_value = props['object_value']
            if 'strict' in props:
                self.strict = props['strict']
            if 'value' in props:
                self.value = props['value']
            if 'overrideValidation' in props:
                self.override_validation = props['overrideValidation']
            if 'override_validation' in props:
                self.override_validation = props['override_validation']
        self.__initialized = True

    def __getattr__(self, key):
        if key == 'format':
            return self._format
        else:
            raise AttributeError(key)

    @property
    def column_id(self):
        return self._column_id

    @column_id.setter
    def column_id(self, value):
        if isinstance(value, six.integer_types):
            self._column_id = value

    @property
    def column_type(self):
        return self._column_type

    @column_type.setter
    def column_type(self, value):
        if isinstance(value, six.string_types):
            self._column_type = value

    @property
    def conditional_format(self):
        return self._conditional_format

    @conditional_format.setter
    def conditional_format(self, value):
        if isinstance(value, six.string_types):
            self._conditional_format = value

    @property
    def display_value(self):
        return self._display_value

    @display_value.setter
    def display_value(self, value):
        if isinstance(value, six.string_types):
            self._display_value = value

    @property
    def _format(self):
        return self.__format

    @_format.setter
    def _format(self, value):
        if isinstance(value, six.string_types):
            self.__format = value

    @property
    def formula(self):
        return self._formula

    @formula.setter
    def formula(self, value):
        if isinstance(value, six.string_types):
            self._formula = value

    @property
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, value):
        if isinstance(value, Hyperlink):
            self._hyperlink = value
        else:
            self._hyperlink = Hyperlink(value, self._base)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if isinstance(value, Image):
            self._image = value
        else:
            self._image = Image(value, self._base)

    @property
    def link_in_from_cell(self):
        return self._link_in_from_cell

    @link_in_from_cell.setter
    def link_in_from_cell(self, value):
        if isinstance(value, CellLink):
            self._link_in_from_cell = value
        else:
            self._link_in_from_cell = CellLink(value, self._base)

    @property
    def links_out_to_cells(self):
        return self._links_out_to_cells

    @links_out_to_cells.setter
    def links_out_to_cells(self, value):
        if isinstance(value, list):
            self._links_out_to_cells.purge()
            self._links_out_to_cells.extend([
                 (CellLink(x, self._base)
                  if not isinstance(x, CellLink) else x) for x in value
             ])
        elif isinstance(value, TypedList):
            self._links_out_to_cells.purge()
            self._links_out_to_cells = value.to_list()
        elif isinstance(value, CellLink):
            self._links_out_to_cells.purge()
            self._links_out_to_cells.append(value)

    @property
    def object_value(self):
        return self._object_value

    @object_value.setter
    def object_value(self, value):
        if isinstance(value, ObjectValue):
            self._object_value = value
        elif isinstance(value, dict):
            object_type = value['objectType']
            if object_type in OBJECT_VALUE['object_type']:
                enum_object_type = enum_object_value_type(object_type)
                if enum_object_type == DURATION:
                    self._object_value = Duration(value, self._base)
                elif enum_object_type == PREDECESSOR_LIST:
                    self._object_value = PredecessorList(value, self._base)
                elif enum_object_type == CONTACT:
                    self._object_value = ContactObjectValue(value, self._base)
                elif enum_object_type == DATE or enum_object_type == DATETIME or enum_object_type == ABSTRACT_DATETIME:
                    self._object_value = DateObjectValue(value, enum_object_value_type, self._base)
                else:
                    self._object_value = None
            else:
                raise ValueError(
                    ("`{0}` is an invalid value for ObjectValue`object_type`,"
                     " must be one of {1}").format(
                        object_type, OBJECT_VALUE['object_type']))
        elif isinstance(value, six.string_types):
            self._object_value = StringObjectValue(value)
        elif isinstance(value, (six.integer_types, float)):
            self._object_value = NumberObjectValue(value)
        elif isinstance(value, bool):
            self._object_value = BooleanObjectValue(value)

    @property
    def strict(self):
        return self._strict

    @strict.setter
    def strict(self, value):
        if isinstance(value, bool):
            self._strict = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (six.string_types, six.integer_types, float, bool)):
            self._value = value

    @property
    def override_validation(self):
        return self._override_validation

    @override_validation.setter
    def override_validation(self, value):
        if isinstance(value, bool):
            self._override_validation = value

    @property
    def pre_request_filter(self):
        return self._pre_request_filter

    @pre_request_filter.setter
    def pre_request_filter(self, value):
        if self.hyperlink is not None:
            self.hyperlink.pre_request_filter = value
        if self.link_in_from_cell is not None:
            self.link_in_from_cell.pre_request_filter = value
        for item in self.links_out_to_cells:
            item.pre_request_filter = value
        if self.object_value is not None:
            self.object_value.pre_request_filter = value
        self._pre_request_filter = value

    def to_dict(self, op_id=None, method=None):
        req_filter = self.pre_request_filter
        if req_filter:
            if self.hyperlink is not None:
                self.hyperlink.pre_request_filter = req_filter
            if self.link_in_from_cell is not None:
                self.link_in_from_cell.pre_request_filter = req_filter
            for item in self.links_out_to_cells:
                item.pre_request_filter = req_filter
            if self.object_value is not None:
                self.object_value.pre_request_filter = req_filter

        obj = {
            'columnId': prep(self._column_id),
            'columnType': prep(self._column_type),
            'conditionalFormat': prep(self._conditional_format),
            'displayValue': prep(self._display_value),
            'format': prep(self.__format),
            'formula': prep(self._formula),
            'hyperlink': prep(self._hyperlink),
            'image': prep(self._image),
            'linkInFromCell': prep(self._link_in_from_cell),
            'linksOutToCells': prep(self._links_out_to_cells),
            'objectValue': prep(self._object_value),
            'strict': prep(self._strict),
            'value': prep(self._value),
            'overrideValidation': prep(self._override_validation)}
        return self._apply_pre_request_filter(obj)

    def _apply_pre_request_filter(self, obj):
        if self.pre_request_filter == 'add_rows':
            permitted = ['columnId', 'value', 'objectValue', 'formula', 'strict',
                         'format', 'hyperlink', 'overrideValidation']
            # make formula, objectValue and value mutually exclusive
            if self.formula is not None:
                del obj['value']
                del obj['objectValue']
            elif self.object_value is not None:
                del obj['formula']
                del obj['value']
            else:
                del obj['formula']
                del obj['objectValue']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        if self.pre_request_filter == 'update_rows':
            if self._link_in_from_cell is not None:
                obj['value'] = None
                permitted = ['columnId', 'value', 'linkInFromCell']
            else:
                permitted = ['columnId', 'value', 'objectValue', 'formula', 'strict',
                             'format', 'hyperlink', 'overrideValidation']
                # make formula, objectValue and value mutually exclusive
                if self.formula is not None:
                    del obj['value']
                    del obj['objectValue']
                elif self.object_value is not None:
                    del obj['formula']
                    del obj['value']
                else:
                    del obj['formula']
                    del obj['objectValue']
            all_keys = list(obj.keys())
            for key in all_keys:
                if key not in permitted:
                    self._log.debug(
                        'deleting %s from obj (filter: %s)',
                        key, self.pre_request_filter)
                    del obj[key]

        return obj

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self):
        return json.dumps(self.to_dict())
