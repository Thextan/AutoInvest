import os
import json
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API


def main():
    """
    My first attempt at pulling data from Oanda
    """

    oanda_environment = 'Practice'
    if oanda_environment == 'Live':
        # oanda_account_id = os.environ['OANDA_ACCOUNTID']
        oanda_access_token = os.environ['OANDA_ACCESS_TOKEN']
        # oanda_hostname = "api-fxtrade.oanda.com"
    else:
        # oanda_account_id = os.environ['OANDA_ACCOUNTID_DEV']
        oanda_access_token = os.environ['OANDA_ACCESS_TOKEN_DEV']
        # oanda_hostname = "api-fxpractice.oanda.com"
    # oanda_port = "443"

    client = API(oanda_access_token)
    instrument, granularity = "EUR_USD", "M15"
    _from = "2021-03-01T00:00:00Z"
    params = {
        "from": _from,
        "granularity": granularity
    }
    fn = "/tmp/{}.{}.json".format(instrument, granularity)
    if os.path.isfile(fn):
        os.remove(fn)
    
    with open(fn, "w") as OUT:
        # The factory returns a generator generating consecutive
        # requests to retrieve full history from date 'from' till 'to'
        for r in InstrumentsCandlesFactory(instrument=instrument, params=params):
            client.request(r)
            OUT.write(json.dumps(r.response.get('candles'), indent=2))

if __name__ == "__main__":
    main()


