import pandas as pd

from pymoo.algorithms.so_de import DE
from pymoo.optimize import minimize

from sklearn.ensemble import RandomForestRegressor

from trading.assets.assets import TimeSeries
from trading.mev.mev import mevs
from trading.metaheuristics.ta_tunning import TATunning

GEN = 20

def causality(inst):

    # Causality
    mev = TimeSeries(mevs("all", "1m"))
    ur = mev.unit_roots(ensure_no_ut = True)
    targets = [ 'industrial', 'materiales', 'financiero', 'consumo frecuente', 'consumo no basico', 'salud', 'telecomunicaciones','mexbol' ]
    c = mev.causality( targets =  targets )

    # Get causal varibles for our target sector
    if inst.descr["sector"] not in c.columns: 
        print("Sector for {} is {}". format( inst, inst.descr["sector"] ))
        return None

    c_targets = list( c[ c[ inst.descr["sector"] ] == 1 ].index )

    inst.df = pd.concat([
        inst.df,
        mev.df[ c_targets ]
    ], axis = 1).dropna()

    if len(inst.df) == 0:
        return None

    return inst 

def metaheuristic(inst):
    
    algorithm = DE(
        pop_size = 100,
        variant="DE/best/2/bin",
        CR = 0.8,
        F = 0.1,
        dither = "scalar",
    )

    problem = TATunning(
        asset = inst,
        regr = RandomForestRegressor(),
        xl = 3,
        xu = 50,
        verbose = 0,
        n_var = 11
    )

    # try:
    res = minimize(
        problem,
        algorithm,
        ("n_gen", GEN),
        seed = 1,
        verbose = False
    )
    # except Exception as e:
    #     print("{} with exception {}".format( inst, e ))
    #     return None

    problem.update_ta( res.X.astype(int) )

    predict = problem.predict(for_real = True)

    aux = predict[-1] if predict is not None else None

    return aux

def func(inst):
    print("My Function for ", inst)
    inst = causality(inst)

    if inst is None: 
        return None

    pred = metaheuristic(inst)
    return pred

def test():
    print(GEN)