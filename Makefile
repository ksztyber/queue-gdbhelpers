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

Q ?= @
app := a.out

all: test.c
	$(Q)$(CC) -g3 test.c

clean:
	$(Q)rm -f $(app)

test: all
	$(Q)gdb -x test.commands $(app) | grep -E "OK|FAIL"

.PHONY: all clean test
