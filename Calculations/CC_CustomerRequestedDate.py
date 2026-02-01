def getCFValue( field):
    return Quote.GetCustomField(field).Content

if  getCFValue("Quote Tab Booking LOB") == 'LSS' and getCFValue("Quote Type") == 'Parts and Spot' and Item['QI_Customer_Requested_Date'].Value:
    newDate =Item['QI_Customer_Requested_Date'].Value
    today = DateTime.Today
    isValid= DateTime.Compare(newDate , today) > -1

    if not isValid:
        Item['QI_Expedite_Fees'].Value = 0
        Item['QI_Customer_Requested_Date'].Value = None
        if not Quote.Messages.Contains(Translation.Get('Error.DateInPast')):
            Quote.Messages.Add(Translation.Get('Error.DateInPast'))
    elif isValid and not getCFValue('Customer Requested Date'):
        Item['QI_Expedite_Fees'].Value = 0
        Item['QI_Customer_Requested_Date'].Value = None
        if not Quote.Messages.Contains(Translation.Get('Error.EnterCustomerRequestedDate')):
            Quote.Messages.Add(Translation.Get('Error.EnterCustomerRequestedDate'))
    else:
        custReqDate = UserPersonalizationHelper.CovertToDate(getCFValue('Customer Requested Date'))
        dateWithinLimit =  DateTime.Compare(custReqDate, Item['QI_Customer_Requested_Date'].Value) > -1
        if not dateWithinLimit:
            Item['QI_Expedite_Fees'].Value = 0
            Item['QI_Customer_Requested_Date'].Value = None
            if not Quote.Messages.Contains(Translation.Get('Error.DateBeyondCustomerReqDate')):
                Quote.Messages.Add(Translation.Get('Error.DateBeyondCustomerReqDate'))
elif not(Item['QI_Customer_Requested_Date'].Value) and getCFValue("Quote Tab Booking LOB") == 'LSS' and getCFValue("Quote Type") == 'Parts and Spot' :
    Item['QI_Expedite_Fees'].Value = 0