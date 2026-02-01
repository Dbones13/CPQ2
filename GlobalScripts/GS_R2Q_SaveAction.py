import GS_R2Q_FunctionalUtil

try:
    context = Param.action
except AttributeError:
    context = ""
def Deletemainitem():
    try:
        if Quote.GetCustomField("R2QFlag").Content in ('yes', 'Yes', 'YES', 'True', 'true', 'True') and Quote.GetCustomField("R2Q_Save").Content=='Save':
            for Item in Quote.MainItems:
                Item.Delete()
    except Exception as ex:
        Deletemainitem()
def save_submit():
    GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Initial", "Notification", 'Quote Submitted Successfully')
    Log.Info("sent structure to SFDC")
    return True

try:
    Deletemainitem()
    Quote.GetCustomField("R2Q_Save").Content = context if context in ["Save", "Submit"] else ""
except Exception as ex:
    msg = 'Error Occured, {"ErrorCode": "SaveConfig", "ErrorDescription": "Failed at: Mapping at CPQ"}'
    GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
    raise
#Log.Info("context--> " +str(context))
if context == "Submit" and Quote.OrderStatus.Name == "Preparing":
    try:
        ApiResponse = ApiResponseFactory.JsonResponse(save_submit())
    except Exception as ex:
        msg = 'Error Occured, {"ErrorCode": "SubmitConfig", "ErrorDescription": "Failed at: Mapping at CPQ"}'
        GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
        raise