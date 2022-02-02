# Stock price prediction with MEV, TA, and ML ( mevtaml )

Use of macroeconomic variables, technical analysis and Machine Learning to make prediction of stocks quoted in the  Mexican Stock exchange (MSE).

Algorith of the Computer Science Master Thesis project: "BMV stocks return prediction using macro economics variables,technical analysis, and machine learning".

## Technical Requirements.

Installation of python3, and python packages "trading".

### trading package extra configuration
Once the trading python package is installed in the system, and configured, we configure the stocks used to make our analysis.

Stocks quoted in the MSE are in file "MSE_stocks.json"

1. Add assets of project "msetaml". "msetaml" is just the name of the project, if wanted to name it differently, just keep in mind make the change inside the "main.py".
```
$ add_assets -broker mevtaml -json "path/to/json/MSE_stocks.json"
```

### MEV sources API
We requier to communicate with external APIS for MEV data, these data sources are: Inegi and SIE.

1. Get Inegi API key at :
```
$ add_api -name inegi -apikey <APIKEY>
```

2. Get SIE API key at: 
```
$ add_api -name sie -apikey <APIKEY>
```


## Reference.
