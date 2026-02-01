newValue = arg.NewValue
oldValue = arg.OldValue

if newValue:
    newDate = UserPersonalizationHelper.CovertToDate(newValue)
    now = newDate.Today

    isValid = DateTime.Compare(newDate , now) > -1
    if not isValid:
        sender.Content = oldValue
    else:
        for item in Quote.Items:
            item['QI_Customer_Requested_Date'].Value = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('Customer Requested Date').Content)