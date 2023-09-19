# GDB helpers for sys/queue.h containers

Commands for container inspection:
 - queue-size returning size of the container
 - queue-at returning N-th element from the container
 - queue-foreach executing an expression (or just printing) each element of
   the container

## Examples
```
(gdb) source queue.py
(gdb) queue-at LIST_head link 0
$1 = {id = 1, link = {le_next = 0x555555559e48, le_prev = 0x555555558108 <LIST_head>}}
(gdb) queue-size LIST_head link
$2 = 128
(gdb) queue-at CIRCLEQ_head link 15
$3 = {id = 16, link = {cqe_next = 0x55555555cd80, cqe_prev = 0x55555555cdb0}}
(gdb) queue-size CIRCLEQ_head link
$4 = 128
(gdb) queue-foreach LIST_head link
$5 = {id = 1, link = {le_next = 0x555555559318, le_prev = 0x5555555581a8 <LIST_head>}, inner = {link = {le_next = 0x0, le_prev = 0x0}}}
$6 = {id = 2, link = {le_next = 0x5555555592f0, le_prev = 0x555555559348}, inner = {link = {le_next = 0x0, le_prev = 0x0}}}
$7 = {id = 3, link = {le_next = 0x5555555592c8, le_prev = 0x555555559320}, inner = {link = {le_next = 0x0, le_prev = 0x0}}}
$8 = {id = 4, link = {le_next = 0x0, le_prev = 0x5555555592f8}, inner = {link = {le_next = 0x0, le_prev = 0x0}}}
(gdb) queue-foreach LIST_head link link.le_next
$9 = (struct LIST_item *) 0x555555559318
$10 = (struct LIST_item *) 0x5555555592f0
$11 = (struct LIST_item *) 0x5555555592c8
$12 = (struct LIST_item *) 0x0
```
