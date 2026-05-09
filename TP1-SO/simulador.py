from escalonador import Escalonador
from executor import executar_instrucao


class Simulador:
    def __init__(self, processos, tempo_maximo=100):
        """
        processos     → lista de objetos Processo
        tempo_maximo  → limite de segurança para o loop
        """
        self.processos    = processos
        self.escalonador  = Escalonador()
        self.tempo_maximo = tempo_maximo
        self.tempo_atual  = 0
        self.historico    = []               # lista de (tempo, nome_rodando)
        self.labels_por_processo = {}

    def registrar_labels(self, nome_processo, labels):
        """Associa o dicionário de labels ao nome do processo."""
        self.labels_por_processo[nome_processo] = labels

    def rodar(self):
        """Loop principal da simulação."""
        processos_pendentes = sorted(self.processos, key=lambda p: p.arrival_time)

        while self.tempo_atual <= self.tempo_maximo:
            eventos_tick = []

            # --- 1. Chegadas ---
            chegaram = [p for p in processos_pendentes
                        if p.arrival_time == self.tempo_atual]
            for p in chegaram:
                self.escalonador.adicionar_processo(p)
                processos_pendentes.remove(p)
                eventos_tick.append(
                    f"  [CHEGADA] {p.nome} chegou (deadline={p.deadline_absoluto})"
                )

            # --- 2. Tick do escalonador ---
            eventos_tick += self.escalonador.tick(self.tempo_atual)

            # --- 3. Captura quem está rodando ANTES de executar (para exibição correta) ---
            rodando_nome = "—"
            if self.escalonador.processo_rodando:
                rodando_nome = self.escalonador.processo_rodando.nome

            # --- 4. Imprime cabeçalho do tick ANTES da execução ---
            print(f"\n⏱ t={self.tempo_atual}")
            print(f"  CPU: {rodando_nome}")
            for e in eventos_tick:
                print(e)

            # --- 5. Executa 1 instrução e imprime na ordem correta ---
            if self.escalonador.processo_rodando:
                p      = self.escalonador.processo_rodando
                labels = self.labels_por_processo.get(p.nome, {})

                resultado, mensagens_exec = executar_instrucao(p, labels)

                for m in mensagens_exec:
                    print(m)

                eventos_pos = self.escalonador.pos_execucao(resultado, self.tempo_atual)
                for e in eventos_pos:
                    print(e)

            # --- 6. Verifica perda de deadline ---
            alertas = self.escalonador.verificar_deadlines(self.tempo_atual)
            for a in alertas:
                print(a)

            # --- 7. Salva histórico para o Gantt ---
            self.historico.append((self.tempo_atual, rodando_nome))

            self.tempo_atual += 1

            # --- Condição de parada ---
            sem_pendentes  = len(processos_pendentes) == 0
            sem_prontos    = len(self.escalonador.fila_prontos) == 0
            sem_bloqueados = len(self.escalonador.fila_bloqueados) == 0
            sem_rodando    = self.escalonador.processo_rodando is None

            if sem_pendentes and sem_prontos and sem_bloqueados and sem_rodando:
                print(f"\n Simulação encerrada no tempo {self.tempo_atual}")
                break

        self._exibir_resumo()

    def _exibir_resumo(self):
        """Exibe o diagrama de Gantt simplificado."""
        print("\n" + "=" * 50)
        print("DIAGRAMA DE GANTT")
        print("=" * 50)

        nomes = list(dict.fromkeys(n for _, n in self.historico if n != "—"))

        for nome in nomes:
            linha = f"{nome:>4} |"
            for _, rodando in self.historico:
                linha += "█" if rodando == nome else "░"
            print(linha)

        tempo_linha = "     |" + "".join(str(t % 10) for t, _ in self.historico)
        print(tempo_linha)
        print("=" * 50)