# Update assets info

#!/bin/bash

historic_download -broker mevtaml -fiat mx -frequency 1m -from "yahoo" -verbose

historic_download -broker mevtaml -fiat mx -frequency 1d -from "yahoo" -verbose

mev_download -mode all -frequency 1m -verbose

