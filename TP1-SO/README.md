# TP1 — Simulador EDF de Processos
**Sistemas Operacionais — PUCRS**

Simulador de execução dinâmica de processos com escalonamento **EDF (Earliest Deadline First)**. Os processos são descritos em uma linguagem assembly hipotética baseada em acumulador.

---

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária

Verifique sua versão do Python:
```bash
python --version
```

---

## Estrutura do Projeto

```
tp1-so/
├── main.py           # Ponto de entrada — executa o simulador
├── processo.py       # Classe que representa um processo
├── parser_asm.py     # Lê e interpreta arquivos .asm
├── executor.py       # Executa instruções do assembly
├── escalonador.py    # Política de escalonamento EDF
├── simulador.py      # Loop principal da simulação
└── programas/        # Pasta com os programas .asm de exemplo
    ├── exemplo.asm   # Contador regressivo com impressão na tela
    └── p2.asm        # Contador com loop finito, sem bloqueio
```

---

## Como Executar

Na raiz do projeto, rode:

```bash
python main.py
```

O programa irá solicitar, para cada processo:

| Campo | Descrição | Exemplo |
|---|---|---|
| Nome | Identificador do processo | `P1` |
| Arquivo `.asm` | Caminho do programa assembly | `programas/p1.asm` |
| Arrival time | Instante de chegada na simulação | `0` |
| Ci | Tempo de computação (unidades de tempo) | `5` |
| Pi | Período = Deadline | `10` |

Quando terminar de cadastrar os processos, digite `iniciar` para começar a simulação.

---

## Programas de Exemplo

### `programas/p1.asm`

Contador regressivo que imprime na tela e usa `SYSCALL` (causa bloqueio).

```asm
.code
LOAD variable
ponto1: SUB #1
SYSCALL 1
BRPOS ponto1
SYSCALL 0
.endcode
.data
variable 3
.endcode
```

**O que faz:** carrega o valor 3, subtrai 1 a cada iteração, imprime o resultado e repete enquanto o acumulador for positivo. Ao chegar em 0, encerra.

**Comportamento esperado:** o processo bloqueia a cada `SYSCALL 1` por 1 a 3 unidades de tempo.

---

### `programas/p2.asm`

Contador decrescente sem bloqueio. Ideal para testar preempção pura do EDF.

```asm
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
```

**O que faz:** conta de 5 até 0 armazenando o valor na memória a cada passo. Encerra ao atingir 0.

**Comportamento esperado:** nunca bloqueia — só é interrompido por preempção do EDF.

---

## Como Criar um Programa `.asm`

Um programa válido deve ter duas seções obrigatórias:

```asm
.code
    ; instruções aqui
.endcode
.data
    ; variáveis aqui
.enddata
```

### Instruções disponíveis

**Aritméticas** — operam sobre o acumulador (`acc`):

| Instrução | Efeito |
|---|---|
| `ADD op` | `acc = acc + op` |
| `SUB op` | `acc = acc - op` |
| `MULT op` | `acc = acc * op` |
| `DIV op` | `acc = acc / op` (inteira) |

**Memória:**

| Instrução | Efeito |
|---|---|
| `LOAD op` | `acc = op` |
| `STORE var` | `var = acc` (somente modo direto) |

**Saltos:**

| Instrução | Condição |
|---|---|
| `BRANY label` | Sempre salta |
| `BRPOS label` | Salta se `acc > 0` |
| `BRZERO label` | Salta se `acc = 0` |
| `BRNEG label` | Salta se `acc < 0` |

**Sistema:**

| Instrução | Efeito |
|---|---|
| `SYSCALL 0` | Encerra o processo |
| `SYSCALL 1` | Imprime `acc` na tela (bloqueia 1–3 unidades) |
| `SYSCALL 2` | Lê inteiro do teclado (bloqueia 1–3 unidades) |

### Modos de endereçamento

- **Imediato** (`#valor`): usa o número diretamente. Ex: `ADD #5`
- **Direto** (`nome`): usa o valor da variável. Ex: `ADD contador`

### Labels

Defina um label colocando um nome seguido de `:` antes da instrução:

```asm
loop: SUB #1
      BRPOS loop
```

---

## Exemplo de Sessão Completa

```
python main.py

==================================================
   SIMULADOR EDF — Sistemas Operacionais
==================================================

--- Cadastrar novo processo ---
Nome do processo (ou 'iniciar' para começar): P1
Caminho do arquivo .asm de P1: programas/p1.asm
Arrival time (instante de chegada): 0
Ci (tempo de computação): 5
Pi (período = deadline): 10
P1 cadastrado. Memória: 6 posição(ões).

--- Cadastrar novo processo ---
Nome do processo (ou 'iniciar' para começar): P2
Caminho do arquivo .asm de P2: programas/p2.asm
Arrival time (instante de chegada): 2
Ci (tempo de computação): 3
Pi (período = deadline): 6
P2 cadastrado. Memória: 6 posição(ões).

--- Cadastrar novo processo ---
Nome do processo (ou 'iniciar' para começar): iniciar

Iniciando simulação com 2 processo(s)...

⏱ t=0
  CPU: P1
  [CHEGADA] P1 chegou (deadline=10)
  [ESCALONA] P1 começa a rodar (deadline=10)

⏱ t=2
  CPU: P2
  [CHEGADA] P2 chegou (deadline=8)
  [PREEMPÇÃO] P1 preemptado por P2
  [ESCALONA] P2 começa a rodar (deadline=8)
...
```

---

## Saída da Simulação

Cada unidade de tempo exibe:

- `CPU: <nome>` — processo em execução naquele tick
- `[CHEGADA]` — processo adicionado à fila de prontos
- `[ESCALONA]` — processo começa a usar a CPU
- `[PREEMPÇÃO]` — processo de maior prioridade assume a CPU
- `[SYSCALL 1]` — valor impresso pelo processo
- `[BLOQUEIO]` — processo aguardando retorno de I/O
- `[DESBLOQUEADO]` — processo volta à fila de prontos
- `[PERÍODO]` — processo completou seu `Ci` e inicia novo período
- `[FIM]` — processo encerrou com `SYSCALL 0`
- `DEADLINE PERDIDO` — processo ultrapassou seu deadline

Ao final, é exibido o **Diagrama de Gantt**:

```
DIAGRAMA DE GANTT
  P1 |██░░░█░██
  P2 |░░███░█░░
     |012345678
```

`█` = processo rodando | `░` = processo aguardando ou bloqueado