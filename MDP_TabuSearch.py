import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime


# Define the parameters needed to execute the algorithm
iterationCount = 20
tabuTenure = [10, 15, 20]
result = pd.DataFrame(columns=['File', 'InitialDiversity', 'FinalDiversity', 'runTime', 'TabuTenure'])
stoppingCriteria = 20000
# Get the paths of all txt files in the folder
folder_path = r"instances"
txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

def readInstance(path):
    instance = {}
    with open(path, "r") as f:
        # First line in file has two numbers: n p
        n, p = f.readline().split()
        n = int(n)
        p = int(p)
        instance['n'] = n
        instance['p'] = p
        instance['d'] = []
        for i in range(n):
            instance['d'].append([0] * n)
        for i in range(n):
            for j in range(i+1, n):
                u, v, d = f.readline().split()
                u = int(u)
                v = int(v)
                d = round(float(d), 2)
                instance['d'][u][v] = d
                instance['d'][v][u] = d
    return instance

# Generate an initial solution by greedily selecting 'm' elements with maximum sum of distances to already selected elements.
def generate_initial_solution(df, m):
    initial_solution = [np.random.choice(df.columns, 1, replace=False)[0]]
    while len(initial_solution) < m:
        next_element = df.drop(initial_solution, axis=1).loc[initial_solution].sum().idxmax()
        initial_solution.append(next_element)
    return initial_solution



for file in txt_files:
    my_dict = readInstance(file)
    m = my_dict['p']
    df = pd.DataFrame(my_dict['d'])
    # Generate an initial solution called "CurrentBestSolution"
    CurrentBestSolution = generate_initial_solution(df, m)
    initialDiversity = df.loc[CurrentBestSolution, CurrentBestSolution].sum().sum() / 2
    MaxDiversity = initialDiversity
    for tenureIter in tabuTenure:
        tabuList = pd.DataFrame({'From': [np.nan] * tenureIter, 'To': [np.nan] * tenureIter})
        bestSwap = tabuList.iloc[0].copy()
        noImprovement = 0
        tic = datetime.now()

        # Perform Tabu Search for 'iterationCount' iterations, swapping elements in the current solution to seek improved solutions, and update the tabu list after each iteration
        for iterCount in range(iterationCount):
            
            candidates = [col for col in df.columns if col not in CurrentBestSolution]
            for i in CurrentBestSolution:
                for j in candidates:
                    if noImprovement >= stoppingCriteria:
                        break
                    if i in tabuList['To'].values or j in tabuList['From'].values:
                        continue
                    iterSolution = [j if x == i else x for x in CurrentBestSolution]
                    newDiversity = df.loc[iterSolution, iterSolution].sum().sum() / 2
                    
                    # Identify the best swap and update the current solution
                    Swap = {'From': i, 'To': j, 'Diversity': newDiversity}
                    newSolution = [Swap['To'] if x == Swap['From'] else x for x in CurrentBestSolution]
                    
                    # If new solution is better than current best solution, replace it
                    if newDiversity > MaxDiversity:
                        MaxDiversity = newDiversity
                        bestSwap = Swap
                        CurrentBestSolution = newSolution
                    else:
                        noImprovement += 1

            tabuList = pd.concat([tabuList.iloc[1:], pd.DataFrame([bestSwap])], ignore_index=True)
        
        toc = datetime.now()
        file = os.path.basename(file)
        result_row = { 'File': file,'InitialDiversity': round(initialDiversity,2), 'FinalDiversity': round(MaxDiversity,2), 'runTime': (toc-tic).total_seconds(), 'TabuTenure': tenureIter}
        print('For file',file,'the initial diversity is',round(initialDiversity, 2),'and the final diversity is',round(MaxDiversity, 2))
        result = pd.concat([result, pd.DataFrame([result_row])], ignore_index=True)

print(result)

result.to_csv('TabuSearch_MDP Results.csv', index=False)