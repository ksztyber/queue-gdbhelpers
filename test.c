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
#include <bsd/sys/tree.h>

const int MAX_ITEMS = 128;

#define DEFINE_QUEUE_ITEM(type) \
struct type##_item { \
	unsigned int id; \
	type##_ENTRY(type##_item) link; \
	struct { \
		type##_ENTRY(type##_item) link; \
	} inner; \
}; \
type##_HEAD(, type##_item) type##_head = type##_HEAD_INITIALIZER(type##_head); \
type##_HEAD(, type##_item) type##_empty_head = type##_HEAD_INITIALIZER(type##_empty_head); \
type##_HEAD(, type##_item) type##_single_head = type##_HEAD_INITIALIZER(type##_single_head); \
type##_HEAD(, type##_item) type##_inner_head = type##_HEAD_INITIALIZER(type##_inner_head); \
type##_HEAD(, type##_item) type##_inner_empty_head = type##_HEAD_INITIALIZER(type##_inner_empty_head); \
type##_HEAD(, type##_item) type##_inner_single_head = type##_HEAD_INITIALIZER(type##_inner_single_head); \
static void  __attribute__((constructor)) setup_##type(void) { \
	struct type##_item *item; \
	item = calloc(MAX_ITEMS + 1, sizeof(*item)); \
	item->id = MAX_ITEMS; \
	type##_INSERT_HEAD(&type##_single_head, item, link); item++; \
	for (int i = 0; i < MAX_ITEMS; ++i) { \
		item->id = MAX_ITEMS - i; \
		type##_INSERT_HEAD(&type##_head, item, link); \
		item++; \
	} \
	item = calloc(MAX_ITEMS + 1, sizeof(*item)); \
	item->id = MAX_ITEMS; \
	type##_INSERT_HEAD(&type##_inner_single_head, item, inner.link); item++; \
	for (int i = 0; i < MAX_ITEMS; ++i) { \
		item->id = MAX_ITEMS - i; \
		type##_INSERT_HEAD(&type##_inner_head, item, inner.link); \
		item++; \
	} \
}

#define DEFINE_TREE_ITEM(type) \
struct type##_item { \
	unsigned int id; \
	type##_ENTRY(type##_item) link; \
}; \
static int type##_cmp(struct type##_item *a, struct type##_item *b) { \
	return a->id - b->id; \
} \
type##_HEAD(type##_t, type##_item); \
type##_PROTOTYPE(type##_t, type##_item, link, type##_cmp); \
type##_GENERATE(type##_t, type##_item, link, type##_cmp); \
static struct type##_t type##_head = type##_INITIALIZER(type##_head); \
static struct type##_t type##_empty_head = type##_INITIALIZER(type##_empty_head); \
static struct type##_t type##_single_head = type##_INITIALIZER(type##_single_head); \
static void  __attribute__((constructor)) setup_##type(void) { \
	struct type##_item *item; \
	item = calloc(MAX_ITEMS + 1, sizeof(*item)); \
	item->id = MAX_ITEMS; \
	type##_INSERT(type##_t, &type##_single_head, item); item++; \
	for (int i = 1; i <= MAX_ITEMS; ++i) { \
		item->id = i; \
		type##_INSERT(type##_t, &type##_head, item); \
		item++; \
	} \
}

DEFINE_QUEUE_ITEM(LIST);
DEFINE_QUEUE_ITEM(SLIST);
DEFINE_QUEUE_ITEM(STAILQ);
DEFINE_QUEUE_ITEM(SIMPLEQ);
DEFINE_QUEUE_ITEM(TAILQ);
DEFINE_QUEUE_ITEM(CIRCLEQ);
DEFINE_TREE_ITEM(RB);
DEFINE_TREE_ITEM(SPLAY);

int main(void) { return 0; }
