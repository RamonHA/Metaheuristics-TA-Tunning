import warnings
warnings.filterwarnings("ignore")

from trading.processes import Simulation
from trading.mev.mev import mevs
from trading.metaheuristics.ta_tunning import TATunning

from trading.assets.assets import TimeSeries
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

from pymoo.algorithms.so_cmaes import CMAES
from pymoo.algorithms.so_de import DE
from pymoo.optimize import minimize


# Debbuging help
# from trading.assets import Asset
# inst = Asset( "ABBV.MX", frequency="1m", start = date(1998,11,1), end = date(2018,11,30), broker = "mevtaml", fiat = "mx", from_ = "db" )

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
        ("n_gen", 2),
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

if __name__ == "__main__":

    portfolio_value = 100000

    s = Simulation(
        broker = "mevtaml", # change if different project name in configuration
        fiat = "mx",
        commission=0, # If wanted to test with brokers commisions
        assets=None, # If you didnt add assets in configuration step, you can add the dictionary in this step
                    # just change the broker name to default
        end = date(2020,12,1), # If more recent data, simulation end time can be extended
        simulations=36, # Amount of simulations to run (based on the analysis frequency period)
        realistic=1,
        verbose = 2,
        subdivision = "sector",
        parallel = True
    )


    s.analyze(
        frequency="1m",
        test_time=1,
        analysis={
            "DE":{
                "type":"prediction",
                "time":240,
                "function":func
            }
        },
        run = False
    )

    for bt in [12, 24, 48]:
        for r, o in [ ("efficientfrontier", "minvol"), ("efficientsemivariance", "minsemivariance"), ("efficientcvar", "mincvar"), ("efficientcdar", "mincdar") ]:

            print( bt, r, o )

            s.optimize(
                balance_time = bt,
                value = portfolio_value,
                exp_return = True,
                risk = r,
                objective = o,
                run = False
            )


    results = s.results_compilation()

    print(results)
    
    df = s.behaviour( results.loc[ 0, "route" ] )

    df[ "acc" ].plot()
    plt.show()
