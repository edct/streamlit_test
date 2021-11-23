import numpy as np
import pandas as pd
import random

n_pop = 200
n_bits = 10
max_score = 900000000
n_iterations = 100


def create_pop(n_bits, n_pop):
    population = [random.sample(range(0, 10), n_bits) for _ in range(0, n_pop)]
    return population

def mutate(ind):
    #print(ind)
    if random.random() < 0.5:
        for i in ind['individual']:
            if random.random() < 0.3:
                i = random.randint(0, 10)
        ind['score'] = 0
    return ind

##need to make this not affect the original df somehow
def breed(df):
    df = df.reset_index(drop = True)
    ind_1 = df.loc[0]
    ind_2 = df.loc[1]
    for i in range(0, len(ind_1['individual'])):
        if random.random() < 0.5:
            ind_1['individual'][i] = ind_2['individual'][i]
        if random.random() < 0.5:
            ind_2['individual'][i] = ind_1['individual'][i]
    df.loc[0] = ind_1
    df.loc[1] = ind_2
    return df

def mutateNbreed(df):
    modify_df = df.drop(columns = ['rank'])
    n_df = modify_df[df['rank'] <= 2]
    ##mutate individuals
    for i in range(0, 98):
        sample_df = modify_df.sample(2)
        n_df = n_df.append(breed(sample_df))
    n_df[['individual', 'score']] = n_df[['individual', 'score']].apply(mutate, axis = 1)
    n_df['rank'] = 0
    return n_df

def run_game(individual):
    val = 1
    for i in range(0, len(individual)):
        val = val * individual[i]
    return val

def evaluate(individual, attempts = 1):
    scores = []
    for i in range(0, attempts):
        scores.append(run_game(individual))
    return max(scores)

def print_eval(individual):
    val = 1
    for i in range(0, len(individual)):
        val = val * individual[i]
    print('best individual: ' + str(individual))
    print('best score: ' + str(val))
    return val

score_df = pd.DataFrame({'max score' : [0], 'avg score' : [0], 'best individual' : [[0, 0, 0, 0, 0, 0, 0, 0]]})
score_df.to_csv('C:/Users/barre/python stuff/data/score_df.csv')
for gen in range(0, n_iterations):
    if gen == 0:
        population = create_pop(n_bits, n_pop)
        pop_df = pd.DataFrame({'individual' : population, 'score' : [0 for i in population]})
        pop_df['score'] = pop_df['individual'].apply(evaluate)
    print('---------------------------------')
    print('GENERATION :' + str(gen))
    ##SELECTION:
    pop_df = pop_df.sort_values(by = 'score', ascending = False).reset_index(drop = True)
    pop_df['rank'] = pop_df.index + 1
    pop_df = pop_df[:int(pop_df.shape[0]/2)]

    ##MUTATION:
    top_2.to_csv('C:/Users/barre/python stuff/data/top_2.csv')
    pop_df = mutateNbreed(pop_df)
    top_2 = pd.read_csv('C:/Users/barre/python stuff/data/top_2.csv',
                       usecols = ['individual', 'score', 'rank'],
                       )
    top_2['individual'] = top_2['individual'].map(lambda x: eval(x))
    pop_df = pd.concat([pop_df, top_2], ignore_index = True)
    ##EVALUATION:
    pop_df['score'] = pop_df['individual'].apply(evaluate)
    pop_df = pop_df.sort_values(by = 'score', ascending = False).reset_index(drop = True)
    pop_df['rank'] = pop_df.index + 1
    best_df = pop_df[pop_df['score'] == pop_df['score'].max()]
    if len(best_df.index) == 1:
        top_2 = pd.concat([best_df, best_df], ignore_index = True)
    else:
        top_2 = best_df[:2]
    best_individual = best_df.loc[0, 'individual']
    print_eval(best_individual)
    score_series = pd.Series({'max score' : pop_df['score'].max(), 'avg score' : pop_df['score'].mean(), 'best individual' : best_individual})
    score_df = pd.read_csv('C:/Users/barre/python stuff/data/score_df.csv')
    score_df = pd.read_csv('C:/Users/barre/python stuff/data/score_df.csv',
                      usecols = ['max score', 'avg score', 'best individual'],
                      )
    score_df['best individual'] = score_df['best individual'].map(lambda x: eval(x))
    score_df = score_df.append(score_series, ignore_index = True)
    score_df.to_csv('C:/Users/barre/python stuff/data/score_df.csv')
    #if max(pop_df['score']) > max_score:
        ##work out how to end the thing here
    #    print('RUN COMPLETED: ' + pop_df[pop_df['score'] > max_score]['individual'])
    #    break
score_df.to_csv('C:/Users/barre/python stuff/data/score_df.csv')