import random
import math

def simulatedAnnealingSearch(problem):
    """
    Busca caminhos através do algoritmo Simulated Annealing (Têmpera Simulada).
    """
    # Variáveis mandatórias da especificação
    T = 1000.0
    alpha = 0.995
    Tmin = 0.01

    # Estado inicial do Pac-Man
    start_state = problem.getStartState()
    current_state = start_state
    
    # Histórico para reconstrução e otimização do caminho (poda de ciclos)
    state_history = [current_state]
    action_path = []

    # Identificação do estado objetivo (meta)
    goal = None
    if hasattr(problem, 'goal'):
        goal = problem.goal

    def get_energy(state):
        """Calcula a energia baseada na Distância de Manhattan até o objetivo."""
        if goal:
            return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
        return 0

    # Loop principal até encontrar o estado final
    while not problem.isGoalState(current_state):
        successors = problem.getSuccessors(current_state)
        
        if not successors:
            # Caso encontre um beco sem saída absoluto, reinicia o estado
            current_state = start_state
            state_history = [start_state]
            action_path = []
            T = 1000.0
            continue

        # Seleciona um sucessor aleatório (vizinhança)
        next_state, action, cost = random.choice(successors)

        # Cálculo da variação de energia (Minimização da distância)
        current_energy = get_energy(current_state)
        next_energy = get_energy(next_state)
        delta_E = next_energy - current_energy

        # Critério de aceitação de Metropolis
        accept = False
        if delta_E < 0:
            accept = True
        else:
            if T > 0:
                probability = math.exp(-delta_E / T)
                if random.random() < probability:
                    accept = True

        if accept:
            if next_state in state_history:
                # Otimização: Poda o ciclo se redefinir passos anteriores
                idx = state_history.index(next_state)
                state_history = state_history[:idx + 1]
                action_path = action_path[:idx]
            else:
                state_history.append(next_state)
                action_path.append(action)
            
            current_state = next_state

        # Resfriamento do sistema
        T *= alpha

        # Estratégia de reaquecimento adaptativo para evitar congelamento precoce
        if T < Tmin and not problem.isGoalState(current_state):
            T = 1000.0

    return action_path

# Definição obrigatória do alias de função conforme a especificação
sa = simulatedAnnealingSearch
