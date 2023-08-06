# denarius

currency and other utilities

>If you don't find a way to make money while you sleep, you will work until you die. -- Warren Buffett

# introduction

denarius is a project, not a finished product. It features various utilities for collating cryptocurrency, mining, financial and other data, for plotting data and for accessing bank accounts. It features analyses of data for systematic descriptions, for predictions, for arbitrage etc.

# setup

```Bash
sudo apt-get install sqlite

wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -xvzf geckodriver-v0.19.1-linux64.tar.gz
rm geckodriver-v0.19.1-linux64.tar.gz
chmod +x geckodriver
sudo cp geckodriver /usr/local/bin/

sudo pip install denarius
```

# Bitcoin values

![](media/2010_07_17--2017_01_20_Bitcoin_EUR.png)

![](media/2016-12--2017-01_Bitcoin_EUR.png)

The function `ticker_Bitcoin` returns data of the following form:

```Python
{'volume': 2050.1665002833397, 'last': 992.2553834529656, 'timestamp': 1487551580.0, 'bid': 991.8303740083114, 'vwap': 993.3415187004156, 'high': 1002.9278428409522, 'low': 981.3656970154892, 'ask': 992.2553834529656, 'open': 993.3887419720438}
```

It accesses data from Bitstamp.

|**feature**|**description**                            |
|-----------|-------------------------------------------|
|last       |last Bitcoin price                         |
|high       |last 24 hours price high                   |
|low        |last 24 hours price low                    |
|vwap       |last 24 hours volume weighted average price|
|volume     |last 24 hours volume                       |
|bid        |highest buy order                          |
|ask        |lowest sell order                          |
|timestamp  |UNIX timestamp date and time               |
|open       |first price of the day                     |

The function `data_historical_Bitcoin` returns by default data of the following form:

```Python
{'bpi': {'2017-02-17': 992.1077, '2017-02-16': 969.2414, '2017-02-15': 952.6512, '2017-02-14': 954.1432, '2017-02-13': 940.7982, '2017-02-12': 940.1764, '2017-02-11': 949.3397, '2017-02-10': 933.4325, '2017-02-19': 991.254, '2017-02-18': 997.0854}, 'time': {'updated': 'Feb 20, 2017 00:20:08 UTC', 'updatedISO': '2017-02-20T00:20:08+00:00'}, 'disclaimer': 'This data was produced from the CoinDesk Bitcoin Price Index. BPI value data returned as EUR.'}
```

With the option `return_list`, it returns data of the following form:

```Python
[['2017-02-10', 933.4325], ['2017-02-11', 949.3397], ['2017-02-12', 940.1764], ['2017-02-13', 940.7982], ['2017-02-14', 954.1432], ['2017-02-15', 952.6512], ['2017-02-16', 969.2414], ['2017-02-17', 992.1077], ['2017-02-18', 997.0854], ['2017-02-19', 991.254]]
```

With the option `return_UNIX_times`, it returns data of the following form:

```Python
[[1486684800, 933.4325], [1486771200, 949.3397], [1486857600, 940.1764], [1486944000, 940.7982], [1487030400, 954.1432], [1487116800, 952.6512], [1487203200, 969.2414], [1487289600, 992.1077], [1487376000, 997.0854], [1487462400, 991.254]]
```

# LocalBitcoins

LocalBitcoins data is available via its API. For example, the following URL gives data on current trades in GBP available by national bank transfer:

- <https://localbitcoins.com/buy-bitcoins-online/GB/united-kingdom/national-bank-transfer/.json>

The data returned by the API is of a form [like this](data/2017-03-07T2249Z.txt).

The function `values_Bitcoin_LocalBitcoin` returns the price values returned by calling the API in this way.

```Python
import denarius
denarius.values_Bitcoin_LocalBitcoin()
```

The script `loop_save_LocalBitcoins_values_to_database.py` loop records LocalBitcoins data to database. To address closed gateways arising from repeat calls, the script could be used in a way like the following:

```Bash
while true; do
    loop_save_LocalBitcoins_values_to_database.py --timeperiod=3600
    sleep 5400
done
```

The script `login_web_LocalBitcoins.py` is available for a quick login to LocalBitcoins using Selenium. It depends on the credentials file `~/.lbc` existing and containing information of the following form:

```Python
username = "xxxxxxxxxx"
passcode = "xxxxxxxxxx"
secret   = "xxxxxxxxxxxxxxxxxxxxxxxx"
```

# databases

A database of Bitcoin values can be saved in the following ways:

```Python
import denarius
denarius.save_database_Bitcoin(filename = "database.db")
```

```Python
import denarius
denarius.save_database_Bitcoin(filename = "database_Bitcoin_EUR.db", currency = "EUR")
denarius.save_database_Bitcoin(filename = "database_Bitcoin_GBP.db", currency = "GBP")
```

# graphs

The function `save_graph_Bitcoin` creates a graph of Bitcoin historical values over a specified time. The function `save_graph_LocalBitcoins` creates a graph of LocalBitcoins Bitcoin lowest prices in GBP as recorded in a database by the script `loop_save_LocalBitcoins_values_to_database.py`.

## denarius_graph_Bitcoin

The script `denarius_graph_Bitcoin.py` displays a PyQt GUI with a graph of the last Bitcoin values.

```Bash
denarius_graph_Bitcoin.py --help
```

```Bash
denarius_graph_Bitcoin.py
```

```Bash
denarius_graph_Bitcoin.py --currency=EUR --days=100
```

![](media/denarius_graph_Bitcoin.png)

## LocalBitcoins

A graph can be generated of Bitcoin GBP value versus LocalBitcoins GBP lowest value:

```bash
import denarius
denarius.save_graph_Bitcoin_LocalBitcoins()
```

![](media/Bitcoin_LocalBitcoins_lowest_price_GBP.png)

A graph can be generated of Bitcoin GBP value versus LocalBitcoins GBP lowest 5 values:

```bash
import denarius
denarius.save_graphs_Bitcoin_LocalBitcoins()
```

![](media/Bitcoin_LocalBitcoins_prices_GBP.png)

A graph can be generated of LocalBitcoins normalized prices over days:

![](media/LocalBitcoins_Bitcoin_lowest_price_GBP_days.png)

A graph can be generated of LocalBitcoins normalized prices over weeks:

![](media/LocalBitcoins_Bitcoin_lowest_price_GBP_weeks.png)

A graph can be generated of LocalBitcoins non-normalized prices over weeks:

![](media/LocalBitcoins_Bitcoin_lowest_price_GBP_weeks_not_normalized.png)

## Bollinger bands

![](media/LocalBitcoins_1_Bollinger_bands.png)

# KanoPool

KanoPool records for addresses can be recorded to CSV in a way like the following:

```Bash
denarius_loop_save_KanoPool.py --help

denarius_loop_save_KanoPool.py --addresses=1Miner7R28PKcTRbEDwQt4ykMinunhTehs --interval=10
```

The CSV data can be analysed using the Jupyter Notebook [KanoPool.ipynb](https://github.com/wdbm/denarius/blob/master/KanoPool.ipynb).

# Nanopool

Nanopool records for addresses can be recorded to CSV in a way like the following:

```Bash
denarius_loop_save_Nanopool.py --help

denarius_loop_save_Nanopool.py --addresses=0xbd3f1126d4c20f72a77e38dfda18622a6d663cd0
```

The CSV fields are, in order, as follows:

- datetime
- account
- balance
- earnings_per_day_BTC
- earnings_per_day_ETH
- earnings_per_day_EUR
- earnings_per_hour_BTC
- earnings_per_hour_ETH
- earnings_per_hour_EUR
- earnings_per_minute_BTC
- earnings_per_minute_ETH
- earnings_per_minute_EUR
- earnings_per_month_BTC
- earnings_per_month_ETH
- earnings_per_month_EUR
- earnings_per_week_BTC
- earnings_per_week_ETH
- earnings_per_week_EUR
- hashrate
- hashrate12hr
- hashrate1hr
- hashrate24hr
- hashrate3hr
- hashrate6hr
- hashrate_pool
- pool_miners
- pool_workers

# Slush Pool

Slush Pool records for an address can be recorded to CSV in a way like the following:

```Bash
denarius_loop_save_SlushPool.py --help

denarius_loop_save_SlushPool.py --addresses=1Miner7R28PKcTRbEDwQt4ykMinunhTehs --interval=60 --alarm=11800000 --slushloginname=user --slushworkername=worker1
```

The CSV fields are, in order, as follows:

- address
- hash rate
- shares
- UNIX timestamp
- unconfirmed reward in Bitcoin
- confirmed reward in Bitcoin
- total reward (confirmed + unconfirmed) in Bitcoin
- total payout since script launch in Bitcoin
- number of blocks found since script launch

The CSV data can be analysed using the Jupyter Notebook [SlushPool.ipynb](https://github.com/wdbm/denarius/blob/master/SlushPool.ipynb).

# banks

The banks module provides utilities for getting transactions of a bank account (Monzo or RBS) using the [Monzo API](https://monzo.com/docs/) and the [Teller API](https://teller.io/). To use this module, credentials files should be created. 

Access the [Monzo developers portal](https://developers.monzo.com) and create a new OAuth confidential client. Set the redirect URL for the client to <https://github.com/pawelad/pymonzo>. Create a URL of the following form using the client ID string:

```
https://auth.getmondo.co.uk/?response_type=code&redirect_uri=https://github.com/pawelad/pymonzo&client_id=<YOUR_CLIENT_ID>
```

Access this URL and authorize the client application. The confirmation e-mail sent contains a URL of the following form:

```
https://github.com/pawelad/pymonzo?code=<YOUR_AUTH_CODE>&state=
```

Copy the authorization code from this URL and then access the URL to authorize the client application.

Launch an interactive Python session and, using the client credentials and the `pymonzo` API interface, generate an access token and a refresh token.

```Python
client_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
auth_code = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

from pymonzo import MonzoAPI

monzo = MonzoAPI(
    client_id     = client_id,
    client_secret = client_secret,
    auth_code     = auth_code
)
```

This saves an authorization that lasts 48 hours to the file `~/.pymonzo-token`, which contains a dictionary of the following form:

```Python
{
    "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "client_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "expires_at": 1517106306.8881364,
    "expires_in": 172799,
    "refresh_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "token_type": "Bearer",
    "user_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

Now, API access can be tested by calling the `monzopy` Monzo API interface without any arguments (such that it loads tokens from the file `~/.pymonzo-token` and manages token refreshes).

```Python
from pymonzo import MonzoAPI

monzo = MonzoAPI()

print(monzo.accounts())
print(monzo.balance())
print(monzo.transactions())
```

For RBS, the credentials file (by default `~/.rbs`) should have content of the following form:

```Python
token_teller        = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
account_code_teller = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Pandas DataFrames of transactions can be retrieved in ways like the following:

```Python
import denarius.banks
df = denarius.banks.transactions_DataFrame_Monzo()
df = denarius.banks.transactions_DataFrame_RBS()
```

A payment can be searched for in ways like the following:

```Python
denarius.banks.payment_in_transactions_Monzo(reference = "271828182", amount = 314)
denarius.banks.payment_in_transactions_RBS(reference = "271828182", amount = 314)
```

These functions search the "counterparty_reference" and "description" fields of a DataFrame of bank account transactions for a specified reference. If the reference is found, the specified amount of the payment is compared to the sum of amounts found for the specified reference in the "amount" field. They return a dictionary of the following form:

```Python
{
    "reference_found":   bool,      # True if reference found
    "amount_correct":    bool,      # True if sum of amounts found is amount specified
    "valid":             bool,      # True if reference found and amount correct
    "transactions"       DataFrame, # DataFrame of matches
    "amount_difference": float      # difference between amount specified and sum of amounts found
}
```

So, these functions could be used in a straightforward boolean way to check if a payment has been made:

```Python
denarius.banks.payment_in_transactions_Monzo(reference = "271828182", amount = 314)["valid"]
```

They also could be used in a more involved way to account for occasions in which a payment is found but has an incorrect amount and a further payment with the same reference must be requested.

Both the `transactions_DataFrame` and `payment_in_transactions` functions have the option `print_table` which can print to terminal a table of the transactions under consideration:

```Python
df = denarius.banks.transactions_DataFrame_Monzo(print_table = True)
```

The script `print_table_bank_account.py` uses this functionality to print to terminal a table of transactions from a specified bank.

# Kraken

The Kraken module provides utilities for getting current balances of currencies held, buying Bitcoin for Euros at the last market price, and sending Bitcoin from Kraken to an address, the key for which has been verified on Kraken. The scripts `print_Kraken_balances.py`, `print_Kraken_last_price_BTC_EUR.py` and `buy_BTC_for_EUR_last_price_on_Kraken.py` all use these functionalities.

The Kraken module depends on the credentials file `~/.kraken` existing and containing the key on the first line and the secret on the second line.

Bitcoin can be sent from Kraken to an address key in a way like the following:

```Python
import denarius.Kraken

denarius.Kraken.start_API()
print(denarius.Kraken.send_XBT(amount = 0.1, address_key = "BIGMONEY"))
```

The script `login_web_Kraken.py` is available for a quick login to Kraken using Selenium. It depends on the credentials file `~/.kraken_credentials` existing and containing information of the following form:

```Python
username = "xxxxxxxxxx"
passcode = "xxxxxxxxxx"
secret   = "xxxxxxxxxxxxxxxxxxxxxxxx"
```

# RBS

The RBS module provides utilities for getting the balance and recent transactions of an RBS account using the RBS banking web interface, Selenium and Firefox. For convenience, account details can be stored in a credentials file, which is assumed by default to be `~/.rbs`. The account code is an alphanumeric code extracted from the web interface. The content of a credentials file is of the following form, which is Python code:

```Python
customer_number = "XXXXXXXXXX"
PIN             = "XXXXXX"
passcode        = "XXXXXXXXXXXXXXXXXXXX"
account_code    = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

A dictionary of the current balance and a pandas DataFrame of recent transactions is returned by the function `RBS.account_status`.

```Python
import denarius.RBS

status  = RBS.account_status()
balance = status["balance"]
df      = status["transactions"]
```

The DataFrame features the fields `date`, `description` and `amount`. A transaction containing a certain reference or description could be selected in the following way:

```Python
df[df["description"].str.contains("transaction reference 123")]
```

The existence of a transaction can be tested in a way like the following:

```Python
if df[df["description"].str.contains("transaction reference 123")].values.any():

    print("transaction found")

else:

    print("transaction not found")
```

The script `get_account_balance_RBS.py` is available to open an RBS account web interface and to display the current balance and recent transactions in the terminal, optionally in a loop.

```Bash
get_account_balance_RBS.py --loop
```

The script `detect_transaction_RBS.py` is available to search for a transaction or transactions with a specified reference.

```Bash
detect_transaction_RBS.py --reference=123
```

The script `loop_save_RBS_to_CSV.py` is available to loop save RBS transactions and balance to CSV, merging with recorded CSV data to avoid recording duplicates.

# Santander

The Santander module provides utilities for getting recent transactions using the Santander banking web interface, Selenium and Firefox. Account details are stored in a credentials file, which is assumed by default to be `~/.santander`. The content of a credentials file is of the following form, which is Python code:

```Python
customer_number          = "XXXXXXXX"
customer_PIN             = "XXXXX"
security_question_answer = "XXXXXXXX"
```

A DataFrame of recent transactions is returned by the function `Santander.transactions_DataFrame`. The script `loop_save_Santander_to_CSV.py` saves transactions to CSV in a continuous loop. The function `Santander.payment_in_transactions_CSV` can search in transactions recorded in CSV for a specified transaction reference together with a specified value and returns a boolean to indicate whether the transaction was detected.

# arbitrage

The script `loop_save_arbitrage_data_Kraken_LocalBitcoins_UK.py` records data for arbitrage between Kraken and LocalBitcoins UK.

The script `loop_display_arbitrage_data.py` is available for display of recorded data and current prices for arbitrage between Kraken and LocalBitcoins UK.

![](media/loop_display_arbitrage_data.png)

# paper wallets for Bitcoin, QR codes of keys

The script `create_QR_codes_of_public_and_private_keys.py` creates a QR code for a specified public key and private key and enables optional specification of the size of the resulting PNG images. It loads the keys from a Python file (`keys.py` by default) which defines the string variables `key_public` and `key_private`.

The script `create_paper_wallet.py` creates a QR code for a specified public key and private key. It then creates an image of a Bitcoin paper wallet. It loads the keys from a Python file (`keys.py` by default) which defines the string variables `key_public` and `key_private`.

![](media/paper_wallet.png)

# Faster Payments Service

- [2018-01-14 participants](http://www.fasterpayments.org.uk/about-us/current-participants)

- Barclays
- Citi
- Clear Bank
- Clydesdale Bank
- The Co-operative Bank
- HSBC
- Lloyds Bank
- Metro Bank
- Monzo
- Nationwide
- NatWest
- Northern Bank
- Raphaels Bank
- Royal Bank of Scotland
- Santander
- Starling Bank
- Turkish Bank UK

# SEPA Instant

- [2018-01-14 participants](https://www.europeanpaymentscouncil.eu/sites/default/files/participants_export/sepa_instant_credit_transfer/sepa_instant_credit_transfer.pdf?v=1515763349)

- Austria
- Belgium
- Bulgaria
- Estonia
- France
- Germany
- Italy
- Latvia
- Lithuania
- Malta
- Netherlands
- Spain
