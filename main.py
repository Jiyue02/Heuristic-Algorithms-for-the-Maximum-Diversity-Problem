from structure import instance, solution
from algorithms import grasp
import random
import pandas as pd
import os
import glob
from datetime import datetime

def executeInstance():
    all_results = []
    alpha_values = [0.3, 0.6, 0.9]

    for path in glob.glob("instances/*.txt"):
        inst = instance.readInstance(path)

        for alpha in alpha_values:
            start_time = datetime.now()

            sol = grasp.execute(inst, 20, alpha)

            end_time = datetime.now()
            run_time = (end_time - start_time).total_seconds()

            final_diversity = round(sol['of'], 2)
            data = {
                "File": path.split("/")[-1],
                "FinalDiversity": final_diversity,
                "runTime": run_time,
                "Alpha": alpha
            }
            all_results.append(data)

    result_df = pd.DataFrame(all_results)
    result_df.to_csv(f"GRASP_MDP.csv", index=False)

if __name__ == '__main__':
    random.seed(1)
    executeInstance()

