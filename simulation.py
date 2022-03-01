import warnings
warnings.filterwarnings("ignore")

from trading.processes import Simulation

from datetime import date
import matplotlib.pyplot as plt

from functions import *

# Debbuging help
# from trading.assets import Asset
# inst = Asset( "ABBV.MX", frequency="1m", start = date(1998,11,1), end = date(2018,11,30), broker = "mevtaml", fiat = "mx", from_ = "db" )

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
