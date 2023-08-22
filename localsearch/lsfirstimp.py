import random

from structure import solution

def improve(sol):
    improve = True
    while improve:
        improve = tryImprove(sol)


def tryImprove(sol):
    selected, unselected = createSelectedAndUnselected(sol)
    random.shuffle(selected)
    random.shuffle(unselected)
    for s in selected:
        ds = solution.distanceToSol(sol, s)
        for u in unselected:
            du = solution.distanceToSol(sol, u, without=s)
            if du > ds:
                solution.removeFromSolution(sol, s, ds)
                solution.addToSolution(sol, u, du)
                return True
    return False


def createSelectedAndUnselected(sol):
    selected = []
    unselected = []
    n = sol['instance']['n']
    for v in range(n):
        if solution.contains(sol, v):
            selected.append(v)
        else:
            unselected.append(v)
    return selected, unselected
