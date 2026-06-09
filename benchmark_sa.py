# benchmark_sa.py
# -----------------------------------------------------------------------------
# Script de benchmark para o trabalho "Pac-Man: Way of the Katana" (MATA64).
#
# Objetivo: medir, de forma reproduzivel, como os hiperparametros do Simulated
# Annealing (T inicial, alpha e Tmin) afetam:
#   - a taxa de sucesso (quantas execucoes chegam ao objetivo),
#   - a qualidade do caminho (numero de passos ate a meta),
#   - o custo computacional (iteracoes e reaquecimentos),
#   - o tempo de execucao.
#
# Como o algoritmo e estocatico (usa sorteios), uma unica execucao nao e
# representativa. Por isso, cada configuracao e rodada varias vezes (TRIALS) e
# reportamos a media. Essa e a metodologia usada para gerar a tabela do Slide 4.
#
# Como rodar (a partir da pasta do projeto, junto do pacman.py):
#     python3 benchmark_sa.py
#
# Opcional: trocar o labirinto ou o numero de repeticoes la no final do arquivo.
# -----------------------------------------------------------------------------

import time

import layout
import pacman
import searchAgents
import search
from game import Actions


def build_problem(layout_name):
    """Cria um PositionSearchProblem para o labirinto pedido."""
    lay = layout.getLayout(layout_name)
    if lay is None:
        raise ValueError("Layout nao encontrado: %s" % layout_name)
    game_state = pacman.GameState()
    game_state.initialize(lay, 0)
    return searchAgents.PositionSearchProblem(
        game_state, warn=False, visualize=False)


def path_reaches_goal(problem, actions):
    """Reexecuta a sequencia de acoes e confere se termina no objetivo
    (e se nenhum passo atravessa parede)."""
    x, y = problem.getStartState()
    for a in actions:
        dx, dy = Actions.directionToVector(a)
        nx, ny = int(x + dx), int(y + dy)
        if problem.walls[nx][ny]:
            return False
        x, y = nx, ny
    return (x, y) == problem.getGoalState()


def run_config(layout_name, T0, alpha, Tmin, trials):
    """Roda 'trials' execucoes de uma configuracao e devolve as medias."""
    wins = 0
    lengths = []
    iters = []
    reheats = []
    t0 = time.time()

    for _ in range(trials):
        problem = build_problem(layout_name)
        actions, n_iter, n_reheat, finished = search.simulatedAnnealingSearch(
            problem, T0=T0, alpha=alpha, Tmin=Tmin,
            max_iters=2000000, return_stats=True)
        if finished and path_reaches_goal(problem, actions):
            wins += 1
        lengths.append(len(actions))
        iters.append(n_iter)
        reheats.append(n_reheat)

    elapsed = time.time() - t0
    avg = lambda xs: sum(xs) / len(xs)
    return {
        'win_rate': wins / trials,
        'wins': wins,
        'trials': trials,
        'len_avg': avg(lengths),
        'len_min': min(lengths),
        'len_max': max(lengths),
        'iter_avg': avg(iters),
        'reheat_avg': avg(reheats),
        'time_total': elapsed,
    }


def print_header(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
    print("%-24s %-8s %-13s %-11s %-10s %-8s"
          % ("config (T0/alpha/Tmin)", "sucesso", "passos", "iters", "reaquec", "tempo"))
    print("-" * 78)


def print_row(label, r):
    print("%-24s %-8s %-13s %-11.0f %-10.1f %-8s"
          % (label,
             "%d/%d" % (r['wins'], r['trials']),
             "%.0f (%d-%d)" % (r['len_avg'], r['len_min'], r['len_max']),
             r['iter_avg'],
             r['reheat_avg'],
             "%.1fs" % r['time_total']))



def main():
    LAYOUT = "mediumMaze"   # labirinto usado nos experimentos
    TRIALS = 20             # repeticoes por configuracao (media estatistica)

    print("Benchmark Simulated Annealing | labirinto=%s | repeticoes=%d por config"
          % (LAYOUT, TRIALS))
    print("(o algoritmo e estocastico; cada valor abaixo e a MEDIA de %d execucoes)"
          % TRIALS)

    # --- Experimento 1: variando alpha (taxa de resfriamento) ---
    print_header("EXPERIMENTO 1 - taxa de resfriamento (alpha) | T0=1000, Tmin=0.01")
    for alpha in [0.800, 0.950, 0.995, 0.9995]:
        r = run_config(LAYOUT, 1000.0, alpha, 0.01, TRIALS)
        print_row("1000 / %.4g / 0.01" % alpha, r)

    # --- Experimento 2: variando T0 (temperatura inicial) ---
    print_header("EXPERIMENTO 2 - temperatura inicial (T0) | alpha=0.995, Tmin=0.01")
    for T0 in [1.0, 10.0, 100.0, 1000.0, 10000.0]:
        r = run_config(LAYOUT, T0, 0.995, 0.01, TRIALS)
        print_row("%.4g / 0.995 / 0.01" % T0, r)

    # --- Experimento 3: variando Tmin (temperatura minima) ---
    print_header("EXPERIMENTO 3 - temperatura minima (Tmin) | T0=1000, alpha=0.995")
    for Tmin in [0.001, 0.01, 1.0, 50.0]:
        r = run_config(LAYOUT, 1000.0, 0.995, Tmin, TRIALS)
        print_row("1000 / 0.995 / %.4g" % Tmin, r)

    print("\nLegenda:")
    print("  sucesso  = execucoes que chegaram a meta / total de execucoes")
    print("  passos   = tamanho medio do caminho (min-max) apos poda de ciclos")
    print("  iters    = numero medio de iteracoes do laco principal")
    print("  reaquec  = numero medio de reaquecimentos (T reiniciada para T0)")
    print("  tempo    = tempo total das %d execucoes da configuracao" % TRIALS)
    print("\nObs.: tempos dependem da maquina; taxas variam um pouco por ser")
    print("      estocastico. As TENDENCIAS (nao os numeros exatos) sao o que importa.")


if __name__ == "__main__":
    main()
