import GS_ITEMCREATE_UPDATE_Functions as funct
from GS_FME_CONFIG_MOD import config2fme,getAccessToken
def Populate_FME(cartitem,prd,Quote):
	hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME(nolock) where Domain in (select tenant_name from tenant_environments(nolock) where is_current_environment = 1)")
	host = hostquery.HostName
	accessTkn = getAccessToken(host)
	qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(prd)))
	if qry is not None:
		Trace.Write(str()+'--rechecking--333-->'+str(cartitem.QI_FME.Value))
		jsonConfig = config2fme(host, accessTkn,prd)
		gtval = funct.getfmeval(jsonConfig,cartitem)
		Trace.Write(str(gtval)+'--rechecking--444-->'+str(cartitem.QI_FME.Value))
		cartitem.QI_Short_FME_Code.Value = str(Quote.GetGlobal('gv_short_fme'))
		if str(Quote.GetGlobal('Yspec_Fme')) != "":
			#item.QI_FME.Value = str(Quote.GetGlobal('Yspec_Fme'))
			funct.fn_QI_FME_Assignment(str(Quote.GetGlobal('Yspec_Fme')),cartitem)
		else:
			if gtval != "YSPEC YES":
				#item.QI_FME.Value = gtval
				funct.fn_QI_FME_Assignment(gtval,cartitem)
		#Below global parameters are set in FME Bulk Upload product script
		if str(Quote.GetGlobal('BU_Extended_Desc')) != "":
			cartitem.QI_ExtendedDescription.Value = str(Quote.GetGlobal('BU_Extended_Desc'))
			Quote.SetGlobal('BU_Extended_Desc', '')
		if str(Quote.GetGlobal('BU_ACE_Quote_Ref')) != "":
			cartitem.QI_Ace_Quote_Number.Value = str(Quote.GetGlobal('BU_ACE_Quote_Ref'))
			Quote.SetGlobal('BU_ACE_Quote_Ref', '')
		if str(Quote.GetGlobal('BU_ACE_Quote_Desc')) != "":
			cartitem.QI_Ace_Description.Value = str(Quote.GetGlobal('BU_ACE_Quote_Desc'))
			Quote.SetGlobal('BU_ACE_Quote_Desc', '')
		if str(Quote.GetGlobal('BU_ACE_Quote_Cost')) != "":
			if str(Quote.GetGlobal('BU_AdderTotalETO')) == "ETO":
				cartitem.QI_ETO_COST.Value = float(Quote.GetGlobal('BU_ACE_Quote_Cost'))
			Quote.SetGlobal('BU_ACE_Quote_Cost', '')
			cartitem.QI_REGIONAL_ETO_COST.Value = cartitem.QI_ETO_COST.Value * cartitem.Quantity
			cartitem.QI_TOTAL_COST.Value = cartitem.QI_ETO_COST.Value + cartitem.Cost
			cartitem.QI_TOTAL_EXTENDED_COST.Value = cartitem.QI_TOTAL_COST.Value * cartitem.Quantity
		if str(Quote.GetGlobal('BU_ACE_Quote_ListPrice')) != "" and str(cartitem.QI_Ace_Quote_Number.Value) != "":
			cartitem.QI_AceQuote_ListPrice.Value = float(Quote.GetGlobal('BU_ACE_Quote_ListPrice'))
			Quote.SetGlobal('BU_ACE_Quote_ListPrice', '')
		if str(Quote.GetGlobal('BU_Parent_Generic_system_GUID')) != "":
			cartitem.QI_Parent_Generic_system_GUID.Value = str(Quote.GetGlobal('BU_Parent_Generic_system_GUID'))
			Quote.SetGlobal('BU_Parent_Generic_system_GUID', '')
		if str(Quote.GetGlobal('BU_Generic_system_FME_ContRoWID')) != "":
			cartitem.QI_Generic_system_FME_ContRoWID.Value = str(Quote.GetGlobal('BU_Generic_system_FME_ContRoWID'))
			Quote.SetGlobal('BU_Generic_system_FME_ContRoWID', '')
		if str(Quote.GetGlobal('no_of_configuration')) != "":
			cartitem.QI_VCProducts.Value = str(Quote.GetGlobal('no_of_configuration'))
			Quote.SetGlobal('no_of_configuration', '')    
	else:
		if "Yspecial" in cartitem.Description:
			cartitem.QI_ParentVcModel.Value = prd.split("-")[0]
		query = "select TOP 10 STANDARD_ATTRIBUTE_NAME from FME_ATTRIBUTE_ORDER fao join ATTRIBUTE_DEFN ad on fao.Attribute = ad.SYSTEM_ID where Material = '{}' order by ATTRIBUTE_Order asc".format(cartitem.PartNumber)
		res = SqlHelper.GetList(query)

		fme = ''
		attrDict = dict()
		cartitem.QI_Short_FME_Code.Value = str(Quote.GetGlobal('gv_short_fme'))
		for attr in cartitem.SelectedAttributes:
			for value in attr.Values:
				attrDict[attr.Name]= value.Display

		for attr in res:
			fme = '{}{}'.format(fme , attrDict[attr.STANDARD_ATTRIBUTE_NAME])
		if str(Quote.GetGlobal('Yspec_Fme')) != "":
			#item.QI_FME.Value = str(Quote.GetGlobal('Yspec_Fme'))
			funct.fn_QI_FME_Assignment(str(Quote.GetGlobal('Yspec_Fme')),cartitem)
		else:
			if fme != "YSPEC YES":
				#item.QI_FME.Value = fme
				funct.fn_QI_FME_Assignment(fme,cartitem)
	Quote.SetGlobal('Yspec_Fme', '')
	Quote.SetGlobal('gv_short_fme','')