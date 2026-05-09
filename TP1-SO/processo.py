# processo.py

class Processo:
    def __init__(self, nome, instrucoes, variaveis, arrival_time, ci, pi):
        # --- Identificação ---
        self.nome = nome                  # Nome do processo (ex: "P1")

        # --- Programa carregado ---
        self.instrucoes = instrucoes      # Lista de instruções da área .code
        self.variaveis = dict(variaveis)  # Dicionário: {"variavel": valor}

        # --- Registradores (estado interno da CPU) ---
        self.pc = 0                       # Ponteiro de instrução (começa na instrução 0)
        self.acc = 0                      # Acumulador (começa em 0)

        # --- Parâmetros de escalonamento ---
        self.arrival_time = arrival_time  # Instante em que o processo chega
        self.ci = ci                      # Tempo de computação (Ci)
        self.pi = pi                      # Período = Deadline (Pi)

        # --- Controle de execução ---
        self.tempo_executado = 0          # Quanto tempo já rodou no período atual
        self.deadline_absoluto = arrival_time + pi  # Primeiro deadline

        # --- Estado do processo ---
        self.estado = "novo"              # novo | pronto | rodando | bloqueado | finalizado

        # --- Controle de bloqueio ---
        self.tempo_bloqueado = 0          # Quantas unidades de tempo ainda fica bloqueado