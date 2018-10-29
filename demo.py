
import layers as layers_fw
import pandas as pd
import time


score_orig = [
    [None, 10, 15, 25, 32, 25, 21, 21, 15, 22, 12, 54],
    [41, None, 57, 24, 52, 2, 66, 55, 61, 15, 6, 7],
    [21, 31, None, 21, 21, 44, 21, 22, 22, 61, 47, 61],
    [66, 22, 15, None, 47, 21, 41, 15, 21, 22, 32, 34],
    [21, 44, 61, 47, None, 32, 26, 61, 55, 34, 18, 12],
    [22, 18, 22, 23, 41, None, 21, 22, 44, 55, 54, 54],
    [15, 25, 34, 21, 26, 27, None, 34, 25, 41, 7, 22],
    [61, 34, 12, 54, 21, 23, 15, None, 21, 21, 55, 55],
    [22, 54, 54, 65, 3, 25, 61, 77, None, 47, 22, 22],
    [34, 7, 22, 23, 54, 42, 22, 54, 21, None, 12, 15],
    [26, 61, 55, 22, 18, 18, 22, 18, 34, 21, None, 12],
    [22, 18, 25, 34, 21, 22, 18, 61, 55, 2, 22, None]
]

score_test = [[0, 3, 8, 12],
         [6, 0, 4, 2],
         [3, 8, 0, 7],
         [12, 5, 9, 0]]


def test_parametres(generations_max=500, g_step=5, population_max=50, p_step=2, mutation_max=0.8, m_step=0.05, repetitions=5, backup_frequency=500):
    layers = layers_fw.LayerSolver(score=score_orig, population_size=7, generations=400)
    cols = ['Generations', 'Population Size', 'Mutation Probability', 'Scores', 'Individuals', 'Iteration', 'Time (avg.)']
    results = pd.DataFrame(columns=cols)
    population_size = p_step
    generations = g_step
    mutation_prob = m_step
    total = int(population_max / p_step) * int( mutation_max / m_step) * int(generations_max / g_step)
    c = 0
    while population_size <= population_max:
        mutation_prob = m_step
        while(mutation_prob <= mutation_max):
            generations = g_step
            while generations <= generations_max:
                scores, individuals, iterations = [], [], []
                s = time.time()
                for r in range(repetitions):
                    layers.update_parameters(generations=generations, population_size=population_size, mutation_prob=mutation_prob)
                    top_score, top_individual, solution_iteration = layers.run()
                    scores.append(top_score)
                    individuals.append(top_individual)
                    iterations.append(solution_iteration)
                c += 1
                e = time.time()
                # time in seconds
                t = (e - s)/repetitions
                new = pd.DataFrame([generations, population_size, mutation_prob, scores, individuals, iterations, t]).transpose()
                new.columns = cols
                results = pd.concat([results, new])
                if int(c) % backup_frequency == 0:
                    print("{0} % done: {1} steps out of {2} done.".format(c / total * 100, c, total))
                    results.to_hdf("results.hdf", "table")
                generations += g_step
            mutation_prob += m_step
        population_size += p_step




if __name__ == '__main__':
    test_parametres()