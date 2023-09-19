#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from collections import namedtuple
import functools


class Iterator:
    def __init__(self, first, next, head, field):
        self._next = next
        self._first = gdb.parse_and_eval(head)[first]
        self._head = head
        self._field = field
        self._current = None

    def _is_empty(self, entry):
        if entry == gdb.parse_and_eval(self._head).address:
            return True
        if int(str(entry), 16) == 0:
            return True
        return False

    def __iter__(self):
        self._current = None if self._is_empty(self._first) else self._first
        return self

    def __next__(self):
        try:
            if self._current is None:
                raise StopIteration
            current = self._current
            entry = functools.reduce(lambda e, f: e[f], self._field.split('.'),
                                     self._current.dereference())[self._next]
            self._current = None if self._is_empty(entry) else entry
            return current
        except gdb.MemoryError:
            raise StopIteration


def make_iter(head, field):
    Container = namedtuple('Container', ['first', 'next'])
    containers = [Container('lh_first',     'le_next'),
                  Container('slh_first',    'sle_next'),
                  Container('stqh_first',   'stqe_next'),
                  Container('sqh_first',    'sqe_next'),
                  Container('tqh_first',    'tqe_next'),
                  Container('cqh_first',    'cqe_next')]

    headobj = gdb.parse_and_eval(head)

    for c in containers:
        try:
            if headobj[c.first] is not None:
                return Iterator(c.first, c.next, head, field)
        except gdb.error:
            pass

    raise ValueError('Unknown container type')


def return_result(value):
    if type(value) is gdb.Value:
        dereference = '*' if value.type.code == gdb.TYPE_CODE_PTR else ''
        cmd = 'print {}({}){}'.format(dereference, value.type, value)
    else:
        cmd = 'print {}'.format(value)

    gdb.execute(cmd)


class SizeCommand(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, 'queue-size', gdb.COMMAND_DATA,
                             gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)

        if len(arg_list) != 2:
            print('usage: queue-size HEAD FIELD')
            return

        head, field = arg_list
        iter = make_iter(head, field)
        return_result(functools.reduce(lambda v, _: v + 1, iter, 0))


class AtCommand(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, 'queue-at', gdb.COMMAND_DATA,
                             gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)

        if len(arg_list) != 3:
            print('usage: queue-at HEAD FIELD INDEX')
            return

        head, field, index = arg_list
        index = int(str(gdb.parse_and_eval(index)), 10)

        for i, entry in enumerate(make_iter(head, field)):
            if i == index:
                return_result(entry)


SizeCommand()
AtCommand()
