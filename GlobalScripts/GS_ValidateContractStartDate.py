newValue = arg.NewValue
oldValue = arg.OldValue
cf_endDate = Quote.GetCustomField("EGAP_Contract_End_Date")
if Quote.GetCustomField("Quote Type").Content in ['Contract New','Contract Renewal']:
    if newValue:
        newDate = UserPersonalizationHelper.CovertToDate(newValue)
        #now = Quote.EffectiveDate
        endDate = UserPersonalizationHelper.CovertToDate(cf_endDate.Content) if cf_endDate.Content != '' else ''
        #isValid = DateTime.Compare(newDate , now) > -1
        '''
        if not isValid:
            sender.Content = oldValue
            Quote.Save(False)
        '''
        if endDate != '':
            isValidEndDate = DateTime.Compare(endDate , newDate) > 0
            '''Set End Date as none if New Start Date is greater than the End Date'''
            if not isValidEndDate:
                sender.Content = oldValue
                # Quote.Save(False)
            else:
                Quote.MainItems[0].IsComplete = False
else:
    if newValue:
        newDate = UserPersonalizationHelper.CovertToDate(newValue)
        now = newDate.Today
        endDate = UserPersonalizationHelper.CovertToDate(cf_endDate.Content) if cf_endDate.Content != '' else ''
        isValid = DateTime.Compare(newDate , now) > -1
        if not isValid:
            sender.Content = oldValue
            # Quote.Save(False)
        elif endDate != '':
            isValidEndDate = DateTime.Compare(endDate , newDate) > -1
            '''Set End Date as none if New Start Date is greater than the End Date'''
            if not isValidEndDate:
                cf_endDate.Content = ''
                # Quote.Save(False)