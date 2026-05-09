class Escalonador:
    def __init__(self):
        self.fila_prontos     = []
        self.fila_bloqueados  = []
        self.processo_rodando = None

    # ------------------------------------------------------------------
    # ADICIONAR PROCESSO
    # ------------------------------------------------------------------
    def adicionar_processo(self, processo):
        """Coloca um processo novo na fila de prontos."""
        processo.estado = "pronto"
        self.fila_prontos.append(processo)
        self._ordenar_prontos()

    # ------------------------------------------------------------------
    # ORDENAÇÃO EDF
    # ------------------------------------------------------------------
    def _ordenar_prontos(self):
        """
        Ordena pelo deadline absoluto (menor = mais prioritário).
        Isso É o EDF.
        """
        self.fila_prontos.sort(key=lambda p: p.deadline_absoluto)

    # ------------------------------------------------------------------
    # TICK — uma unidade de tempo
    # ------------------------------------------------------------------
    def tick(self, tempo_atual):
        """
        Processa uma unidade de tempo:
        1. Libera processos bloqueados que terminaram sua espera
        2. Verifica preempção
        3. Escala o próximo processo se CPU livre
        """
        eventos = []

        # --- 1. Atualiza processos bloqueados ---
        ainda_bloqueados = []
        for p in self.fila_bloqueados:
            p.tempo_bloqueado -= 1
            if p.tempo_bloqueado <= 0:
                # Saiu do bloqueio → volta para prontos com o MESMO deadline do período
                p.estado = "pronto"
                self.fila_prontos.append(p)
                eventos.append(
                    f"  [DESBLOQUEADO] {p.nome} volta para prontos "
                    f"(deadline={p.deadline_absoluto})"
                )
            else:
                ainda_bloqueados.append(p)

        self.fila_bloqueados = ainda_bloqueados
        self._ordenar_prontos()

        # --- 2. Verifica preempção ---
        if self.processo_rodando and self.fila_prontos:
            mais_prioritario = self.fila_prontos[0]
            if mais_prioritario.deadline_absoluto < self.processo_rodando.deadline_absoluto:
                eventos.append(
                    f"  [PREEMPÇÃO] {self.processo_rodando.nome} preemptado "
                    f"por {mais_prioritario.nome}"
                )
                self.processo_rodando.estado = "pronto"
                self.fila_prontos.append(self.processo_rodando)
                self._ordenar_prontos()
                self.processo_rodando = None

        # --- 3. Escala próximo se CPU livre ---
        if self.processo_rodando is None and self.fila_prontos:
            self.processo_rodando = self.fila_prontos.pop(0)
            self.processo_rodando.estado = "rodando"
            eventos.append(
                f"  [ESCALONA] {self.processo_rodando.nome} começa a rodar "
                f"(deadline={self.processo_rodando.deadline_absoluto})"
            )

        return eventos

    # ------------------------------------------------------------------
    # PÓS-EXECUÇÃO — chamado após executar uma instrução
    # ------------------------------------------------------------------
    def pos_execucao(self, resultado, tempo_atual):
        """
        Atualiza o estado do processo conforme o resultado da instrução.
        """
        p = self.processo_rodando
        eventos = []

        p.tempo_executado += 1

        if resultado == "finalizado":
            eventos.append(f"  [FIM] {p.nome} finalizou no tempo {tempo_atual}")
            self.processo_rodando = None
            p.estado = "finalizado"

        elif resultado == "bloqueado":
            eventos.append(
                f"  [BLOQUEIO] {p.nome} bloqueado por {p.tempo_bloqueado} unidade(s)"
            )
            self.fila_bloqueados.append(p)
            self.processo_rodando = None
            p.estado = "bloqueado"

        elif p.tempo_executado >= p.ci:
            # Completou o Ci do período → volta para prontos com novo deadline
            eventos.append(
                f"  [PERÍODO] {p.nome} completou Ci={p.ci}, volta para prontos"
            )
            p.tempo_executado    = 0
            p.deadline_absoluto += p.pi
            p.estado             = "pronto"
            self.fila_prontos.append(p)
            self._ordenar_prontos()
            self.processo_rodando = None

        return eventos

    # ------------------------------------------------------------------
    # VERIFICA PERDA DE DEADLINE
    # ------------------------------------------------------------------
    def verificar_deadlines(self, tempo_atual):
        alertas = []
        todos = self.fila_prontos + self.fila_bloqueados
        if self.processo_rodando:
            todos.append(self.processo_rodando)

        for p in todos:
            if tempo_atual > p.deadline_absoluto:
                alertas.append(
                    f" DEADLINE PERDIDO: {p.nome} no tempo {tempo_atual} "
                    f"(deadline era {p.deadline_absoluto})"
                )
        return alertas

    # ------------------------------------------------------------------
    # STATUS ATUAL
    # ------------------------------------------------------------------
    def status(self):
        rodando = self.processo_rodando.nome if self.processo_rodando else "—"
        prontos = [p.nome for p in self.fila_prontos]
        bloq    = [f"{p.nome}(+{p.tempo_bloqueado})" for p in self.fila_bloqueados]
        return f"  Rodando: {rodando} | Prontos: {prontos} | Bloqueados: {bloq}"