# Initial population
# Fitness function
# Selection
# Crossover
# Mutation


from functools import reduce
import random

class LayerSolver():
    def __init__(self, score, population_size=15, generations=50, fitness_fcn=None, convergence=5, mutation_prob=0.1):
        self.fitness = fitness_fcn if fitness_fcn is not None else self.default_fitness
        self.score = score
        self.initial_population_size = population_size * 2
        self.population_size = population_size
        self.generations = generations
        self.layers_c = len(score[0])
        self.convergence = convergence
        self.top_individual = None
        self.top_score = 0
        self.mutation_probability = mutation_prob

    def update_parameters(self, population_size=None, generations=None, fitness_fcn=None, mutation_prob=None):
        if population_size != None:
            self.population_size = population_size
        if generations != None:
            self.generations = generations
        if fitness_fcn != None:
            self.fitness = fitness_fcn
        if mutation_prob != None:
            self.mutation_probability = mutation_prob

    def init_population(self):
        self.population = []
        for i in range(self.initial_population_size):
            new_individual = [x for x in range(self.layers_c)]
            random.shuffle(new_individual)
            self.population.append(new_individual)


    def default_fitness(self, individual):
        sum = 0
        for i in range(len(individual) - 1):
            a, b = individual[i:i+2]
            sum += self.score[a][b]
        return sum

    def cross_over(self):
        crossed = []
        for i in range(len(self.population) - 1):
            for j in range(1, len(self.population)):
                if i != j:
                    split = random.randint(0, self.layers_c)
                    a1 = self.population[i][:split]
                    a2 = self.population[i][split:]
                    b2 = self.population[j][split:]
                    missing = [k for k in a2 if k not in b2]
                    new = a1 + [missing.pop(0) if e in a1 else e for e in b2]
                    crossed.append(new)
        self.population = self. population + crossed

    # currently swaps two genes randomly
    def mutation(self, debug=False):
        for individual in self.population:
            s = "{0} has been mutated to ".format(individual)
            if random.random() < self.mutation_probability:
                g1 = random.randint(0, self.layers_c - 1)
                g2 = random.randint(0, self.layers_c - 1)
                while(g1 == g2):
                    g2 = random.randint(0, self.layers_c - 1)
                tmp = individual[g1]
                individual[g1] = individual[g2]
                individual[g2] = tmp
            if debug:
                print(s + str(individual))

    def selection(self):
        self.population = sorted(self.population, key = lambda x: self.fitness(x), reverse=True)
        self.population = self.population[:self.population_size]

    # 1. Initial population
    # 2. Fitness function
    # 3. Selection
    # 4. Crossover
    # 5. Mutation

    def run(self, debug=False):
        solution_iteration = None
        self.top_score = 0
        self.top_individual = None
        self.init_population()
        for g in range(self.generations):
            self.selection()
            top = self.population[0]
            score = self.fitness(top)
            if score > self.top_score:
                self.top_score = score
                self.top_individual = top
                solution_iteration = g
            if debug:
                print("Iteration {0}: {1} with score {2}.".format(g, self.top_individual, self.top_score))
            self.cross_over()
            self.mutation()
        return self.top_score, self.top_individual, solution_iteration




score = [[0, 3, 8, 12],
         [6, 0, 4, 2],
         [3, 8, 0, 7],
         [12, 5, 9, 0]]



if __name__ == '__main__':
    pass