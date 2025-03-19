```
joo@Jo:/mnt/d/ccc/ccc113bSp/_sp/HW4$ gcc -std=c99 mul3main.c mul3.s
mul3.s: Assembler messages:
mul3.s:7: Warning: end of file not at end of a line; newline inserted
/usr/bin/ld: warning: /tmp/ccctcU9a.o: missing .note.GNU-stack section implies executable stack
/usr/bin/ld: NOTE: This behaviour is deprecated and will be removed in a future version of the linker
joo@Jo:/mnt/d/ccc/ccc113bSp/_sp/HW4$ ./a.out
mul3(3,2,5)=30
```
#執行gcc -o3會優化，加上-o3優化