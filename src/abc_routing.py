"""Random-key ABC for a fixed-depot directed tour. No route-specific shortcuts."""
import numpy as np
from time import perf_counter

def decode(keys):
    return np.r_[0, np.argsort(keys, kind='stable')+1, 0].astype(int)

def tour_cost(route, matrix):
    return float(matrix[route[:-1],route[1:]].sum())

def validate_route(route, n):
    assert len(route)==n+1 and route[0]==route[-1]==0
    assert sorted(route[1:-1])==list(range(1,n))

def solve(matrix, seed=11, method='ABC', budget=5000, sources=20, limit=50):
    assert method in ('ABC','Random') and budget>=sources and sources>=2
    start=perf_counter()
    rng=np.random.default_rng(seed); dim=len(matrix)-1
    pop=rng.random((sources,dim)); trials=np.zeros(sources,int)
    costs=np.array([tour_cost(decode(x),matrix) for x in pop])
    used=sources; bestidx=int(costs.argmin()); bestkey=pop[bestidx].copy();best=float(costs[bestidx])
    history_fe=[used];history_best=[best]; unique_population=[len({tuple(decode(x)) for x in pop})]
    all_routes={tuple(decode(x)) for x in pop}; same_route=0; scouts=0; candidates=0; neighbor_attempts=0
    def evaluate(v):
        nonlocal used,best,bestkey,candidates
        route=decode(v);validate_route(route,len(matrix))
        score=tour_cost(route,matrix);used+=1;candidates+=1;all_routes.add(tuple(route))
        if score<best:best=score;bestkey=v.copy()
        return score
    def neighbor(i):
        nonlocal same_route, neighbor_attempts
        neighbor_attempts+=1
        k=int(rng.integers(sources-1));k+=k>=i
        j=int(rng.integers(dim));v=pop[i].copy()
        v[j]=np.clip(v[j]+rng.uniform(-1,1)*(v[j]-pop[k,j]),0,1)
        same_route+=int(np.array_equal(decode(v),decode(pop[i])))
        score=evaluate(v)
        if score<costs[i]: pop[i]=v;costs[i]=score;trials[i]=0
        else:trials[i]+=1
    while used<budget:
        if method=='Random':
            # Same first 20 candidates as ABC, then independent random keys.
            v=rng.random(dim);evaluate(v)
            if used%40==0 or used==budget:
                history_fe.append(used);history_best.append(best)
                unique_population.append(None)
            continue
        for i in range(sources):
            if used==budget:break
            neighbor(i)
        # Static roulette probabilities per onlooker phase, as in classical ABC.
        fitness=1/(1+costs);prob=fitness/fitness.sum()
        for _ in range(sources):
            if used==budget:break
            neighbor(int(rng.choice(sources,p=prob)))
        if used<budget and trials.max()>=limit:
            i=int(trials.argmax());pop[i]=rng.random(dim);costs[i]=evaluate(pop[i]);trials[i]=0;scouts+=1
        history_fe.append(used);history_best.append(best)
        unique_population.append(len({tuple(decode(x)) for x in pop}))
    route=decode(bestkey);validate_route(route,len(matrix))
    assert used==budget and np.isclose(tour_cost(route,matrix),best)
    assert np.all(np.diff(history_best)<=1e-9)
    return {'method':method,'seed':seed,'cost_seconds':best,'runtime_seconds':perf_counter()-start,
            'evaluations':used,'route':route.tolist(),'keys':bestkey.tolist(),'unique_routes':len(all_routes),
            'same_route_fraction':same_route/max(1,neighbor_attempts) if method=='ABC' else None,
            'scouts':scouts,'history_fe':history_fe,'history_best':history_best,
            'unique_population':unique_population}

def nearest_neighbor(matrix):
    pending=set(range(1,len(matrix)));route=[0]
    while pending:
        nxt=min(pending,key=lambda j:(matrix[route[-1],j],j));route.append(nxt);pending.remove(nxt)
    route.append(0);return route,tour_cost(np.array(route),matrix)

def held_karp(matrix):
    """Exact dynamic programming for a small directed fixed-depot TSP."""
    m=len(matrix)-1;dp={};parent={}
    for j in range(m):dp[(1<<j,j)]=float(matrix[0,j+1])
    for mask in range(1,1<<m):
        for j in range(m):
            if not(mask>>j&1) or mask==(1<<j):continue
            prev=mask^(1<<j)
            cost,k=min((dp[(prev,k)]+matrix[k+1,j+1],k) for k in range(m) if prev>>k&1)
            dp[(mask,j)]=float(cost);parent[(mask,j)]=k
    mask=(1<<m)-1
    value,j=min((dp[(mask,j)]+matrix[j+1,0],j) for j in range(m))
    rev=[]
    while True:
        rev.append(j+1)
        if mask==1<<j:break
        k=parent[(mask,j)];mask^=1<<j;j=k
    route=[0]+rev[::-1]+[0];validate_route(route,len(matrix))
    assert np.isclose(tour_cost(np.array(route),matrix),value)
    return route,float(value)
