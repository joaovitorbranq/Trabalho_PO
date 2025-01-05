from mip import Model, xsum, BINARY, minimize

# Definição dos conjuntos e parâmetros
e_funcionarios = ['Alice', 'Bob', 'Carol']
d_dias = range(7)  # 7 dias
turnos = ['Manhã', 'Tarde', 'Noite']
demanda_turno = {t: 1 for t in turnos}  # 1 funcionário por turno

# Criação do modelo
model = Model("Employee Scheduling")

# Variáveis de decisão: x[e, d, t] = 1 se funcionário e trabalhar no turno t no dia d
x = {(e, d, t): model.add_var(var_type=BINARY, name=f"x_{e}_{d}_{t}")
     for e in e_funcionarios for d in d_dias for t in turnos}

# Restrição 1: Cobertura de Turnos
for d in d_dias:
    for t in turnos:
        model += xsum(x[e, d, t] for e in e_funcionarios) >= demanda_turno[t], f"Cobertura_{d}_{t}"

# Restrição 2: Um funcionário por turno por dia
for e in e_funcionarios:
    for d in d_dias:
        model += xsum(x[e, d, t] for t in turnos) <= 1, f"MaxTurnos_{e}_{d}"

# Restrição 3: Balanceamento de carga de trabalho (minimizar diferença de carga entre funcionários)
carga_trabalho = {e: xsum(x[e, d, t] for d in d_dias for t in turnos) for e in e_funcionarios}

# Variáveis auxiliares para modelar o valor absoluto
diff_max = model.add_var(name="diff_max")
diff_min = model.add_var(name="diff_min")

# Definindo restrições para balanceamento
diff_ref = carga_trabalho[e_funcionarios[0]]
for e in e_funcionarios:
    model += carga_trabalho[e] <= diff_max
    model += carga_trabalho[e] >= diff_min

# Função Objetivo: Minimizar a diferença máxima entre cargas de trabalho
model.objective = minimize(diff_max - diff_min)

# Resolver o problema
model.optimize()

# Exibir a solução
if model.num_solutions > 0:
    for e in e_funcionarios:
        print(f"\nEscala de {e}:")
        for d in d_dias:
            for t in turnos:
                if x[e, d, t].x >= 0.99:
                    print(f" - Dia {d+1}, Turno: {t}")
else:
    print("Nenhuma solução encontrada!")
