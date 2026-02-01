newDateValue = arg.NewValue
oldDateValue = arg.OldValue
cf_endDate = Quote.GetCustomField("SC_CF_CURANNDELENDT")
from GS_SC_Extension_Error_Msg import *
if newDateValue:
    newDate = UserPersonalizationHelper.CovertToDate(newDateValue)
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
            sender.Content = oldDateValue
            #Quote.Save(False)
	if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content == 'True':
         Extension_Func(Quote)