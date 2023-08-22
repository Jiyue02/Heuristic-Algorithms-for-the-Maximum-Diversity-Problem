from constructives import cgrasp_eff, cgrasp
from localsearch import lsbestimp, lsfirstimp, lsfirstimp_sorted
from structure import instance, solution

def execute(inst, iters, alpha):
    best = None
    for i in range(iters):
        #print("Iter "+str(i+1)+": ", end="")
        # sol = cgrasp_eff.construct(inst, alpha)
        sol = cgrasp.construct(inst, alpha)
        #print("C -> "+str(round(sol['of'], 2)), end=", ")
        lsbestimp.improve(sol)
        #lsfirstimp.improve(sol)
        #lsfirstimp_sorted.improve(sol)
        #print("LS -> "+str(round(sol['of'], 2)))
        if best is None or best['of'] < sol['of']:
            best = sol
    return best
