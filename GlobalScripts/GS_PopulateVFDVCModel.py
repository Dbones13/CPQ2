for item in Quote.MainItems:
    vfdquery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.PartNumber))
    if vfdquery is not None:
        def populateQuoteTableRow(table , dataDict , row = None):
            if not row:
                row = table.AddNewRow()
            for key , value in dataDict.items():
                row[key] = value

        def populateSimple(VFDVCTable , item,areaflag):
            rowDict = {
                'CartItemGUID' : item.QuoteItemGuid,
                'ItemNumber' : item.RolledUpQuoteItem ,
                'PartNumber' : item.PartNumber,
                'ProductName' : item.ProductName,
                'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName),
                'Area': areaflag
            }
            populateQuoteTableRow(VFDVCTable , rowDict)

        def getfmeval(VFDVCTable,item,areaflag):
            populateSimple(VFDVCTable , item,areaflag)
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
                'AttributeDescription': item.QI_FME.Value,
                'Area': areaflag
            }
            populateQuoteTableRow(VFDVCTable , rowDict_conf)

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
                            'AttributeDescription': "[{}] - {}".format(value.ValueCode , value.Display ),
                            'Area': areaflag
                            }
                            #Log.Write("rowDict---->"+str(rowDict))
                            populateQuoteTableRow(VFDVCTable , rowDict)

        VFDVCTable = Quote.QuoteTables["VFD_VC_Model_Configuration"]
        if VFDVCTable.Rows.Count > 0:
            VFDVCTable.Rows.Clear()
        area = []
        project = ""
        for item in Quote.MainItems:
            if item.PartNumber == 'PRJT':
                project = item
                break
        if project != "":
            for sys_group in project.Children:
                for system in sys_group.Children:
                    if system.ProductName in ['Variable Frequency Drive System']:
                        area.append(system.QI_Area.Value)
        for item in Quote.MainItems:
            vfdvcquery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.PartNumber))
            if vfdvcquery is not None:
                if item.QI_Area.Value in area:
                    areaflag = "True"
                else:
                    areaflag = "False"
                getfmeval(VFDVCTable,item,areaflag)
        VFDVCTable.Save()
        break
    else:
        VFDVCTable = Quote.QuoteTables["VFD_VC_Model_Configuration"]
        if VFDVCTable.Rows.Count > 0:
            VFDVCTable.Rows.Clear()