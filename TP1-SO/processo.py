class Processo:
    def __init__(self, nome, instrucoes, variaveis, arrival_time, ci, pi):
        # --- Identificação ---
        self.nome = nome

        # --- Programa carregado ---
        self.instrucoes = instrucoes
        self.variaveis  = dict(variaveis)

        # --- Registradores ---
        self.pc  = 0
        self.acc = 0

        # --- Parâmetros de escalonamento ---
        self.arrival_time = arrival_time
        self.ci = ci
        self.pi = pi

        # --- Controle de execução ---
        self.tempo_executado   = 0
        self.deadline_absoluto = arrival_time + pi

        # --- Estado ---
        self.estado = "novo"  # novo | pronto | rodando | bloqueado | finalizado

        # --- Controle de bloqueio ---
        self.tempo_bloqueado = 0