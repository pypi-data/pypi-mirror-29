# -*- coding: utf-8 -*-
"""
Copyright François Durand
fradurand@gmail.com

This file is part of Hanabython.

    Hanabython is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Hanabython is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Hanabython.  If not, see <http://www.gnu.org/licenses/>.
"""
from hanabython.Modules.Color import Color
from hanabython.Modules.StringAnsi import StringAnsi


class ColorMulticolor(Color):

    def match(self, clue_color: Color) -> bool:
        """
        Multicolor matches any color clue.

        >>> multicolor = ColorMulticolor(name='Multicolor', symbol='M',
        ...                              print_color=StringAnsi.MAGENTA)
        >>> brown = Color(name='Brown', symbol='N',
        ...               print_color=StringAnsi.BROWN)
        >>> multicolor.match(clue_color=brown)
        True
        """
        return True

    @property
    def is_cluable(self):
        """
        :return: False. It is not allowed to give "multicolor" as a clue.
        """
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
