if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
    import GS_R2Q_Configuration_Data as ConfigData
    ConfigData.saveProductAttributes(Quote, Product)