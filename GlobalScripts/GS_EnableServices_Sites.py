from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountName = Quote.GetCustomField('Account Name').Content
mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
hidden_cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
asset_cont	= Product.GetContainerByName('Asset_details_ServiceProd')

def deleteAsset(msid):
	indexes = [row.RowIndex for row in	asset_cont.Rows if row['MSID'] == msid]
	start_index = 0
	for indx in indexes:
		asset_cont.DeleteRow(indx - start_index)
		start_index += 1

updateSites = []
removeSites = []
for row in mSites_Cont.Rows:
	if row.IsSelected:
		updateSites.append(row['Sites'])
	elif not row.IsSelected:
		removeSites.append(row['Sites'])
AccountSite = updateSites
MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont')
unchecked_indexes = []
if len(updateSites) <= 0:
	MSID_Cont.Rows.Clear()
	hidden_cont.Rows.Clear()
	asset_cont.Rows.Clear()
else:
	MSIDTable = class_contact_modules.get_site_assets(AccountName, AccountSite,isParent=True)
	MSID_CONT_NAMES = [row['MSIDs'] + '<,>' + row['siteName'] for row in hidden_cont.Rows]
	if MSIDTable:
		for asset in MSIDTable.records:
			if asset.Name.ToString() + '<,>' + asset.Account.Site.ToString()  not in MSID_CONT_NAMES:
				#row = MSID_Cont.AddNewRow(False)
				row_h = hidden_cont.AddNewRow(False)
				row_h['MSIDs'] = asset.Name.ToString()
				row_h['System Name'] = asset.ProductCode.ToString()
				row_h['System Number'] = asset.SiteLicSeqSys__c.ToString()
				row_h['siteName'] = asset.Account.Site.ToString()
				#row['MSIDs'] = asset.Name.ToString()
				#row['System Name'] = asset.ProductCode.ToString()
				#row['System Number'] = asset.SiteLicSeqSys__c.ToString()
				#row['siteName'] = asset.Account.Site.ToString()

	if removeSites > 0:
		for site in removeSites:
			unchecked_indexes = [row.RowIndex for row in  hidden_cont.Rows	if row['siteName'] == site]
			start_index = 0
			for indx in unchecked_indexes:
				hidden_cont.DeleteRow(indx - start_index)
				start_index += 1
			unchecked_indexes = [row.RowIndex for row in  MSID_Cont.Rows	if row['siteName'] == site]
			start_index = 0
			for indx in unchecked_indexes:
				newIndx = indx - start_index
				r = MSID_Cont.Rows[newIndx]
				msid = r['MSIDs']
				MSID_Cont.DeleteRow(newIndx)
				deleteAsset(msid)
				start_index += 1

def addRowToMSIDCONT(i):
	row = MSID_Cont.AddNewRow(False)
	row['MSIDs'] = i['MSIDs']
	row['System Name'] = i['System Name']
	row['System Number'] = i['System Number']
	row['siteName'] = i['siteName']

searchBox = Product.Attr('EnabledsearchBox').GetValue()
if searchBox == '':
	for i in hidden_cont.Rows:
		isRowExsists = [row['MSIDs'] for row in MSID_Cont.Rows if row['MSIDs'] == i['MSIDs'] and row['siteName'] == i['siteName']]
		if	not len(isRowExsists) > 0: #this is for not adding duplicate rows from hidden cont
			addRowToMSIDCONT(i)
else:
	for i in hidden_cont.Rows:
		isRowExsists = [row.RowIndex for row in MSID_Cont.Rows if row['MSIDs'] == i['MSIDs'] and row['siteName'] == i['siteName']]
		if searchBox in i['MSIDs'] and not len(isRowExsists) > 0 :
			addRowToMSIDCONT(i)
		elif searchBox	not in i['MSIDs'] and  len(isRowExsists) > 0:
			newIndx = isRowExsists[0]
			r = MSID_Cont.Rows[newIndx]
			msid = r['MSIDs']
			MSID_Cont.DeleteRow(newIndx)
			deleteAsset(msid)
asset_cont.Calculate()