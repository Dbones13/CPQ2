from GS_ITEMCREATE_UPDATE_Functions import populateSimple,populateIdentificationRow,getIdentificationCodeAttrName
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