# GDB helpers for sys/queue.h containers

Commands for container inspection:
 - queue-size returning size of the container
 - queue-at returning N-th element from the container

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
```
