# Pac-Man: Way of the Katana - Documentação e Código

Este arquivo contém a documentação completa e o código-fonte estruturado para o projeto da disciplina MATA64 - Inteligência Artificial. O conteúdo abaixo foi elaborado rigorosamente de acordo com as diretrizes do documento Especificacao-Trabalho-pacman-20261.pdf.

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

sa = simulatedAnnealingSearch}

# 2. Fundamentação Matemática

O comportamento de busca do agente é regido pelas seguintes formulações:

## Função de Energia ($E$)

Baseada na Distância de Manhattan até a meta:

$$
E(s) = |x_s - x_g| + |y_s - y_g|
$$

## Variação de Energia ($\Delta E$)

Diferença de potencial entre o estado candidato e o atual:

$$
\Delta E = E(s') - E(s)
$$

## Critério de Aceitação de Metropolis ($P$)

Probabilidade de escolher caminhos que inicialmente se afastam do objetivo para escapar de mínimos locais:

$$
P = e^{-\frac{\Delta E}{T}}
$$

## Função de Resfriamento

Decaimento geométrico da temperatura do sistema:

$$
T_{k+1} = T_k \cdot \alpha
$$

---

# 3. Análise Experimental de Parâmetros

Dados consolidados sobre o comportamento do agente mediante alterações nos hiperparâmetros:

| Configuração | Parâmetros | Tempo de Execução | Qualidade do Caminho | Taxa de Sucesso |
|-------------|------------|-------------------|---------------------|-----------------|
| Padrão Homologado | $T=1000$, $\alpha=0.995$ | Moderado | Alta (sem redundâncias) | Alta |
| Resfriamento Agressivo | $T=1000$, $\alpha=0.800$ | Muito Baixo | Baixa (trava em paredes) | Baixa |
| Baixa Energia Inicial | $T=10$, $\alpha=0.995$ | Baixo | Regular | Média |

## Conclusões Críticas para os Slides

### Janela de Exploração

Taxas de resfriamento muito aceleradas ($\alpha = 0.800$) reduzem a probabilidade de aceitação de Metropolis quase instantaneamente, transformando a busca em um algoritmo ganancioso míope.

### Controle de Loops

A presença do histórico com indexação reversa (`state_history.index`) garante que caminhos ciclistas gerados pela natureza estocástica do algoritmo sejam limpos antes do retorno final das ações, maximizando a pontuação do jogo.

---

# 4. Instruções de Execução

Comando oficial para inicialização do ambiente de teste com o algoritmo implementado:

```bash
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=sa
```
