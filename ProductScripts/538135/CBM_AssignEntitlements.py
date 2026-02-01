################################## Insert Entitlements ####################################
Product.Attr('CBM_Service_Product').Access = AttributeAccess.ReadOnly
Product.Attr('CBM_PM_Level').Access = AttributeAccess.ReadOnly
Product.Attr('CBM_PM_Description').Access = AttributeAccess.ReadOnly
#######
entList = SqlHelper.GetList("Select Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = 'Condition Based Maintenance'")
if entList:
    for ent in entList:
        CBM_EntCont = Product.GetContainerByName('CBM_Entitlements_Cont')
        Ent_Row = CBM_EntCont.AddNewRow(False)
        Ent_Row["Entitlement"] = ent.Entitlement
        if ent.IsMandatory.ToString() == 'TRUE':
        	Ent_Row.IsSelected = True
        elif ent.IsMandatory.ToString() == 'FALSE':
            Ent_Row.IsSelected = False
################################## Level Settings ##########################################
level = Product.Attr('CBM_Level').GetValue()
get_PMLevel_PMDescription = SqlHelper.GetFirst("select PM_Strategy,PM_Description from SC_CT_PM_STRATEGY where Level = '"+level+"'")
if get_PMLevel_PMDescription:
    Product.Attr('CBM_PM_Description').AssignValue(get_PMLevel_PMDescription.PM_Description.ToString())
    Product.Attr('CBM_PM_Level').AssignValue(get_PMLevel_PMDescription.PM_Strategy.ToString())
if Quote:
	currency = Quote.SelectedMarket.CurrencyCode
else:
	currency = 'USD'
Product.Attr('SC_Quote_Currency').AssignValue(currency)