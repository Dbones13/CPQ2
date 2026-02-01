#This script is used for SetQty after effectivedate functionality reset qty to 1. [Workaround script]
#This script was trigged via "CartHeader" template.
from GS_CommonConfig import CL_CommonSettings as CS
from GS_Display_Warning_Message import Laborwarningmessage
def getSetQty():
    for item in Quote.Items:
        if int(item.Quantity)>1:
            CS.setBeforeEffectivedate[item.QuoteItemGuid] = item.Quantity

def setGetQty():
    for item in Quote.Items:
        if CS.setBeforeEffectivedate.get(item.QuoteItemGuid):
            item.Quantity = int(CS.setBeforeEffectivedate.get(item.QuoteItemGuid))
        if item.ProductName == 'Winest Labor Import':
            product = item.AsMainItem.EditConfiguration()
            product.ParseString('<* ExecuteScript(PS_Refresh_Labor_Containers_Data)*>')
            product.UpdateQuote()
        elif item.ProductName == 'TPC System Name':
            product = item.AsMainItem.EditConfiguration()
            product.ParseString('<* ExecuteScript(ResetProductPricing) *>')
            product.UpdateQuote()
    Quote.Save(False)

if Param.Action == 'getSet':
    getSetQty()
elif Param.Action == 'setGet':
    setGetQty()
    Laborwarningmessage(Quote)
    Quote.ExecuteAction(3202) #Trigger Reprice

ApiResponse = ApiResponseFactory.JsonResponse(True)