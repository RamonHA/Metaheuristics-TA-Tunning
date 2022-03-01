
from trading.processes import Bot
from datetime import date
import argparse

from functions import *

def bot(args):
    b = Bot(
        broker = "mevtaml",
        fiat = "mx",
        commission=args.comission,
        end = args.end,
        subdivision="sector",
        parallel = True
    )

    b.analyze(
        frequency="1m",
        test_time=1,
        analysis={
            "DE":{
                "type":"prediction",
                "time":240,
                "function":func
            }
        }
    )

    b.optimize(
        balance_time=args.time,
        value = args.pv,
        exp_return=True,
        risk = args.opt,
        objective=args.target,
        target_return = args.return_target
    )

    b.run()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-portfolio-value", "-pv", dest="pv", help = "Portfolio Value", nargs='?', const=0, type=int)
    parser.add_argument("-comission", "-c", dest="comission", help = "Broker's comission", nargs='?', const=0, type=float)
    parser.add_argument("-end", "-e", dest="end", help = "Month to make prediction of. Months beginning. Set Default to date.today()", nargs='?', const=date.today(), type=str)
    parser.add_argument("-opt", "-o", dest="opt", help = "Optimization objective", nargs='?', const="efficientcdar", type=str)
    parser.add_argument("-target", dest="target", help = "Optimization target", nargs='?', const="mincdar", type=str)
    parser.add_argument("-time", "-e", dest="time", help = "Time to consider for optimization", nargs='?', const=12, type=int)
    parser.add_argument("-return-target", "-rt", dest="return_target", help = "Return target if target is efficientreturn", nargs='?', const=0.02, type=float)

    args = parser.parse_args()

    bot(
        args = args
    )

