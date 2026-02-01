#Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'false'

# HCP Lob to update WTW Cost on FME parts.
if Quote.GetCustomField("Booking LOB").Content == "HCP":
    for item in Quote.MainItems:
        wtw = SqlHelper.GetFirst("SELECT WTW_FACTOR from HPS_PLSG_WTW_FACTOR where PL_PLSG = '"+str(item.QI_PLSG.Value).strip()+"' ")
        fme = SqlHelper.GetFirst("SELECT *from FME_PARTS where PARTNUMBER='"+str(item.PartNumber)+"' ")
        if fme and item["QI_PLSG"].Value and wtw and item.Cost:
            UnitWTWCost = item.Cost/(1+float(wtw.WTW_FACTOR)) # ExtendedCost
            item.QI_UnitWTWCost.Value = UnitWTWCost
            item.QI_ExtendedWTWCost.Value = item.Quantity * UnitWTWCost

Quote.Calculate(12) #Refer 12 in PROD #14 in QA