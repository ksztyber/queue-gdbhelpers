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


class Iterator:
    def __init__(self, first, next):
        self._next = next
        self._first = first

    def _has_next(self, entry, head):
        if entry == gdb.parse_and_eval(head).address:
            return False

        if int(str(entry), 16) == 0:
            return False

        return True

    def first(self, head):
        return gdb.parse_and_eval(head)[self._first]

    def next(self, entry, field):
        return entry.dereference()[field][self._next]

    def size(self, head, field):
        entry = self.first(head)
        count = 0

        try:
            while self._has_next(entry, head):
                entry = self.next(entry, field)
                count += 1
        except gdb.MemoryError:
            pass

        return count

    def at(self, head, field, index):
        entry = self.first(head)

        try:
            while self._has_next(entry, head):
                if index == 0:
                    return entry

                entry = self.next(entry, field)
                index -= 1
        except gdb.MemoryError:
            pass

        return None


def return_result(value):
    if type(value) is gdb.Value:
        dereference = '*' if value.type.code == gdb.TYPE_CODE_PTR else ''
        cmd = 'print {}({}){}'.format(dereference, value.type, value)
    else:
        cmd = 'print {}'.format(value)

    gdb.execute(cmd)


class Command(gdb.Command):
    def __init__(self, container, action, first, next):
        gdb.Command.__init__(self,
                             '{}-{}'.format(container, action),
                             gdb.COMMAND_DATA,
                             gdb.COMPLETE_SYMBOL,
                             True)

        self._name = container
        self._iter = Iterator(first, next)

    def invoke(self, arg, from_tty):
        raise NotImplementedError()


class SizeCommand(Command):
    def __init__(self, name, first, next):
        Command.__init__(self, name, 'size', first, next)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)

        if len(arg_list) != 2:
            print('usage: {}-size HEAD FIELD'.format(self._name))
            return

        return_result(self._iter.size(arg_list[0], arg_list[1]))


class AtCommand(Command):
    def __init__(self, name, first, next):
        Command.__init__(self, name, 'at', first, next)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)

        if len(arg_list) != 3:
            print('usage: {}-at HEAD FIELD INDEX'.format(self._name))
            return

        entry = self._iter.at(arg_list[0], arg_list[1], int(arg_list[2], 10))
        if entry is not None:
            return_result(entry)


Container = namedtuple('Container', ['name', 'first', 'next'])
containers = [Container('list', 'lh_first', 'le_next'),
              Container('slist', 'slh_first', 'sle_next'),
              Container('stailq', 'stqh_first', 'stqe_next'),
              Container('simpleq', 'sqh_first', 'sqe_next'),
              Container('tailq', 'tqh_first', 'tqe_next'),
              Container('circleq', 'cqh_first', 'cqe_next')]


for c in containers:
    SizeCommand(c.name, c.first, c.next)
    AtCommand(c.name, c.first, c.next)
