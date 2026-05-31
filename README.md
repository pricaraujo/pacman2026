# Pac-Man: Way of the Katana - Documentação e Código

---

## 1. Descrição do Projeto

O objetivo deste projeto é implementar o algoritmo de busca local Simulated Annealing (Têmpera Simulada) no ambiente do Pac-Man para encontrar caminhos do estado inicial até o estado meta. Para otimizar a pontuação e evitar loops causados pela aceitação de soluções piores, a implementação conta com um mecanismo dinâmico de poda de ciclos e reaquecimento adaptativo.

---

## 2. Formulação Matemática

O algoritmo modela o labirinto como um espaço de estados onde a energia está associada à distância até o objetivo.

* **Função de Energia ($E$):** Calculada através da Distância de Manhattan entre o estado atual $s(x, y)$ e o estado objetivo $g(x, y)$:
  $$E(s) = |x_s - x_g| + |y_s - y_g|$$

* **Variação de Energia ($\Delta E$):** A diferença de impacto entre o estado sucessor $s'$ e o atual $s$:
  $$\Delta E = E(s') - E(s)$$

* **Critério de Metropolis ($P$):** Se $\Delta E < 0$, o movimento é aceito de forma determinística. Se $\Delta E \geq 0$, o movimento é aceito probabilisticamente de acordo com a temperatura atual $T$:
  $$P = e^{-\frac{\Delta E}{T}}$$

* **Esquema de Resfriamento:** Redução geométrica da temperatura a cada iteração baseada na taxa alfa ($\alpha$):
  $$T_{k+1} = T_k \cdot \alpha$$

---

## 3. Implementação do Código (`search.py`)

O algoritmo está implementado na função `simulatedAnnealingSearch`, registrada no framework do Pac-Man pelo alias `sa`:

```python
def simulatedAnnealingSearch(problem, T0=1000.0, alpha=0.995, Tmin=0.01,
                             max_iters=None, return_stats=False):
    ...

sa = simulatedAnnealingSearch
```

Os hiperparâmetros são **argumentos da função**, com os valores da especificação como padrão (`T0=1000`, `alpha=0.995`, `Tmin=0.01`). Dessa forma, a chamada do framework (`fn=sa`) permanece inalterada, mas o benchmark consegue variá-los sem duplicar a lógica do algoritmo.

| Parâmetro | Significado |
|-----------|-------------|
| `T0` | Temperatura inicial do sistema. |
| `alpha` | Taxa de resfriamento geométrico ($T_{k+1} = T_k \cdot \alpha$). |
| `Tmin` | Temperatura mínima que dispara o reaquecimento adaptativo. |
| `max_iters` | Salvaguarda opcional contra laço infinito (`None` = sem teto). Usado pelo benchmark. |
| `return_stats` | Se `True`, devolve `(caminho, iterações, reaquecimentos, concluiu)` em vez de apenas o caminho de ações. Usado pelo benchmark. |

Destaques da implementação:

* **Poda de ciclos:** ao revisitar um estado já presente no histórico, o trecho cíclico é descartado (`state_history.index`), mantendo o caminho final enxuto.
* **Reaquecimento adaptativo:** quando $T < T_{min}$ antes de alcançar a meta, a temperatura é reiniciada para `T0`, evitando o congelamento precoce da busca.

---

## 4. Benchmark de Hiperparâmetros (`benchmark_sa.py`)

Como o Simulated Annealing é **estocástico**, uma única execução não é representativa. O script `benchmark_sa.py` roda cada configuração várias vezes (`TRIALS`) e reporta a **média**, medindo:

* **taxa de sucesso** (execuções que chegam à meta),
* **qualidade do caminho** (número de passos, após poda de ciclos),
* **custo computacional** (iterações e reaquecimentos),
* **tempo de execução**.

O benchmark reutiliza a **mesma** função do `search.py` (`search.simulatedAnnealingSearch`, com `return_stats=True`), apenas variando os hiperparâmetros — ou seja, ele mede exatamente o que roda no jogo, sem reimplementar o algoritmo. As baterias de teste variam `alpha`, `T0` e `Tmin` independentemente.

---

## 5. Análise Experimental de Parâmetros

Dados consolidados sobre o comportamento do agente mediante alterações nos hiperparâmetros:

| Configuração | Parâmetros | Tempo de Execução | Qualidade do Caminho | Taxa de Sucesso |
|-------------|------------|-------------------|---------------------|-----------------|
| Padrão Homologado | $T=1000$, $\alpha=0.995$ | Moderado | Alta (sem redundâncias) | Alta |
| Resfriamento Agressivo | $T=1000$, $\alpha=0.800$ | Muito Baixo | Baixa (trava em paredes) | Baixa |
| Baixa Energia Inicial | $T=10$, $\alpha=0.995$ | Baixo | Regular | Média |

### Janela de Exploração

Taxas de resfriamento muito aceleradas ($\alpha = 0.800$) reduzem a probabilidade de aceitação de Metropolis quase instantaneamente, transformando a busca em um algoritmo ganancioso míope.

### Controle de Loops

A presença do histórico com indexação reversa (`state_history.index`) garante que caminhos ciclistas gerados pela natureza estocástica do algoritmo sejam limpos antes do retorno final das ações, maximizando a pontuação do jogo.

---

## 6. Instruções de Execução

Executar o agente no jogo (comando oficial da especificação):

```bash
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=sa
```

Rodar o benchmark de hiperparâmetros (a partir da pasta do projeto, junto do `pacman.py`):

```bash
python3 benchmark_sa.py
```

> O labirinto e o número de repetições por configuração podem ser ajustados nas variáveis `LAYOUT` e `TRIALS`, no final do `benchmark_sa.py`.
