import requests
import json
import locale
from decouple import config

# currencyJSON = response.json() # Euro based currency
# coefficient = currencyJSON["rates"]['EUR']

steam_currencies = ['A$', 'ARS$', None, 'R$', 'CDN$', 'CHF', 'CLP$', None, 'COL$', '₡', '€', '£', 'HK$', '₪', 'Rp', '₹',
                    '¥', '₩', 'KD', '₸', 'Mex$', 'RM', 'kr', 'NZ$', 'S/.', 'P', 'zł', 'QR', 'pуб', 'SR', 'S$', '฿',
                    'TL', 'NT$', '₴', '$', '$U', '₫', 'R', 'kr']

ISO4217_CurrencyCodes = ['AUD', 'ARS', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'EUR', 'GBP', 'HKD',
                         'ILS', 'IDR', 'INR', 'JPY', 'KRW', 'KWD', 'KZT', 'MXN', 'MYR', 'NOK', 'NZD', 'PEN', 'PHP',
                         'PLN', 'QAR', 'RUB', 'SAR', 'SGD', 'THB', 'TRY', 'TWD', 'UAH', 'USD', 'UYU', 'VND', 'ZAR',
                         'SEK']

currencyJSON = json.load(open("currency.json"))

class SteamCurrencyExchanger(object):

    @staticmethod
    def updateCurrencyJSONFile():
        api_key = config('FIXERIO_API_KEY')  # fixer.io/dashboard
        url = "http://data.fixer.io/api/latest?access_key=" + api_key
        response = requests.get(url)
        currencyJSON = response.json()  # Euro based currency
        with open('currency.json', 'w') as f:
            json.dump(currencyJSON, f, indent=4)

    def convertPrice(self, inputVal='$9999999,999999 USD', currency_type: str = 'TRY') -> str:
        """
        Price converter main function.
        Gets currency and price information from raw input string.
        Converts the price to target currency and returns as string.
        Example usage: newVal = convertPrice('1,58€', 'USD')
        """
        currency_type = currency_type.upper()  # make uppercase
        # inputVal = '2390,35 pуб.'
        inputVal = self.makeReadable(inputVal)
        foreign_currency = self.getISOCurrencyFromString(inputVal)
        actualPriceWithForeignCurrency = self.getPriceFromString(inputVal)  # take base price
        finalPrice = self.getEquivalentValue(actualPriceWithForeignCurrency, foreign_currency,
                                             currency_type)  # convert price
        finalPrice = locale.format_string("%.2f", finalPrice, grouping=True)  # set 2 decimal after comma
        finalPrice = str(finalPrice) + " " + currency_type
        return finalPrice

    def getISOCurrencyFromString(self, s) -> str:
        """Returns the ISO code of the input currency.
        """
        steamCurrency = self.getCurrencySymbolFromString(s)

        # '$2.05 USD' -> '$'.  USD' -> '$'
        if '$' in steamCurrency and 'USD' in steamCurrency:
            steamCurrency = '$'

        iso_equivalent_currency = ISO4217_CurrencyCodes[steam_currencies.index(steamCurrency)]
        return iso_equivalent_currency

    def makeReadable(self, s: str) -> str:
        """Replaces comma with dot and deletes the hypen,
        and strips with the dots.
        """
        s = s.replace(',', '.')
        s = s.replace('-', '')
        s = s.strip('.')
        return s

    def getPriceFromString(self, s) -> float:
        """
        Extracts and returns float price value.
        Firstly replaces colon with dot, deletes digits
        and strips with space, dot, colon and dash characters.
        """
        # number = ''.join((character if character in '0123456789.e' else '') for character in s)
        number = ''.join((character if character in '0123456789.' else '') for character in s)

        try:
            if len(number) > 7:
                number = number.replace('.', '', 1)
                number = float(number)
            else:
                number = float(number)
        except ValueError as val_err:
            print(val_err)
        except Exception as e:
            print(e)

        return number

    def getCurrencySymbolFromString(self, s) -> str:
        """
        Firstly deletes digits and strips with space, dot, colon and dash characters.
        """
        symbol = ''.join([i for i in s if not i.isdigit()])
        symbol = symbol.strip(".,- ")
        return symbol

    def getEquivalentValue(self, price, steamCurrency, targetCurrency='TRY') -> float:
        # Return price as it is if currency types are the same
        if steamCurrency == targetCurrency:
            return price

        # Check if foreignCurrency is base currency type
        if steamCurrency == 'EUR':
            baseKatsayi = 1.0
        else:
            baseKatsayi = float(currencyJSON["rates"][steamCurrency])

        # Fetch the base and target coefficients and calculate value
        hedefKatsayi = float(currencyJSON["rates"][targetCurrency])
        convertedPrice = price * hedefKatsayi / baseKatsayi
        return convertedPrice
