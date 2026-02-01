Connected_Level = 0
LPM_Level = 0
Connected_Site = Product.Attr('CBM_Connected_Site').GetValue()
LPM = Product.Attr('CBM_Local_Preventive_Maintenance').GetValue()
if Connected_Site == "" or Connected_Site == "No":
    Connected_Level = 0
elif Connected_Site == "Yes":
    Connected_Level = 1
if LPM == "" or LPM == "No":
    LPM_Level = 0
elif LPM == "Yes":
    LPM_Level = 2
Product.Attr('CBM_Level').AssignValue(str(1 + Connected_Level + LPM_Level))
################################ PM LEVEL AND DESCRIPTION ################
level = Product.Attr('CBM_Level').GetValue()
get_PMLevel_PMDescription = SqlHelper.GetFirst("select PM_Strategy,PM_Description from SC_CT_PM_STRATEGY where Level = '"+level+"'")
if get_PMLevel_PMDescription:
    Product.Attr('CBM_PM_Description').AssignValue(get_PMLevel_PMDescription.PM_Description.ToString())
    Product.Attr('CBM_PM_Level').AssignValue(get_PMLevel_PMDescription.PM_Strategy.ToString())
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")
ScriptExecutor.Execute('PS_Refresh_PricingContainer')