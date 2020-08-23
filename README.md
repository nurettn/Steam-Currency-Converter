<h3 align = "center">
    <img src = "https://github.com/nurettinabaci/Steam-Currency-Converter/blob/master/csgo_trader.png" alt = "Logo" />
</h3>

---
# Steam Currency Converter

Takes scraped raw value as input, extracts its price and currency 
and converts price to target currency.

The up-to-date available currencies to customers on Steam are can be found in this 
[documentation](https://partner.steamgames.com/doc/store/pricing/currencies).
 

## Usage
1. This API uses [fixer.io](https://fixer.io/) currency API inside it. You should take
an API key from [fixer.io](https://fixer.io/) and put it in environment variable.

    ```FIXERIO_API_KEY="api_key"```
 
   (Note: In the code, the API endpoint is created as below:

   ```url = "http://data.fixer.io/api/latest?access_key=" + api_key``` )
2. Before converting your raw values, you should create a json file 
with the code below. Currency values are changing frequently during 
the daytime, so you can update values by rerunning the function.
     
    ```SteamCurrencyExchanger.updateCurrencyJSONFile()``` 

3. Now you can give your scraped raw price strings as below and get
price in targeted currency.

    ```python
   >>> exchanger = SteamCurrencyExchanger()
  
   >>> myPrice1: str = exchanger.convertPrice('R$ 13,05')
   >>> myPrice1
   '17.03 TRY'
   
   >>> myPrice2: str = exchanger.convertPrice('₪57.00')
   >>> myPrice2
   '122.92 TRY'
   
   >>> myPrice3: str = exchanger.convertPrice('$1,095.85 USD')
   >>> myPrice3
   '8035.91 TRY'
   ```
    

## Contribution
Please open an issue if there is an unhandled currency value so we
can append it to codebase.

Pull requests are welcome. For major changes, please open an issue 
first to discuss what you would like to change.

## License
This repository is licensed under the MIT License. Please see the 
[LICENSE](https://github.com/nurettinabaci/Steam-Currency-Converter/blob/master/LICENSE)
file for more details.

 