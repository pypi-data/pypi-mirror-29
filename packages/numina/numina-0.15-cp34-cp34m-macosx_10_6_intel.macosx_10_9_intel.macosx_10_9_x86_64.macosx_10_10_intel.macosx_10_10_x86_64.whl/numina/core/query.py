#
# Copyright 2011-2017 Universidad Complutense de Madrid
#
# This file is part of Numina
#
# Numina is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Numina is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Numina.  If not, see <http://www.gnu.org/licenses/>.
#

"""Modify how to query results in the DAL"""


class QueryModifier(object):
    pass


class Result(QueryModifier):
    def __init__(self, mode_field, node=None):
        self.mode_field = mode_field
        self.node = node

        splitm = mode_field.split('.')
        lm = len(splitm)
        if lm == 1:
            mode = None
            field = mode_field
        elif lm == 2:
            mode = splitm[0]
            field = splitm[1]
        else:
            raise ValueError('malformed mode_field %s' % mode_field)
        self.mode = mode
        self.field = field

        super(QueryModifier, self).__init__()


class Ignore(QueryModifier):
    """Ignore this parameter"""
    pass
