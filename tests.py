from steam_currency import SteamCurrencyExchanger

def testValues(*args) -> None:
    testList = [
        '$1,095.85 USD',
        '¥ 16.50',
        '833,03 pуб',
        '$11.99 USD',
        '2390,35 pуб.',
        'R$ 13,05',
        '220,--€',
        '1,58€',
        'A$ 50.00',
        '₪57.00',
        'HK$ 300.00',
        'CDN$ 2.77',
        '£12.25',
        'RM69.58',
        'Mex$ 52.99'
    ]

    if len(args) > 0:
        for newValues in args:
            testList.append(newValues)

    print('-' * 30)
    for val in testList:
        try:
            print("Input: " + val + '\t\t' + '-----> '
                  + exchanger.convertPrice(val, 'TRY') + '  --> ' + ' \t\tSUCCESS')
        except Exception:
            print("<-----ERROR-----> :", val)
            continue
    print("Test is finished...")
    print('-' * 30)


exchanger = SteamCurrencyExchanger()
# exchanger.updateCurrencyJSONFile()
testValues()