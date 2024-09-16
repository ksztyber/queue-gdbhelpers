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
    def __init__(self, head, field, first, next):
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

    def _deref(self, ptr, field):
        entry = functools.reduce(lambda e, f: e[f], self._field.split('.'),
                                 ptr.dereference())[field]
        return None if self._is_empty(entry) else entry

    def __iter__(self):
        self._current = None if self._is_empty(self._first) else self._first
        return self

    def __next__(self):
        try:
            if self._current is None:
                raise StopIteration
            current = self._current
            self._current = self._deref(current, self._next)
            return current
        except gdb.MemoryError:
            raise StopIteration


class TreeIterator(Iterator):
    def __init__(self, head, field, root, left, right):
        super().__init__(head, field, root, None)
        self._left = left
        self._right = right

    def _left_node(self, node):
        return self._deref(node, self._left)

    def _right_node(self, node):
        return self._deref(node, self._right)

    def _next_nodes(self, current):
        if current is None or self._is_empty(current):
            return None
        yield from self._next_nodes(self._left_node(current))
        yield current
        yield from self._next_nodes(self._right_node(current))

    def __iter__(self):
        return self.__next__()

    def __next__(self):
        yield from self._next_nodes(self._first)


def make_iter(head, field):
    Container = namedtuple('Container', ['type', 'head', 'params'])
    containers = [
        Container(Iterator, 'lh_first', ['le_next']),
        Container(Iterator, 'slh_first', ['sle_next']),
        Container(Iterator, 'stqh_first', ['stqe_next']),
        Container(Iterator, 'sqh_first', ['sqe_next']),
        Container(Iterator, 'tqh_first', ['tqe_next']),
        Container(Iterator, 'cqh_first', ['cqe_next']),
        Container(TreeIterator, 'sph_root', ['spe_left', 'spe_right']),
        Container(TreeIterator, 'rbh_root', ['rbe_left', 'rbe_right'])]

    headobj = gdb.parse_and_eval(head)
    for c in containers:
        try:
            if headobj[c.head] is not None:
                return c.type(head, field, c.head, *c.params)
        except gdb.error as err:
            pass
    raise ValueError('Unknown container type')


def print_result(value, expr=None):
    if type(value) is gdb.Value:
        dereference = '*' if value.type.code == gdb.TYPE_CODE_PTR else ''
        expr = f'.{expr}' if expr is not None else ''
        cmd = 'print ({}({}){}){}'.format(dereference, value.type, value, expr)
    else:
        if expr is not None:
            raise ValueError(f'Invalid expression "{expr}" on object of type {type(value)}')
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
        print_result(functools.reduce(lambda v, _: v + 1, iter, 0))


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
                print_result(entry)


class ForeachCommand(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, 'queue-foreach', gdb.COMMAND_DATA,
                             gdb.COMPLETE_SYMBOL, True)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)

        if len(arg_list) not in (2, 3):
            print('usage: queue-foreach HEAD FIELD [EXPR]')
            return

        head, field, expr, *_ = [*arg_list, None]
        for entry in make_iter(head, field):
            print_result(entry, expr)


SizeCommand()
AtCommand()
ForeachCommand()
