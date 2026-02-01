if (Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Quote.GetCustomField('R2Q_Save').Content == 'Submit'):
    import GS_R2Q_Configuration_Data as ConfigData
    ConfigData.saveProductAttributes(Quote, Product)
    Quote.Save(False)