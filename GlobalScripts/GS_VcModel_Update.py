#CXCPQ-66140 : Added VC check condition
#CXCPQ-78758: Added Quote Type condition to improve the performance for Service contracts.
def VcModelupdate(Quote,item):
    
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
            #'Area': 'False', #CXCPQ-66140: Added Area column
            'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName)
        }
        populateQuoteTableRow(VCModelConfiguration , rowDict)

	
    def getfmeval(VCModelConfiguration,item,Quote):
		populateSimple(VCModelConfiguration , item)
		rowDict_conf = {
			'CartItemGUID' : item.QuoteItemGuid,
			'ItemNumber' : item.RolledUpQuoteItem,
			'PartNumber' : item.PartNumber,
			'ProductName' : item.ProductName,
			'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
			'AttributeSystemId' : '',
			'AttributeName': 'Configured Model No',
			'AttributeValueSystemId': '',
			'AttributeValueCode': '',
			'AttributeValue': item.QI_FME.Value,
			#'Area': 'False', #CXCPQ-66140: Added Area column
			'AttributeDescription': item.QI_FME.Value,
		}
		populateQuoteTableRow(VCModelConfiguration , rowDict_conf)

		fmeval = ""
		#for attnm in list(resp):

		for attr in item.SelectedAttributes: 
			#Trace.Write("attr--->"+attr.Name)
			getprdid = SqlHelper.GetFirst("SELECT PRODUCT_ID,PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}' AND PRODUCT_ACTIVE = 'True'".format(str(item.PartNumber)))
			#Log.Info("atrr---->{}--prdid---{}".format(attr.Name,str(getprdid.PRODUCT_ID)))
			getsyid = SqlHelper.GetFirst("SELECT SYSTEM_ID FROM ATTRIBUTE_DEFN A JOIN PRODUCT_ATTRIBUTES B ON A.STANDARD_ATTRIBUTE_CODE = B.STANDARD_ATTRIBUTE_CODE WHERE A.STANDARD_ATTRIBUTE_NAME = '{}' AND B.PRODUCT_ID = '{}'".format(attr.Name,str(getprdid.PRODUCT_ID)))
			if getsyid is not None:

				for value in attr.Values:

					if str(value.ValueCode) != "DefaultValue" and attr.Name != "Special Options?":
						rowDict = {
						'CartItemGUID' : item.QuoteItemGuid,
						'ItemNumber' : item.RolledUpQuoteItem,
						'PartNumber' : item.PartNumber,
						'ProductName' : getprdid.PRODUCT_NAME,
						'ProductDescription' : "{} {}".format(item.PartNumber , getprdid.PRODUCT_NAME),
						'AttributeSystemId' : getsyid.SYSTEM_ID,
						'AttributeName': attr.Name,
						'AttributeValueSystemId': str(getsyid.SYSTEM_ID)+"_"+str(value.ValueCode),
						'AttributeValueCode': value.ValueCode,
						'AttributeValue': value.Display,
						#'Area': 'False', #CXCPQ-66140: Added Area column
						'AttributeDescription': "[{}] - {}".format(value.ValueCode , value.Display ),
						}
						#Log.Write("rowDict---->"+str(rowDict))
						populateQuoteTableRow(VCModelConfiguration , rowDict)

		if item.QI_Ace_Quote_Number.Value != "":
			rowDict1_conf = {
				'CartItemGUID' : item.QuoteItemGuid,
				'ItemNumber' : item.RolledUpQuoteItem,
				'PartNumber' : item.PartNumber,
				'ProductName' : item.ProductName,
				'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
				'AttributeSystemId' : '',
				'AttributeName': 'Ace Quote Number',
				'AttributeValueSystemId':item.QI_Ace_Quote_Number.Value,
				'AttributeValueCode': item.QI_Ace_Quote_Number.Value,
				'AttributeValue': item.QI_FME.Value,
				#'Area': 'False', #CXCPQ-66140: Added Area column
				'AttributeDescription': item.QI_Ace_Quote_Number.Value,
			}
			populateQuoteTableRow(VCModelConfiguration , rowDict1_conf)
			rowDict2_conf = {
				'CartItemGUID' : item.QuoteItemGuid,
				'ItemNumber' : item.RolledUpQuoteItem,
				'PartNumber' : item.PartNumber,
				'ProductName' : item.ProductName,
				'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
				'AttributeSystemId' : '',
				'AttributeName': 'Ace Description',
				'AttributeValueSystemId': item.QI_Ace_Description.Value,
				'AttributeValueCode': item.QI_Ace_Description.Value,
				'AttributeValue': item.QI_FME.Value,
				#'Area': 'False', #CXCPQ-66140: Added Area column
				'AttributeDescription': item.QI_Ace_Description.Value,
			}
			populateQuoteTableRow(VCModelConfiguration , rowDict2_conf)
		Yspecial_Selection = Quote.QuoteTables["Yspecial_Selection"]
		if Yspecial_Selection.Rows.Count > 0:
			for row in Yspecial_Selection.Rows:
				if row['MainPart'] == item.PartNumber and row['CartItemGUID'] == item.QuoteItemGuid:
					rowDict_yspec = {
						'CartItemGUID' : item.QuoteItemGuid,
						'ItemNumber' : item.RolledUpQuoteItem,
						'PartNumber' : item.PartNumber,
						'ProductName' : item.ProductName,
						'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
						'AttributeSystemId' : '',
						'AttributeName': row['Yspecial_Quote'],
						'AttributeValueSystemId':  row['Yspecial_Quote'],
						'AttributeValueCode':  row['Yspecial_Quote'],
						'AttributeValue':  row['Yspecial_Quote'],
						#'Area': 'False', #CXCPQ-66140: Added Area column
						'AttributeDescription':  row['Y_Description'],
					}
					populateQuoteTableRow(VCModelConfiguration , rowDict_yspec)
		PMC_ETO_Selection = Quote.QuoteTables["PMC_ETO_Selection"]
		if PMC_ETO_Selection.Rows.Count > 0:
			for row in PMC_ETO_Selection.Rows:
				if row['PartNumber'] == item.PartNumber and row['CartItemGUID'] == item.QuoteItemGuid:
					Trace.Write("partnumber---->"+row['Partnumber'])
					Trace.Write("etorefno---->"+row['ETO_Ref_No'])
					rowDict_eto = {
						'CartItemGUID' : item.QuoteItemGuid,
						'ItemNumber' : item.RolledUpQuoteItem,
						'PartNumber' : item.PartNumber,
						'ProductName' : item.ProductName,
						'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
						'AttributeSystemId' : '',
						'AttributeName': row['ETO_Ref_No'],
						'AttributeValueSystemId':  row['ETO_Ref_No'],
						'AttributeValueCode':  row['ETO_Ref_No'],
						'AttributeValue':  row['ETO_Ref_No'],
						#'Area': 'False', #CXCPQ-66140: Added Area column
						'AttributeDescription':  row['ETO_Proposal_Notes'],
					}
					populateQuoteTableRow(VCModelConfiguration , rowDict_eto)
		#CXCPQ-53124: Commented as Marine Yspecial and GAS ETO merged into a common quote table
		''''PMC_Marine = Quote.QuoteTables["PMC_Marine_Yspecial_Selection"]
		Trace.Write("Marine Working")
		Trace.Write("CountofRows------>"+ str(PMC_Marine.Rows.Count))
		if PMC_Marine.Rows.Count > 0:
			for row in PMC_Marine.Rows:
				if row['PartNumber'] == item.PartNumber and row['CartItemGUID'] == item.QuoteItemGuid:
					Trace.Write("refno---->"+row['Y_special_reference_no'])
					rowDict_marine = {
						'CartItemGUID' : item.QuoteItemGuid,
						'ItemNumber' : item.RolledUpQuoteItem,
						'PartNumber' : item.PartNumber,
						'ProductName' : item.ProductName,
						'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
						'AttributeSystemId' : '',
						'AttributeName': row['Y_special_reference_no'],
						'AttributeValueSystemId':  row['Y_special_reference_no'],
						'AttributeValueCode':  row['Y_special_reference_no'],
						'AttributeValue':  row['Y_special_reference_no'],
						'AttributeDescription':  row['Y_special_proposal_notes'],
					}
					populateQuoteTableRow(VCModelConfiguration , rowDict_marine)'''

    '''def populateVC(VCModelConfiguration , item):
        populateSimple(VCModelConfiguration , item)

        identificationCodeAttrName = getIdentificationCodeAttrName()

        if identificationCodeAttrName is None:
            return

        identificationAttr = Product.Attr(identificationCodeAttrName)
        populateIdentificationRow(identificationAttr , item)

        identificationCode = item.QI_FME.Value

        if "Table" in identificationCodeAttrName:
            identificationCode = identificationCode.replace('-','')

        temp = "{} ".format(identificationCode)

        for attr in filter(lambda x:'POS' in x.SystemId or 'CV' in x.SystemId or 'KEY' in x.SystemId, Product.Attributes):
            if temp == " ":
                break
            valueCode = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
            valueSystemId = attr.SelectedValue.SystemId if attr.SelectedValue else ""
            if temp.startswith(valueCode):
                temp = "{}".format(temp[len(valueCode):])
                rowDict = {
                    'CartItemGUID' : item.QuoteItemGuid,
                    'ItemNumber' : item.RolledUpQuoteItem,
                    'PartNumber' : Product.PartNumber,
                    'ProductName' : Product.Name,
                    'ProductDescription' : "{} {}".format(Product.PartNumber , Product.Name),
                    'AttributeSystemId' : attr.SystemId,
                    'AttributeName': attr.Name,
                    'AttributeValueSystemId': valueSystemId,
                    'AttributeValueCode': valueCode,
                    'AttributeValue': attr.GetValue(),
                    'Area': 'False', #CXCPQ-66140: Added Area column
                    'AttributeDescription': "[{}] - {}".format(valueCode , attr.GetValue() ),
                }
                populateQuoteTableRow(VCModelConfiguration , rowDict)'''


    VCModelConfiguration = Quote.QuoteTables["VCModelConfiguration"]
    #VCModelConfiguration.Rows.Clear()
    guId = item.QuoteItemGuid

    toBeDeleted = list()
    for row in VCModelConfiguration.Rows:
        if row['CartItemGUID'] == guId:
            toBeDeleted.append(row.Id)
    #Trace.Write("delete----->"+str(toBeDeleted[0]))
    getfmeval(VCModelConfiguration,item,Quote)


    deleteRows(VCModelConfiguration , toBeDeleted)
    VCModelConfiguration.Save()