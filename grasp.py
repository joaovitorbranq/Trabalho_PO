import pulp
import random
import time

# Parâmetros do problema
medicos = ["Dr. A", "Dr. B", "Dr. C", "Dr. D"]
turnos = ["Manhã", "Tarde", "Noite"]
dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horas_por_turno = 8
max_horas_semanais = 40

# Preferências de turno para cada médico (penalidades para turnos indesejados)
preferencias = {
    "Dr. A": {"Manhã": 0, "Tarde": 1, "Noite": 3},
    "Dr. B": {"Manhã": 1, "Tarde": 0, "Noite": 2},
    "Dr. C": {"Manhã": 3, "Tarde": 2, "Noite": 0},
    "Dr. D": {"Manhã": 2, "Tarde": 1, "Noite": 0}
}

# Criar o problema de otimização
prob = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Variáveis de decisão binárias
x = pulp.LpVariable.dicts("turno", (medicos, dias, turnos), cat="Binary")

# Função objetivo: minimizar o custo total das penalidades
prob += pulp.lpSum(preferencias[m][t] * x[m][d][t] for m in medicos for d in dias for t in turnos)

# Restrições: cada turno deve ser preenchido por um médico, e médicos não devem exceder o máximo de horas semanais
for d in dias:
    for t in turnos:
        prob += pulp.lpSum(x[m][d][t] for m in medicos) == 1

for m in medicos:
    prob += pulp.lpSum(x[m][d][t] * horas_por_turno for d in dias for t in turnos) <= max_horas_semanais

# Construção de uma solução inicial aleatória
def construcao_inicial_aleatoria():
    solution = {m: {d: {t: 0 for t in turnos} for d in dias} for m in medicos}
    horarios_livres = {m: max_horas_semanais // horas_por_turno for m in medicos}

    for d in dias:
        for t in turnos:
            medicos_disponiveis = [m for m in medicos if horarios_livres[m] > 0]
            m = random.choice(medicos_disponiveis)
            solution[m][d][t] = 1
            horarios_livres[m] -= 1

    return solution

# Função para calcular o custo de uma solução
def calcular_custo(solution):
    return sum(preferencias[m][t] * solution[m][d][t] for m in medicos for d in dias for t in turnos)

# Função de melhoria local
def melhoria_local(solution):
    melhorou = True
    while melhorou:
        melhorou = False
        melhor_custo = calcular_custo(solution)
        for m in medicos:
            for d in dias:
                for t in turnos:
                    if solution[m][d][t] == 1:
                        for n in medicos:
                            if n != m and solution[n][d][t] == 0:
                                # Trocar médicos
                                solution[m][d][t], solution[n][d][t] = 0, 1
                                novo_custo = calcular_custo(solution)
                                if novo_custo < melhor_custo:
                                    melhor_custo = novo_custo
                                    melhorou = True
                                else:
                                    # Reverter a troca
                                    solution[m][d][t], solution[n][d][t] = 1, 0
    return solution

# Algoritmo GRASP com monitoramento do custo
def grasp(prob, iterations=10):
    melhor_solucao = None
    melhor_custo = float('inf')
    custos = []

    for i in range(iterations):
        solucao_inicial = construcao_inicial_aleatoria()
        solucao_melhorada = melhoria_local(solucao_inicial)
        custo_atual = calcular_custo(solucao_melhorada)

        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_solucao = solucao_melhorada

        custos.append(melhor_custo)
        print(f"Iteração {i + 1}: Custo Atual = {custo_atual}, Melhor Custo = {melhor_custo}")

    return melhor_solucao, melhor_custo, custos

# Executar o GRASP
start_time = time.time()
melhor_solucao, melhor_custo, custos = grasp(prob, iterations=10000)
end_time = time.time()

# Exibir a melhor solução encontrada
print(f"Solução ótima com custo: {melhor_custo}")
for m in medicos:
    print(f"\nEscala de {m}:")
    for d in dias:
        for t in turnos:
            if melhor_solucao[m][d][t] == 1:
                print(f"- {d}: {t}")

print(f"\nTempo total de processamento: {end_time - start_time:.4f} segundos")
