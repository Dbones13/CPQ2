import GS_R2QCalculation_Module as r2q_calc
import GS_FME_CONFIG_MOD
pn = SqlHelper.GetFirst("Select PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK) where PLANT_CODE = '6649' ORDER BY CpqTableEntryId DESC")
if pn:
    Quote.GetCustomField("CF_Plant").Content = str(pn.PLANT_NAME)
if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
	Quote.GetCustomField("SellPricestrategy").Content = Product.Attr('Sell Price Strategy').SelectedValue.Display
	Quote.GetCustomField("CustomerBudget").Content = Product.Attr('Customer_Budget_TextField').GetValue()
Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content = Product.Attr('AR_HCI_Proposal Language').GetValue()
def assignval(resp,prod):
	for atnm in list(resp):
		a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
		if a == "DropDown":
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
		else:
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
	prod.ApplyRules()
	return prod.IsComplete,prod.TotalPrice

if (Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Quote.GetCustomField('R2Q_Save').Content == 'Submit') or Quote.GetCustomField('R2QFlag').Content!= 'Yes' or (Quote.GetCustomField('R2QFlag').Content == 'Yes' and Quote.GetCustomField('IsR2QRequest').Content!= 'Yes'):
	edm = Product.GetContainerByName('AR_HCI_SUBPRD').Rows[0]
	hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	host = hostquery.HostName
	accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
	HCI_PHD_PartSummary_Cont = edm.Product.GetContainerByName("HCI_PHD_PartSummary_Cont")
	invalidFME = []
	#Log.Info("---HCI_PHD_PartSummary_Cont---111--"+str(FME_Valid_Parts.Rows.Count)+"--HCI_PHD_PartSummary_Cont-->"+str(HCI_PHD_PartSummary_Cont.Rows.Count))
	if HCI_PHD_PartSummary_Cont.Rows.Count>0:
		index = 0
		#Session["prevent_execution"] = "true"
		part_lst = "'" + ("','".join([str(prow["PartNumber"]) for prow in HCI_PHD_PartSummary_Cont.Rows if prow["fme"]])) + "'"
		qry =("SELECT product_catalog_code,product_ID,version_number from (SELECT p.product_catalog_code, p.product_ID, pv.version_number, ROW_NUMBER() OVER ( PARTITION BY p.product_catalog_code ORDER BY pv.SAPEffectiveDate DESC, pv.version_number DESC ) AS rn FROM products p LEFT OUTER JOIN product_versions pv ON p.product_id = pv.product_id WHERE p.product_catalog_code IN ({}) AND p.PRODUCT_ACTIVE = 1 AND pv.is_active = 1) RankedProducts WHERE rn = 1".format(str(part_lst)))
		getprdid= SqlHelper.GetList(qry)
		prd_dict = {prd.product_catalog_code: prd.product_ID for prd in getprdid }

		for prow in HCI_PHD_PartSummary_Cont.Rows:
			if prow["fme"]:
				#Log.Info(str(prow["PartNumber"])+"---HCI_PHD_PartSummary_Cont---222--"+str(prd_dict))
				index += 1
				try:
					product_id = prd_dict[prow["PartNumber"]]
					#Log.Info(str(prow["PartNumber"])+"---HCI_PHD_PartSummary_Cont---333--"+str(product_id))
					prod = ProductHelper.CreateProduct(int(product_id))
					#prod.AddToQuote(int(0))
					if not prod.IsComplete:
						jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(prow["PartNumber"]),str(prow["fme"]))
						assignpart,assigntot = assignval(jsonConfig,prod)
					if prod.IsComplete:
						prod.AddToQuote(int(prow["Quantity"]))
				except Exception as e:
					Log.Info("-HCI_PHD_PartSummary_Cont--Error in CPS Connection and moved to invalid parts "+str(prow['PartNumber'])+" : "+ str(e))
Quote.GetCustomField("CF_R2Q_RefreshCart").Content = "Yes"
#Quote.GetCustomField("CF_Plant").Content = str(pn.PLANT_NAME)
#for i in Quote.MainItems:
#	i['QI_Plant'].Value = str(pn.PLANT_NAME)
#Quote.Calculate(14)
#Quote.ExecuteAction(3225)
#if Quote.GetCustomField('R2QFlag').Content == 'Yes':
from GS_SetDefaultPricePlan import setDefaultMpa
setDefaultMpa(Quote,TagParserQuote)
Quote.Save(False)