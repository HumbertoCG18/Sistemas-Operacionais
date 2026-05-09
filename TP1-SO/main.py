from parser_asm import parse_asm
from processo import Processo
from simulador import Simulador


def main():
    print("=" * 50)
    print("   SIMULADOR EDF — Sistemas Operacionais")
    print("=" * 50)

    processos = []
    sim = Simulador(processos)

    while True:
        print("\n--- Cadastrar novo processo ---")
        nome = input("Nome do processo (ou 'iniciar' para começar): ").strip()

        if nome.lower() == 'iniciar':
            break

        caminho = input(f"Caminho do arquivo .asm de {nome}: ").strip()
        arrival = int(input("Arrival time (instante de chegada): "))
        ci      = int(input("Ci (tempo de computação): "))
        pi      = int(input("Pi (período = deadline): "))

        instrucoes, variaveis, labels = parse_asm(caminho)

        p = Processo(nome, instrucoes, variaveis, arrival, ci, pi)
        processos.append(p)
        sim.registrar_labels(nome, labels)

        tamanho_memoria = len(instrucoes) + len(variaveis)
        print(f"{nome} cadastrado. Memória: {tamanho_memoria} posição(ões).")

    if not processos:
        print("Nenhum processo cadastrado. Encerrando.")
        return

    print(f"\n Iniciando simulação com {len(processos)} processo(s)...\n")
    sim.rodar()


if __name__ == "__main__":
    main()