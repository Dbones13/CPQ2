newDateValue = arg.NewValue
oldDateValue = arg.OldValue
startDate = Quote.GetCustomField("SC_CF_CURANNDELSTDT").Content
from GS_SC_Extension_Error_Msg import *
if  Quote.GetCustomField("Quote Type").Content == "Contract New":
    if Quote.GetCustomField("EGAP_Contract_End_Date").Content == '':
    	Quote.GetCustomField("EGAP_Contract_End_Date").Content  = str(Quote.GetCustomField("SC_CF_CURANNDELENDT").Content)
if newDateValue:
    newDate = UserPersonalizationHelper.CovertToDate(newDateValue)
    oldDate = UserPersonalizationHelper.CovertToDate(oldDateValue) if oldDateValue else ''
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
        '''If Old End Date is a valid Future Date'''
        '''
        if oldDate != '':
            if DateTime.Compare(oldDate , now) > -1:
                sender.Content = oldValue
        '''
        #Quote.Save(False)
    if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content == 'True':
        Extension_Func(Quote)