if Quote:
    Product.Attr('quoteCurrency_hwos').AssignValue(Quote.SelectedMarket.CurrencyCode)
else:
    Product.Attr('quoteCurrency_hwos').AssignValue('USD')