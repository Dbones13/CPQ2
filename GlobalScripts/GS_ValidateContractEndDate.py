newValue = arg.NewValue
oldValue = arg.OldValue
startDate = Quote.GetCustomField("EGAP_Contract_Start_Date").Content
if Quote.GetCustomField("Quote Type").Content in ['Contract New','Contract Renewal']:
    if newValue:
        newDate = UserPersonalizationHelper.CovertToDate(newValue)
        oldDate = UserPersonalizationHelper.CovertToDate(oldValue) if oldValue else ''
        now = Quote.EffectiveDate
        '''if End Date is a valid Future Date'''
        #isValidFutureDate = DateTime.Compare(newDate , now) > -1
        isValidEndDate = True
        if startDate:
            startDate = UserPersonalizationHelper.CovertToDate(startDate)
            '''if End Date is greater than the Start Date'''
            isValidEndDate = DateTime.Compare(newDate , startDate) > 0
            now = startDate
        '''If New End Date is not valid'''
        if not isValidEndDate:
            sender.Content = ''
        else:
            Quote.MainItems[0].IsComplete = False
        '''If Old End Date is a valid Future Date'''
        '''
            if oldDate != '':
                if DateTime.Compare(oldDate , now) > -1:
                    sender.Content = oldValue
        '''
            # Quote.Save(False)
else:
    if newValue:
        newDate = UserPersonalizationHelper.CovertToDate(newValue)
        oldDate = UserPersonalizationHelper.CovertToDate(oldValue) if oldValue else ''
        now = newDate.Today
        '''if End Date is a valid Future Date'''
        isValidFutureDate = DateTime.Compare(newDate , now) > -1
        isValidEndDate = True
        if startDate:
            startDate = UserPersonalizationHelper.CovertToDate(startDate)
            '''if End Date is greater than the Start Date'''
            isValidEndDate = DateTime.Compare(newDate , startDate) > -1
            now = startDate
        '''If New End Date is not valid'''
        if not isValidEndDate or not isValidFutureDate:
            sender.Content = ''
            '''If Old End Date is a valid Future Date'''
            if oldDate != '':
                if DateTime.Compare(oldDate , now) > -1:
                    sender.Content = oldValue
            # Quote.Save(False)