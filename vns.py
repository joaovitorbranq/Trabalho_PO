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

# Função de vizinhança 1: Troca entre médicos em turnos específicos
def vizinhanca_1(solution):
    # Escolher um turno aleatório e dois médicos para trocar
    m1, m2 = random.sample(medicos, 2)
    d = random.choice(dias)
    t = random.choice(turnos)

    if solution[m1][d][t] == 1 and solution[m2][d][t] == 0:
        solution[m1][d][t], solution[m2][d][t] = 0, 1
    return solution

# Função de vizinhança 2: Modificar a alocação de turnos
def vizinhanca_2(solution):
    # Trocar aleatoriamente um turno de um médico
    m = random.choice(medicos)
    d1, d2 = random.sample(dias, 2)
    t1 = random.choice(turnos)
    t2 = random.choice(turnos)

    if solution[m][d1][t1] == 1:
        solution[m][d1][t1], solution[m][d2][t2] = 0, 1
    return solution

# Função de vizinhança 3: Trocar turnos inteiros entre dois médicos
def vizinhanca_3(solution):
    m1, m2 = random.sample(medicos, 2)
    d1, d2 = random.sample(dias, 2)
    t = random.choice(turnos)

    if solution[m1][d1][t] == 1 and solution[m2][d2][t] == 0:
        solution[m1][d1][t], solution[m2][d2][t] = 0, 1
    return solution

# Algoritmo VNS
def vns(prob, iterations=10000, max_neighborhood=3):
    melhor_solucao = None
    melhor_custo = float('inf')
    custos = []

    for i in range(iterations):
        solucao_inicial = construcao_inicial_aleatoria()
        solucao_atual = solucao_inicial
        custo_atual = calcular_custo(solucao_atual)

        while True:
            # Explorar as vizinhanças
            melhorou = False
            for vizinhanca_id in range(1, max_neighborhood+1):
                if vizinhanca_id == 1:
                    solucao_atual = vizinhanca_1(solucao_atual)
                elif vizinhanca_id == 2:
                    solucao_atual = vizinhanca_2(solucao_atual)
                elif vizinhanca_id == 3:
                    solucao_atual = vizinhanca_3(solucao_atual)
                
                novo_custo = calcular_custo(solucao_atual)
                if novo_custo < custo_atual:
                    custo_atual = novo_custo
                    melhorou = True
                    break  # Se uma melhoria foi encontrada, recomeçar a busca

            if not melhorou:  # Se nenhuma melhoria foi encontrada, parar
                break

        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_solucao = solucao_atual

        custos.append(melhor_custo)
        print(f"Iteração {i + 1}: Custo Atual = {custo_atual}, Melhor Custo = {melhor_custo}")

    return melhor_solucao, melhor_custo, custos

# Executar o VNS
start_time = time.time()
melhor_solucao, melhor_custo, custos = vns(prob, iterations=1000)
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
