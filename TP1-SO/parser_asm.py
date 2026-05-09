import re

def remover_comentario(linha):
    """
    Remove comentários da linha.
    Comentário: # precedido de espaço e NÃO seguido de dígito ou sinal negativo.
    Exemplos:
        "SUB #1"            → não remove nada      (modo imediato)
        "SYSCALL 1 # msg"   → remove " # msg"
        "SUB #-5 # msg"     → remove " # msg"
    """
    return re.sub(r'\s#(?![0-9\-]).*', '', linha).strip()


def parse_asm(caminho_arquivo):
    """
    Lê um arquivo .asm e retorna:
    - instrucoes : lista de tuplas (mnemônico, operando)
    - variaveis  : dicionário {nome: valor}
    - labels     : dicionário {nome_label: índice_da_instrução}
    """
    instrucoes = []
    variaveis  = {}
    labels     = {}

    with open(caminho_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f.readlines()]
        linhas = [l for l in linhas if l != '']

    # Identifica seções
    idx_code_start = linhas.index('.code')    + 1
    idx_code_end   = linhas.index('.endcode')
    idx_data_start = linhas.index('.data')    + 1
    idx_data_end   = linhas.index('.enddata')

    linhas_code = linhas[idx_code_start:idx_code_end]
    linhas_data = linhas[idx_data_start:idx_data_end]

    # --- Processa área de código ---
    for linha in linhas_code:
        linha = remover_comentario(linha)
        if linha == '':
            continue

        # Verifica se há label (ex: "ponto1: SUB #1")
        if ':' in linha:
            partes     = linha.split(':', 1)
            nome_label = partes[0].strip()
            labels[nome_label] = len(instrucoes)  # índice atual
            linha = partes[1].strip()
            if linha == '':
                continue

        partes    = linha.split()
        mnemonico = partes[0].upper()
        operando  = partes[1] if len(partes) > 1 else None
        instrucoes.append((mnemonico, operando))

    # --- Processa área de dados ---
    for linha in linhas_data:
        linha = remover_comentario(linha)
        if linha == '':
            continue

        partes   = linha.split()
        nome_var = partes[0]
        valor    = int(partes[1])
        variaveis[nome_var] = valor

    return instrucoes, variaveis, labels