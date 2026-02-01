import re
def BuildContainerxml(Item, quote):
    Partscont=Item.SelectedAttributes.GetContainerByName('TPC_PartsContainer')
    ContainerItemsxml=''
    qDiscDist = {}
    for item in quote.MainItems:
        qDiscDist[item.QI_PLSG.Value + '<*>' + ('None' if not item.QI_Year.Value else item.QI_Year.Value) + '<*>' + str(item.QI_No_Discount_Allowed.Value)] = {'QI_Additional_Discount_Percent': item.QI_Additional_Discount_Percent.Value, 'QI_Additional_Discount_Amount':item.QI_Additional_Discount_Amount.Value, 'QI_MPA_Discount_Percent': item.QI_MPA_Discount_Percent.Value, 'QI_MPA_Discount_Amount':item.QI_MPA_Discount_Amount.Value, 'ExtendedAmount': item.ExtendedAmount}
    for row1 in Partscont.Rows:
        row = {col.Name: str(row1[col.Name].encode("ascii", "replace").replace('?','')) for col in row1.Columns}
        if qDiscDist.get(row['QI_PLSG'] + '<*>' + row['QI_Year'] + '<*>' + row['QI_No_Discount_Allowed'], '') != '':
            changeFlag = 0
            if float(qDiscDist[row['QI_PLSG'] + '<*>' + row['QI_Year'] + '<*>' + row['QI_No_Discount_Allowed']]['QI_MPA_Discount_Percent']) != float(row['QI_MPA_Discount_Percent']):
                row['QI_MPA_Discount_Percent'] = str(float(qDiscDist[row['QI_PLSG'] + '<*>' + row['QI_Year'] + '<*>' + row['QI_No_Discount_Allowed']]['QI_MPA_Discount_Percent']))
                row['QI_MPA_Discount_Amount'] = str(float(row['ExtendedListPrice']) * float(row['QI_MPA_Discount_Percent']) / 100) if row['QI_MPA_Discount_Percent'] else  '0'
                changeFlag = 1
            if float(qDiscDist[row['QI_PLSG'] + '<*>' + row['QI_Year'] + '<*>' + row['QI_No_Discount_Allowed']]['QI_Additional_Discount_Percent']) != float(row['QI_Additional_Discount_Percent']):
                row['QI_Additional_Discount_Percent'] = str(float(qDiscDist[row['QI_PLSG'] + '<*>' + row['QI_Year'] + '<*>' + row['QI_No_Discount_Allowed']]['QI_Additional_Discount_Percent']))
                row["QI_Additional_Discount_Amount"] = str((float(row["ExtendedListPrice"]) - float(row["QI_MPA_Discount_Amount"])) * float(row["QI_Additional_Discount_Percent"]) / 100)
                changeFlag = 1
            if changeFlag:
                row["ExtendedAmount"] = str(float(row["ExtendedListPrice"]) - float(row["QI_Additional_Discount_Amount"]) - float(row['QI_MPA_Discount_Amount']))
                row["QI_UnitSellPrice"] = str((float(row["ExtendedAmount"]) / int(row["Quantity"])) if row["Quantity"] not in ['0', '', None] else 0)
                row["QI_RegionalMargin"] = str(float(row["ExtendedAmount"]) - float(row["ExtendedCost"]))
                row["QI_RegionalMarginPercent"] = str(float(row["QI_RegionalMargin"])/float(row["ExtendedAmount"]) * 100) if float(row["ExtendedAmount"]) != 0 else '0'
                row["QI_WTWMargin"] = str(float(row["ExtendedListPrice"]) - float(row["QI_ExtendedWTWCost"]))
                row["QI_WTWMarginPercent"] = str(float(row["QI_WTWMargin"])/float(row["ExtendedListPrice"]) * 100) if float(row["ExtendedListPrice"]) != 0 else '0'

        rowxml='<MainItem CanOverrideMinMaxValues="1"><Id><![CDATA['+str(row1.UniqueIdentifier)+'-'+str(quote.RevisionNumber)+']]></Id><Rank><![CDATA['+str(int((row1.RowIndex)+1))+']]></Rank><RolledUpCartItem><![CDATA['+str(Item.RolledUpQuoteItem)+'.'+str(int((row1.RowIndex)+1))+']]></RolledUpCartItem><ParentItem><![CDATA['+str(Item.RolledUpQuoteItem)+']]></ParentItem>'
        qty=row['Quantity'] if row['Quantity'] else '1'
        rowxml+='<Quantity Editable="0" EditableGroup="0"><![CDATA['+str(qty)+']]></Quantity>'
        rowxml+='<CartItemGuid><![CDATA[---]]></CartItemGuid>'
        rowxml+='<PartNumber Editable="0" EditableGroup="0"><![CDATA['+str(row['PartNumber'])+']]></PartNumber>'
        rowxml+='<UnitOfMeasure><![CDATA['+str(row['QI_UoM'])+']]></UnitOfMeasure>'
        rowxml+='<Cost Editable="0" EditableGroup="0"><![CDATA['+str(row['Cost'])+']]></Cost>'
        rowxml+='<ExtendedCost Editable="0" EditableGroup="0"><![CDATA['+str(row['ExtendedCost'])+']]></ExtendedCost>'
        rowxml+='<ListPrice Editable="0" EditableGroup="0"><![CDATA['+str(row['ListPrice'])+']]></ListPrice>'
        rowxml+='<ExtendedListPrice Editable="0" EditableGroup="0"><![CDATA['+str(row['ExtendedListPrice'])+']]></ExtendedListPrice>'
        rowxml+='<NetPrice Editable="0" EditableGroup="0"><![CDATA['+str(row['QI_UnitSellPrice'])+']]></NetPrice>'
        rowxml+='<ExtendedAmount Editable="0" EditableGroup="0"><![CDATA['+str(row['ExtendedAmount'])+']]></ExtendedAmount>'
        rowxml+='<ProductName Editable="0" EditableGroup="0"><![CDATA['+str(row['ProductName'].encode("ascii", "replace").replace('?','')).strip()+']]></ProductName>'
        rowxml+='<Description Editable="0" EditableGroup="0"><![CDATA['+str(row['QI_ExtendedDescription']).encode('unicode_escape')+']]></Description>'
        rowxml+='<QI_WTWMargin Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_WTWMargin'])+'" CustomFieldDataType="Currency" IsOverridden="0" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_WTWMargin'])+']]></QI_WTWMargin>'
        rowxml+='<QI_WTWMarginPercent Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_WTWMarginPercent'])+'" CustomFieldDataType="Number" IsOverridden="0" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_WTWMarginPercent'])+']]></QI_WTWMarginPercent>'
        rowxml+='<QI_MPA_Discount_Percent Editable="0" EditableGroup="0" DisplaySummary="1" CalculatedValue="'+str(row['QI_MPA_Discount_Percent'])+'" CustomFieldDataType="Number" IsOverridden="1" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_MPA_Discount_Percent'])+']]></QI_MPA_Discount_Percent>'
        rowxml+='<QI_Target_Sell_Price Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="0" CustomFieldDataType="Currency" IsOverridden="1" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA[0]]></QI_Target_Sell_Price>'
        rowxml+='<QI_MPA_Discount_Amount Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_MPA_Discount_Amount'])+'" CustomFieldDataType="Number" IsOverridden="0" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_MPA_Discount_Amount'])+']]></QI_MPA_Discount_Amount>'
        rowxml+='<QI_UnitWTWCost Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_UnitWTWCost'])+'" CustomFieldDataType="Currency" IsOverridden="1" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_UnitWTWCost'])+']]></QI_UnitWTWCost>'
        rowxml+='<QI_ExtendedWTWCost Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_ExtendedWTWCost'])+'" CustomFieldDataType="Currency" IsOverridden="1" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_ExtendedWTWCost'])+']]></QI_ExtendedWTWCost>'
        rowxml+='<QI_RegionalMarginPercent Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_RegionalMarginPercent'])+'" CustomFieldDataType="Number" IsOverridden="1" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_RegionalMarginPercent'])+']]></QI_RegionalMarginPercent>'
        rowxml+='<QI_RegionalMargin Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValue="'+str(row['QI_RegionalMargin'])+'" CustomFieldDataType="Currency" IsOverridden="1" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_RegionalMargin'])+']]></QI_RegionalMargin>'
        rowxml+='<QI_Additional_Discount_Percent Editable="0" EditableGroup="0" DisplaySummary="1" CalculatedValue="'+str(row['QI_Additional_Discount_Percent'])+'" CustomFieldDataType="Number" IsOverridden="0" IsCalculatedSuccessfully="1" IsCustomField="1"><![CDATA['+str(row['QI_Additional_Discount_Percent'])+']]></QI_Additional_Discount_Percent>'
        rowxml+='<QI_ProductCostCategory Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValueString="" CustomFieldDataType="Text" IsOverridden="0" IsCalculatedSuccessfully="1" CharacterLimit="0" IsCustomField="1"><![CDATA['+str(row['QI_ProductCostCategory'])+']]></QI_ProductCostCategory>'
        rowxml+='<QI_ProjectType Editable="0" EditableGroup="0" DisplaySummary="0" CalculatedValueString="" CustomFieldDataType="Text" IsOverridden="0" IsCalculatedSuccessfully="1" CharacterLimit="0" IsCustomField="1"><![CDATA['+str(row['QI_ProjectType'])+']]></QI_ProjectType>'
        ContainerItemsxml += rowxml + '</MainItem>'
    return ContainerItemsxml

Log.Info('GetQuoteData Param-->>'+str(JsonHelper.Serialize(Param)))
try:
    QuoteNumber = Param.cartCompositeNumber
    username = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='CPI_USERNAME'").Value
    password = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='CPI_PASSWORD'").Value
    import System.Net
    webclient=System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.ContentType]="application/soap+xml"
    xml_payload = """<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
            <GetQuoteData xmlns="http://webcominc.com/">
                <username>{}#HONEYWELLINTERNATIONAL_PRD</username>
                <password>{}</password>
                <cartCompositeNumber>{}</cartCompositeNumber>
            </GetQuoteData>
        </soap12:Body>
    </soap12:Envelope>""".format(username, password, QuoteNumber)
    response = webclient.UploadString('https://honeywellinternational.cpq.cloud.sap/wsAPI/CPQAPI.asmx', xml_payload)
    if "&lt;Status&gt;NOK&lt;/Status&gt;" not in response:
        doc=XmlHelper.Load(response)
        new_content = ""

        def processQuoteData(qXmlString):
            xmlItems = {}
            xmlData = ''
            eQuote=QuoteHelper.Edit(QuoteNumber)
            for item in eQuote.RootSystemMainItems:
                if item.ProductName == 'TPC System Name':
                    xmlItems[item.QuoteItemGuid] = BuildContainerxml(item,eQuote)
            xmlMainItems = XmlHelper.Load(qXmlString).SelectSingleNode('//MainItems')
            for child in xmlMainItems.ChildNodes:
                ParentItemGuid = child.SelectSingleNode('ParentItemGuid')
                CartItemGuid = child.SelectSingleNode('CartItemGuid')
                if ParentItemGuid.InnerText.strip() not in xmlItems:
                    if CartItemGuid.InnerText.strip() in xmlItems:
                        xmlData += child.OuterXml.ToString()
                        xmlData += xmlItems[CartItemGuid.InnerText.strip()]
                    else:
                        xmlData += child.OuterXml.ToString()
            return xmlData.strip()


        def replace_mainitems(match):
            return match.group(1) + new_content + match.group(3)

        def getQuoteNode(node):
            if node.Name == 'GetQuoteDataResult' and 'TPC System Name' in node.InnerText and 'TPC_Product' in node.InnerText:
                new_content = processQuoteData(node.InnerText.strip())
                pattern = re.compile(r'(<MainItems>).*?(</MainItems>)', re.DOTALL)
                node.InnerText = pattern.sub(r"\1" + new_content + r"\2", node.InnerText)
                #node.InnerText = re.sub(r"(<MainItems>)(.*?)(</MainItems>)", r"\1" + new_content + r"\3", node.InnerText, re.DOTALL)
            for child in node.ChildNodes:
                getQuoteNode(child)

        getQuoteNode(doc)
        xml_bytes = """<?xml version="1.0" encoding="utf-8"?>""" + '
' + doc.OuterXml.encode('utf-8') #doc.OuterXml.encode('utf-8')
    else:
        xml_bytes = response
    xml_array = System.Array[System.Byte](list(bytearray(xml_bytes)))
    ApiResponse = ApiResponseFactory.FileResponse('application/xml', xml_array)
except Exception as ex:
    Log.Info('GetQuoteData Fail-->>'+str(ex))