#In the Productized Skid,  VC items are added as a child item. This script used to insert SKID VC Item attribute information to VCModelConfiguration quote table. This script should execute after GS_Skid_VC_Items script. CXCPQ-47391
# Added If condition to improve the 
for item in Quote.Items:
	Trace.Write(str()+"-----QI_FME-----recheck---333---"+str(item.QI_FME.Value))
	if Quote.GetCustomField('Booking LOB').Content == "PMC" and  item.ProductName=='Productized Skid Quote Item' and item.QI_FME.Value!='':

		import GS_FME_CONFIG_MOD
		
		def assignval(resp,prod):
			Trace.Write(str(resp))
			for atnm in list(resp):
				Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
				a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
				if a == "DropDown":
					prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
				elif a == "Free Input, no Matching":
					prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
				else:
					prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
					Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
			prod.ApplyRules()
			return prod.IsComplete,prod.TotalPrice
		
		def deleteRows(table , ids):
			for id in ids:
				table.DeleteRow(id)
		
		def populateQuoteTableRow(table , dataDict , row = None):
			if not row:
				row = table.AddNewRow()
			for key , value in dataDict.items():
				row[key] = value
		
		def populateSimple(VCModelConfiguration , item):
			rowDict = {
				'CartItemGUID' : item.QuoteItemGuid,
				'ItemNumber' : item.RolledUpQuoteItem ,
				'PartNumber' : item.PartNumber,
				'ProductName' : item.ProductName,
				'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName)
			}
			populateQuoteTableRow(VCModelConfiguration , rowDict)
		
		def populateIdentificationRow(item,prod):
			rowDict = {
				'CartItemGUID' : item.QuoteItemGuid,
				'ItemNumber' : item.RolledUpQuoteItem,
				'PartNumber' : prod.PartNumber,
				'ProductName' : prod.Name,
				'ProductDescription' : "{} {}".format(prod.PartNumber , prod.Name),
				'AttributeSystemId' : '',
				'AttributeName': "Configured Model No",
				'AttributeValueSystemId': '',
				'AttributeValueCode': '',
				'AttributeValue': item.QI_FME.Value,
				'AttributeDescription': item.QI_FME.Value
			}
			populateQuoteTableRow(VCModelConfiguration , rowDict)
		
		def populateVC(VCModelConfiguration , item):
			populateSimple(VCModelConfiguration , item)
			lv_partnumber=item.PartNumber
			lv_fme = item.QI_FME.Value
			hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME(nolock) where Domain in (select tenant_name from tenant_environments(nolock) where is_current_environment = 1)")
			host = hostquery.HostName
			getprdid = SqlHelper.GetFirst("SELECT top 1 p.product_ID,p.PRODUCT_NAME from products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id where p.IsSyncedFromBackOffice = 'True' and p.IsSimple = 'False' and p.product_catalog_code= '{}' and p.PRODUCT_ACTIVE = 1 and pv.is_active = 1 order by pv.SAPEffectiveDate desc, pv.version_number desc".format(str(lv_partnumber)))
			if getprdid is not None and lv_fme!='':
				try:
					accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
					prod = ProductHelper.CreateProduct(int(getprdid.product_ID))
					jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(lv_partnumber),str(lv_fme))
					assignpart,assigntot = assignval(jsonConfig,prod)
					populateIdentificationRow(item,prod)
				except Exception as e:
					Trace.Write('Error while genearing product attributes based on FME')
				lv_ignored_attribues=[]
				for attr in filter(lambda x:'POS'  in x.SystemId or 'CV'  in x.SystemId or 'KEY'  in x.SystemId, prod.Attributes):
					lv_ignored_attribues.append(attr.Name)
				
				for attr in prod.Attributes:
					if attr.Name not in lv_ignored_attribues:
						Trace.Write('attr.Name'+ str(attr.Name))
						for value in attr.SelectedValues:
							valueCode = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
							#valueCode = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
							valueSystemId = attr.SelectedValue.SystemId if attr.SelectedValue else ""
							rowDict = {
								'CartItemGUID' : item.QuoteItemGuid,
								'ItemNumber' : item.RolledUpQuoteItem,
								'PartNumber' : prod.PartNumber,
								'ProductName' : prod.Name,
								'ProductDescription' : "{} {}".format(prod.PartNumber , prod.Name),
								'AttributeSystemId' : attr.SystemId,
								'AttributeName': attr.Name,
								'AttributeValueSystemId': valueSystemId,
								'AttributeValueCode': valueCode,
								'AttributeValue': attr.GetValue(),
								'AttributeDescription': "[{}] - {}".format(valueCode , attr.GetValue() ),
							}
							populateQuoteTableRow(VCModelConfiguration , rowDict)


		VCModelConfiguration = Quote.QuoteTables["VCModelConfiguration"]
		guId = item.QuoteItemGuid
		toBeDeleted = [ row.Id for row in VCModelConfiguration.Rows]
		#for row in VCModelConfiguration.Rows:
		#	if row['CartItemGUID'] == guId:
		#		toBeDeleted.append(row.Id)
		deleteRows(VCModelConfiguration , toBeDeleted)
		populateVC(VCModelConfiguration , item)
			
		VCModelConfiguration.Save()