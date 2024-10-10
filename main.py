import random
import math

POPULATION_SIZE = 50
GENOME_LENGTH = 40
MUTATION_RATE = 0.1
GENERATIONS = 500

FUNCTION_SET = ['+', '-', '*', '/']
TERMINAL_SET = ['x', '1', '2', '3', '4', '5']

DATA_SET = [(x, x**2 + x + 1) for x in range(-10, 11)]

def generate_genome():
    genes = []
    for _ in range(GENOME_LENGTH):
        if random.random() < 0.5:
            genes.append(random.choice(FUNCTION_SET))
        else:
            genes.append(random.choice(TERMINAL_SET))
    return genes

def build_population():
    return [generate_genome() for _ in range(POPULATION_SIZE)]

def parse_expression(genome):
    stack = []
    for gene in genome:
        if gene in FUNCTION_SET:
            if len(stack) < 2:
                continue
            b = stack.pop()
            a = stack.pop()
            expression = f'({a} {gene} {b})'
            stack.append(expression)
        else:
            stack.append(gene)
    return stack[0] if stack else '0'

def fitness(genome):
    expression = parse_expression(genome)
    total_error = 0.0
    for x_val, y_true in DATA_SET:
        try:
            y_pred = eval(expression, {'x': x_val, 'math': math})
            total_error += abs(y_true - y_pred)
        except (ZeroDivisionError, SyntaxError, NameError, TypeError):
            return float('inf')
    return total_error / len(DATA_SET)

def selection(population):
    selected = []
    for _ in range(POPULATION_SIZE):
        ind1 = random.choice(population)
        ind2 = random.choice(population)
        selected.append(ind1 if fitness(ind1) < fitness(ind2) else ind2)
    return selected

def crossover(parent1, parent2):
    idx = random.randint(1, GENOME_LENGTH - 1)
    child1_genes = parent1[:idx] + parent2[idx:]
    child2_genes = parent2[:idx] + parent1[idx:]
    return child1_genes, child2_genes

def mutate(genome):
    mutated_genome = genome.copy()
    for i in range(len(mutated_genome)):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5:
                mutated_genome[i] = random.choice(FUNCTION_SET)
            else:
                mutated_genome[i] = random.choice(TERMINAL_SET)
    return mutated_genome

def evolve(population):
    new_population = []
    selected = selection(population)
    while len(new_population) < POPULATION_SIZE:
        parent1 = random.choice(selected)
        parent2 = random.choice(selected)
        child1_genes, child2_genes = crossover(parent1, parent2)
        child1 = mutate(child1_genes)
        child2 = mutate(child2_genes)
        new_population.extend([child1, child2])
    return new_population[:POPULATION_SIZE]

# Algoritmo principal
population = build_population()
best_global_genome = None
best_global_fitness = float('inf')
best_global_expression = ""
best_global_gen = None

for generation in range(GENERATIONS):
    population = evolve(population)
    best_genome = min(population, key=lambda genome: fitness(genome))
    best_expression = parse_expression(best_genome)
    best_fitness = fitness(best_genome)

    if best_fitness < best_global_fitness:
        best_global_genome = best_genome
        best_global_fitness = best_fitness
        best_global_expression = best_expression
        best_global_gen = generation + 1

    print(f"Geração {generation + 1}: Melhor Aptidão = {best_fitness}")
    print(f"Melhor Expressão: {best_expression}\n")

print("Melhor solução encontrada:")
print(f"Geração: {best_global_gen}\nExpressão: {best_global_expression}")
print(f"Aptidão: {best_global_fitness}")

