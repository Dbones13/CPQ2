isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    Product.GetContainerByName('CB_EC_migration_to_C300_UHIO_Configuration_Cont').Rows[0].GetColumnByName('CB_EC_Do_you_want_new_TCB_cables_or_just_the_Adapter_cables').SetAttributeValue('Yes - New TCB cables 10m')