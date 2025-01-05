import random
from mip import Model, xsum, BINARY, minimize

# Definição dos conjuntos e parâmetros
e_funcionarios = ['Alice', 'Bob', 'Carol']
d_dias = range(7)  # 7 dias
turnos = ['Manhã', 'Tarde', 'Noite']
demanda_turno = {t: 1 for t in turnos}  # 1 funcionário por turno

# Função para gerar solução inicial gulosa randomizada
def construir_solucao_inicial():
    model = Model("Employee Scheduling")
    x = {(e, d, t): model.add_var(var_type=BINARY, name=f"x_{e}_{d}_{t}")
         for e in e_funcionarios for d in d_dias for t in turnos}

    # Construção gulosa randomizada: atribuir turnos de forma parcial aleatória
    for d in d_dias:
        funcionarios_disponiveis = e_funcionarios.copy()  # lista de funcionários disponíveis para o dia
        random.shuffle(funcionarios_disponiveis)  # embaralhar a lista para aleatoriedade
        for t in turnos:
            if funcionarios_disponiveis:  # Se houver funcionários disponíveis para o turno
                escolhido = funcionarios_disponiveis.pop()
                x[escolhido, d, t].lb = 1  # Fixando a escolha para o turno e dia
                x[escolhido, d, t].ub = 1  # Garantir que o turno será atribuído

    model.optimize()
    return model, x

# Função de busca local para ajuste fino da solução
def busca_local(model, x):
    melhora = True
    while melhora:
        melhora = False
        for e in e_funcionarios:
            for d in d_dias:
                for t in turnos:
                    if x[e, d, t].x >= 0.99:
                        model.remove(x[e, d, t])
                        x[e, d, t] = model.add_var(var_type=BINARY, name=f"x_{e}_{d}_{t}")
                        model.optimize()
                        if model.objective_value < model.objective_value:
                            melhora = True
                        else:
                            x[e, d, t].lb = 1  # Reverter mudança
    return model

# Algoritmo GRASP completo
def grasp(iteracoes):
    melhor_solucao = None
    melhor_objetivo = float('inf')

    for _ in range(iteracoes):
        model, x = construir_solucao_inicial()
        model = busca_local(model, x)

        if model.objective_value < melhor_objetivo:
            melhor_solucao = x
            melhor_objetivo = model.objective_value

    print(f"Melhor objetivo encontrado: {melhor_objetivo}")
    for e in e_funcionarios:
        print(f"\nEscala de {e}:")
        for d in d_dias:
            for t in turnos:
                if melhor_solucao[e, d, t].x >= 0.99:
                    print(f" - Dia {d+1}, Turno: {t}")

# Executar o GRASP com 10 iterações
grasp(1)
