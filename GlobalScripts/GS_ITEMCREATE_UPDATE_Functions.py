from System.Text import Encoding
def deleteRows(table , ids):
    for id in ids:
        table.DeleteRow(id)

def populateQuoteTableRow(table , dataDict , row = None):
        #Log.Info(str(dataDict))
        if not row:
            row = table.AddNewRow()
        for key , value in dataDict.items():
            row[key] = value
def loadwtwfactor(quote):
        wtwfactor_dict ={}
        nonpricecont ={}
        Wtwfactor = """SELECT CATALOGCODE  as PartNumber, WTW_FACTOR from  CART_ITEM A(nolock) JOIN HPS_PRODUCTS_MASTER hpm(NOLOCK) ON A.CATALOGCODE = hpm.PartNumber JOIN HPS_PLSG_WTW_FACTOR wtw(NOLOCK) on hpm.PLSG = wtw.PL_PLSG   where  CART_ID  = '{}' and USERID  = '{}'
                union all
                SELECT CATALOGCODE as PartNumber, WTW_FACTOR as WTW_FACTOR from  CART_ITEM A(nolock) JOIN WriteInProducts wrt(NOLOCK) on A.CATALOGCODE = wrt.Product join HPS_PLSG_WTW_FACTOR wtw(NOLOCK) on wrt.ProductLineSubGroup = wtw.PL_PLSG where  CART_ID  = '{}' and USERID  = '{}'
                union all
                SELECT GES_Service_Material as PartNumber,  WTWMarkupFactorEstimated as WTW_FACTOR  from CART_ITEM A(nolock) join Labor_GES_WTW_Markup_Factor(NOLOCK) on A.CATALOGCODE = GES_Service_Material  where  CART_ID  = '{}' and USERID  = '{}'""".format(quote.QuoteId,quote.UserId,quote.QuoteId,quote.UserId,quote.QuoteId,quote.UserId)

        res = SqlHelper.GetList(Wtwfactor)
        if res:
            wtwfactor_dict = {item.PartNumber : item.WTW_FACTOR for item in res}
        j=0
        x=SqlHelper.GetFirst("SELECT Count(*) as cnt FROM HPS_PLSG_WTW_FACTOR")
        qcount = int(x.cnt/1000)+1
        for i in range(qcount):
            Trace.Write(str(i))
            res2=SqlHelper.GetList("SELECT PL_PLSG, WTW_FACTOR FROM HPS_PLSG_WTW_FACTOR WHERE CpqTableEntryId BETWEEN {} AND {}".format(str(j+1),str(j+1000)))
            j+=1000
            if res2:
                for item in res2:
                	wtwfactor_dict[item.PL_PLSG] = item.WTW_FACTOR
        nonprice = "select Child_Part as PartNumber from  CART_ITEM A(nolock) JOIN MIGRATION_PART_MAPPING B(NOLOCK) ON A.CATALOGCODE = B.Child_Part JOIN KE_Package_Part_Qty_Mapping (NOLOCK) ON Package_Model_Number = Child_Part and IS_Model_name = 'Y' where  CART_ID  = '{}' and USERID  = '{}'" .format(quote.QuoteId,quote.UserId)
        res1 = SqlHelper.GetList(nonprice)
        if res1: 
            nonpricecont = {item.PartNumber : True  for item in res1} 
        return wtwfactor_dict,nonpricecont

def populateRowFromAttr(VCModelConfiguration,attr , item , code,Product):
    valueSystemId = attr.SelectedValue.SystemId if attr.SelectedValue else ""

    rowDict = {
        'CartItemGUID' : item.QuoteItemGuid,
        'ItemNumber' : item.RolledUpQuoteItem,
        'PartNumber' : Product.PartNumber,
        'ProductName' : Product.Name,
        'ProductDescription' : "{} {}".format(Product.PartNumber , Product.Name),
        'AttributeSystemId' : attr.SystemId,
        'AttributeName': attr.Name,
        'AttributeValueSystemId': valueSystemId,
        'AttributeValueCode': code,
        'AttributeValue': attr.GetValue(),
        'AttributeDescription': "[{}] - {}".format(code , attr.GetValue())
    }
    populateQuoteTableRow(VCModelConfiguration , rowDict)

def populateSetPointAttrs(VCModelConfiguration , sender, Product):
        setPointAttrs = SqlHelper.GetList("select Attr_Name from VC_SetPointAttrs")
        SP_Attrs = [atr.Attr_Name for atr in setPointAttrs]
        for attr in filter(lambda x: x.DisplayType == 'FreeInputNoMatching' and x.Name in SP_Attrs, Product.Attributes):
            valueCode = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
            populateRowFromAttr(VCModelConfiguration,attr , sender ,valueCode,Product)

def getFloat(Var):
    return float(Var) if Var else 0.00

def assignval(resp,prod):
    for atnm in list(resp):
        atnam = str(atnm["atnam"])
        atwtb = str(atnm["atwtb"])
        
        attribute = prod.Attributes.GetBySystemId(atnam)
        a = attribute.DisplayType
        
        if a == "DropDown":
            attribute.SelectValue(atwtb)
        else:  
            attribute.AssignValue(atwtb)

    prod.ApplyRules()
    return prod.IsComplete, prod.TotalPrice

def fn_Check_LineItem(pv_PN_r_FME):
    if pv_PN_r_FME[0] == 'Y':
        lv_pn = pv_PN_r_FME[1:pv_PN_r_FME.find('-')]
    else:
        lv_pn = pv_PN_r_FME[:pv_PN_r_FME.find('-')]

    lv_pnexists = any(i.PartNumber == lv_pn and i.QI_FME.Value == pv_PN_r_FME and i.ParentItemGuid == '' for i in Quote.MainItems)

    return lv_pnexists

def fn_QI_FME_Assignment(fme_in,cartitem):
    Trace.Write(str(cartitem.QI_FME.Value)+'--No change in the FME value--000-->'+str(fme_in))
    if cartitem.QI_FME.Value!='' and cartitem.QI_FME.Value.replace('(','').replace(')','')==fme_in  :
    #QI_FME field is editable on quotation tab. Users can add brackets but FME value from SAP is overriding the QI_FME value. 
    #This logic compares the FME without brackets. If matches,QI_FME value will stay as is...
        Trace.Write('No change in the FME value')

    else:
        cartitem.QI_FME.Value = fme_in


def getfmeval(resp, item):
    fmeval,keynum,ordrval,yspec = "","" ,{},""
    #CXCPQ-90704, CXCPQ-90706
    getprdid = SqlHelper.GetFirst("SELECT PRODUCT_ID FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}' AND PRODUCT_ACTIVE = 'True'".format(str(item.PartNumber)))
    for attnm in list(resp):
        for attr in item.SelectedAttributes:
            #Log.Write("attr--->"+str(attr.Name))
            try:
                attname = str(attr.Name)
            except:
                attname = unicode(attr.Name,encoding="Windows-1252")
            #except:
                #attname = str(attr.Name)
            #Log.Write("attr--->"+str("SELECT SYSTEM_ID FROM ATTRIBUTE_DEFN A JOIN PRODUCT_ATTRIBUTES B ON A.STANDARD_ATTRIBUTE_CODE = B.STANDARD_ATTRIBUTE_CODE WHERE A.STANDARD_ATTRIBUTE_NAME = '{}' AND B.PRODUCT_ID = '{}'".format(attname,str(getprdid.PRODUCT_ID))))
            getsyid = SqlHelper.GetFirst("SELECT SYSTEM_ID FROM ATTRIBUTE_DEFN A JOIN PRODUCT_ATTRIBUTES B ON A.STANDARD_ATTRIBUTE_CODE = B.STANDARD_ATTRIBUTE_CODE WHERE A.STANDARD_ATTRIBUTE_NAME = '{}' AND B.PRODUCT_ID = '{}'".format(attname,str(getprdid.PRODUCT_ID)))
            if getsyid:
                for value in attr.Values:
                    if value.Display:
                        if str(getsyid.SYSTEM_ID) == "V_SPECIAL_OPTIONS":
                            yspec =  str(value.Display)
                        if str(getsyid.SYSTEM_ID) == str(attnm["charAttr"]):
                            ordrval[str(attnm["charClassValue"])] = str(value.Display)
                            '''if "KEY_NUMBER" in str(attnm["charAttr"]):
                                keynum =  str(value.Display)
                            else:
                                fmeval +=  str(value.Display)'''
    '''if fmeval != "" and keynum != "":
        fmeval = keynum + fmeval
    fmeval = ""'''
    Trace.Write(str(resp)+'--rechecking--555-->'+str(ordrval)+'--->'+str(item.QI_FME.Value))
    for k, v in sorted(ordrval.items()):
        fmeval += v
    Trace.Write(str(fmeval)+'--rechecking--666-->'+str(item.QI_FME.Value))
    if yspec.upper() == "YES":
        fmeval = "YSPEC YES"
    return fmeval

def getIdentificationCodeAttrName(Product):
    query = "select Attribute_Name from VC_MODEL_ATTR(nolock) where VC_Model = '{}' and Contribute_Full_Entry = 'YES'".format(Product.PartNumber)
    res = SqlHelper.GetFirst(query)
    return res.Attribute_Name if res else None

def populateSimple(VCModelConfiguration , item):
    rowDict = {
        'CartItemGUID' : item.QuoteItemGuid,
        'ItemNumber' : item.RolledUpQuoteItem ,
        'PartNumber' : item.PartNumber,
        'ProductName' : item.ProductName,
        'ProductDescription' : "{} {}".format(item.PartNumber , item.ProductName)
    }
    populateQuoteTableRow(VCModelConfiguration , rowDict)

def populateIdentificationRow(VCModelConfiguration,attr , item,Product):
    rowDict = {
        'CartItemGUID' : item.QuoteItemGuid,
        'ItemNumber' : item.RolledUpQuoteItem,
        'PartNumber' : Product.PartNumber,
        'ProductName' : Product.Name,
        'ProductDescription' : "{} {}".format(Product.PartNumber , Product.Name),
        'AttributeSystemId' : attr.SystemId,
        'AttributeName': "Configured Model No",
        'AttributeValueSystemId': '',
        'AttributeValueCode': '',
        'AttributeValue': attr.GetValue(),
        'AttributeDescription': item.QI_FME.Value
    }
    populateQuoteTableRow(VCModelConfiguration , rowDict)

def populateVCwithcond(VCModelConfiguration , sender,Product):
    iscallsecfunquery = "select * from VC_MODEL_ATTR where Display_Type = 'FreeInputNoMatching' and Contribute_Model_Code = 'YES' and VC_Model = '{}'".format(sender.PartNumber)
    callSec =  SqlHelper.GetFirst(iscallsecfunquery) is not None
    populateSimple(VCModelConfiguration , sender)

    identificationCodeAttrName = getIdentificationCodeAttrName(Product)

    if identificationCodeAttrName is None:
        return

    identificationAttr = Product.Attr(identificationCodeAttrName)
    populateIdentificationRow(VCModelConfiguration,identificationAttr , sender,Product)

    identificationCode = sender.QI_FME.Value
    if "Table" in identificationCodeAttrName:
        identificationCode = identificationCode.replace('-','')

    if callSec:

        query = "select distinct TOP(1000) Attribute_Name , Position_Length , Position ,  Cast(CASE WHEN Position LIKE '%#_%' ESCAPE '#' THEN LEFT(Position, Charindex('_', Position) - 1) ELSE Position END as INT) as SplitPos from VC_MODEL_ATTR where VC_Model = '{}' and Position <> '' order by SplitPos".format(sender.PartNumber)
        res = SqlHelper.GetList(query)

        counter = 0

        for r in res:
            attr = Product.Attr(r.Attribute_Name)
            populateRowFromAttr(VCModelConfiguration,attr , sender , identificationCode[counter : counter + r.Position_Length],Product)
            counter += r.Position_Length
    else:

        temp = "{} ".format(identificationCode)

        for attr in filter(lambda x:'POS' in x.SystemId or 'CV' in x.SystemId or 'KEY' in x.SystemId, Product.Attributes):
            if temp == " ":
                break
            valueCode = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
            if temp.startswith(valueCode):
                temp = "{}".format(temp[len(valueCode):])
                populateRowFromAttr(VCModelConfiguration,attr , sender ,valueCode,Product)