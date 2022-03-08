
import warnings
warnings.filterwarnings("ignore")

from trading.processes import Bot
from trading.func_brokers import historic_download, mev_download
from datetime import date
import argparse
import time
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
    parser.add_argument("-time", "-t", dest="time", help = "Time to consider for optimization", nargs='?', const=12, type=int)
    parser.add_argument("-return-target", "-rt", dest="return_target", help = "Return target if target is efficientreturn", nargs='?', const=0.02, type=float)
    parser.add_argument( "--mev-download", "-md", dest = "md", action = "store_true", help = "Not Update MEVs DB" )
    parser.add_argument( "--stock-download", "-sd", dest = "sd", action = "store_true", help = "Not Update Stocks DB" )

    args = parser.parse_args()

    args.comission = 0 if args.comission is None else args.comission
    args.end = date.today() if args.end is None else args.end
    args.opt = "efficientcdar" if args.opt is None else args.opt
    args.target = "mincdar" if args.target is None else args.target
    args.time = 12 if args.time is None else args.time
    args.return_target = 0.02 if args.return_target is None else args.return_target
    args.pv = 0 if args.pv is None else args.pv

    if not args.sd:
        historic_download(
            broker="mevtaml",
            fiat = "mx",
            frequency="1m",
            verbose=False
        )

        time.sleep(1)

    if not args.md:
        mev_download(
            mode = "all",
            frequency = "1m",
            verbose=False
        )

        time.sleep(1)

    bot(
        args = args
    )

