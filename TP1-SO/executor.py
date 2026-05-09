import random

def executar_instrucao(processo, labels):
    """
    Executa a instrução apontada pelo pc do processo.

    Retorna: (status, mensagens)
      - status   → "ok" | "bloqueado" | "finalizado"
      - mensagens → lista de strings para exibir no terminal
    """
    instrucao         = processo.instrucoes[processo.pc]
    mnemonico, operando = instrucao
    mensagens         = []

    def resolver_operando(op):
        """
        Modo imediato (#5)  → retorna o número diretamente.
        Modo direto (var)   → busca o valor na área de dados.
        """
        if op.startswith('#'):
            return int(op[1:])
        else:
            return processo.variaveis[op]

    # --- Aritméticas ---
    if mnemonico == 'LOAD':
        processo.acc = resolver_operando(operando)
        processo.pc += 1

    elif mnemonico == 'STORE':
        processo.variaveis[operando] = processo.acc
        processo.pc += 1

    elif mnemonico == 'ADD':
        processo.acc += resolver_operando(operando)
        processo.pc += 1

    elif mnemonico == 'SUB':
        processo.acc -= resolver_operando(operando)
        processo.pc += 1

    elif mnemonico == 'MULT':
        processo.acc *= resolver_operando(operando)
        processo.pc += 1

    elif mnemonico == 'DIV':
        processo.acc //= resolver_operando(operando)
        processo.pc += 1

    # --- Saltos ---
    elif mnemonico == 'BRANY':
        processo.pc = labels[operando]

    elif mnemonico == 'BRPOS':
        if processo.acc > 0:
            processo.pc = labels[operando]
        else:
            processo.pc += 1

    elif mnemonico == 'BRZERO':
        if processo.acc == 0:
            processo.pc = labels[operando]
        else:
            processo.pc += 1

    elif mnemonico == 'BRNEG':
        if processo.acc < 0:
            processo.pc = labels[operando]
        else:
            processo.pc += 1

    # --- Sistema ---
    elif mnemonico == 'SYSCALL':
        index = int(operando)

        if index == 0:
            # Fim do programa
            processo.pc += 1
            return "finalizado", mensagens

        elif index == 1:
            # Imprime acc
            mensagens.append(f"  [SYSCALL 1] {processo.nome} imprime: {processo.acc}")
            processo.tempo_bloqueado = random.randint(1, 3)
            processo.pc += 1
            return "bloqueado", mensagens

        elif index == 2:
            # Lê inteiro do teclado
            valor = int(input(f"  [SYSCALL 2] {processo.nome} aguarda entrada: "))
            processo.acc = valor
            mensagens.append(f"  [SYSCALL 2] {processo.nome} leu: {valor}")
            processo.tempo_bloqueado = random.randint(1, 3)
            processo.pc += 1
            return "bloqueado", mensagens

    return "ok", mensagens