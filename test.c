/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 */

#include <stdlib.h>
#include <sys/queue.h>

const int MAX_ITEMS = 128;

#define DEFINE_ITEM(type) \
struct type##_item { \
	unsigned int id; \
	type##_ENTRY(type##_item) link; \
}; \
type##_HEAD(, type##_item) type##_head = type##_HEAD_INITIALIZER(type##_head); \
type##_HEAD(, type##_item) type##_empty_head = type##_HEAD_INITIALIZER(type##_empty_head); \
type##_HEAD(, type##_item) type##_single_head = type##_HEAD_INITIALIZER(type##_single_head); \
static void  __attribute__((constructor)) setup_##type(void) { \
	struct type##_item *item; \
	item = calloc(MAX_ITEMS + 1, sizeof(*item)); \
	item->id = MAX_ITEMS; \
	type##_INSERT_HEAD(&type##_single_head, item, link); item++; \
	if (!item) abort(); \
	for (int i = 0; i < MAX_ITEMS; ++i) { \
		item->id = MAX_ITEMS - i; \
		type##_INSERT_HEAD(&type##_head, item, link); \
		item++; \
	} \
}

DEFINE_ITEM(LIST);
DEFINE_ITEM(SLIST);
DEFINE_ITEM(STAILQ);
DEFINE_ITEM(SIMPLEQ);
DEFINE_ITEM(TAILQ);
DEFINE_ITEM(CIRCLEQ);

int main(void) { return 0; }
