from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
pAccountName = None
if Quote:
	AccountName = Quote.GetCustomField('Account Name').Content
	AccountSite = Quote.GetCustomField('Account Site').Content
	#Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content = 'Exxon Parent'
	pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
# Needed to populate the sites always.
mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
mSites_Cont_sites = [row['Sites'] for row in mSites_Cont.Rows]
if mSites_Cont.Rows.Count == 0:
	mSites=class_contact_modules.get_sites(AccountName)
	if mSites:
		for site in mSites.records:
			if site.Site not in mSites_Cont_sites:
				Trace.Write('record is not present -> adding it now.')
				sRow = mSites_Cont.AddNewRow(False)
				sRow['Sites'] = str(site.Site)
				sRow['AccountId'] = str(site.Id)
				sRow['AccountName'] = str(site.Name)
Product.Attr('SC_HWOS_Service_Product_ScopeSummary').Access = AttributeAccess.ReadOnly
Product.Attr('EnabledService_Entitlement').Access = AttributeAccess.ReadOnly
Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').Access = AttributeAccess.ReadOnly
Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').Access = AttributeAccess.ReadOnly
Product.Attr('Matrix License').Access = AttributeAccess.ReadOnly
Product.Attr("DurationOfPlan_enabledServices").Access = AttributeAccess.ReadOnly
Product.Attr("CurrentSupportContract_EnabledService").Access = AttributeAccess.ReadOnly
"""if  False:
	Log.Info('----pAccountName inside sites ['+str(pAccountName)+']')
	pass
else:
	#Product.DisallowAttr('SC_SESP_MultiSites')
	#Product.DisallowAttr('SC_SESP_MultiSites_Button')
	MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont')
	Hid_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
	MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
	if Hid_Cont.Rows.Count is 0:
		for asset in MSIDTable.records:
			msid = asset.Name
			SystemName = asset.ProductCode
			Systemnum = asset.SiteLicSeqSys__c
			i = MSID_Cont.AddNewRow(False)
			hrow = Hid_Cont.AddNewRow(False)
			i['MSIDs'] = str(msid)
			i['System Name'] = str(SystemName)
			i['System Number'] = str(Systemnum)
			hrow['MSIDs'] = str(msid)
			hrow['System Name'] = str(SystemName)
			hrow['System Number'] = str(Systemnum)
	MSID_Cont.Calculate()
	Hid_Cont.Calculate()"""