.code
LOAD contador
ponto2: SUB #1
STORE contador
BRPOS ponto2
SYSCALL 0
.endcode
.data
contador 5
.enddata