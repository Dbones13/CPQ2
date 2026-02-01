from GS_R2Q_NewExpansion_Attribute_ContColms import R2QNewExpansionControlEdgePLC as PRDT
import math
def populate_dvm():
    attributes_dict={"DVM_Number_of_DVM_Workstations":"Numbers_of_CCTV_Work_Stations",
                    "DVM_Number_of_Explosion_Proof_PTZ_Cameras":"Numbers_of_PTZ_Type_Camera_at_Hazardous_Area",
                    "DVM_Number_of_Weather_Proof_PTZ_Cameras":"Numbers_of_PTZ_Type_Camera_at_Safe_Area",
                    "DVM_Number_of_Explosion_Proof_Fixed_Cameras": "Numbers_of_FIXED_Type_Camera_at_Hazardous_Area",
                    "DVM_Number_of_Interior_Fixed_Cameras": "Numbers_of_FIXED_Type_Camera_Indoor",
                    "DVM_Number_of_Weather_Proof_Fixed_Cameras": "Numbers_of_FIXED_Type_Camera_at_Safe_Area",
                     "DVM_Number_of_Interior_PTZ_Cameras":"Numbers_of_PTZ_Type_Camera_Indoor"
                    }
    for attr_key, attr_value in attributes_dict.items():
        dvm_value = Product.Attr(attr_value).GetValue()
        Product.Attr(attr_key).AssignValue(str(dvm_value))
    total_value = 0
    for attr_value in ("Numbers_of_FIXED_Type_Camera_at_Hazardous_Area", "Numbers_of_PTZ_Type_Camera_at_Hazardous_Area", "Numbers_of_FIXED_Type_Camera_at_Safe_Area", "Numbers_of_PTZ_Type_Camera_at_Safe_Area", "Numbers_of_FIXED_Type_Camera_Indoor", "Numbers_of_PTZ_Type_Camera_Indoor"):
            value = Product.Attr(attr_value).GetValue()
            if value and value.isdigit():
                total_value += int(value)
    for row in Product.GetContainerByName('DVM_System_Group_Cont').Rows:
        if total_value != 0:
            row.Product.Attr('DVM_4_Camera_Interface').AssignValue(str(int(math.ceil(float(total_value) / 4))))
        for attr, value in PRDT.products["Digital Video Manager Group"].get('displayValueDict', {}).items():
            row.Product.Attr(attr).SelectDisplayValue(value)
        for attr, value in PRDT.products["Digital Video Manager Group"].get('defaultText', {}).items():
            row.Product.Attr(attr).AssignValue(value)
def hideAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Hidden

def showAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Editable

def readAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.ReadOnly

def setDisplayValue(attrDict):
    for attr, value in attrDict.items():
        #values = ''.join(attrDict[attr])
        Product.Attr(attr).SelectDisplayValue(value)

def hideContainerColumns(contColumnList):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def showContainerColumns(contColumnList):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Editable) )*>'.format(contColumn,col))

def setDefaultText(attrDict):
    for attr, value in attrDict.items():
        if (productName in ('FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3') and Product.Attr(attr).GetValue() == '') or productName in ('Terminal Manager','HC900 Group', 'Fire Detection & Alarm Engineering','Industrial Security (Access Control)', 'Digital Video Manager', 'Digital Video Manager Group'):
            #values = ''.join(attrDict[attr])
            Product.Attr(attr).AssignValue(value)

productName = Product.Name
Log.Info('productName ' + str(productName))
checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr('R2Q_QuoteNumber').AssignValue(str(Quote.CompositeNumber))
    if checkproduct =='PRJT R2Q':
        if productName in PRDT.products:
            hideAttr(PRDT.products[productName].get('hideAttrList', []))
            hideContainerColumns(PRDT.products[productName].get('hideContainerColumnDict', {}))
            showContainerColumns(PRDT.products[productName].get('showContainerColumnDict', {}))
            showAttr(PRDT.products[productName].get('showAttrList', []))
            readAttr(PRDT.products[productName].get('readAttrList', []))
            setDisplayValue(PRDT.products[productName].get('displayValueDict', {}))
            setDefaultText(PRDT.products[productName].get('defaultText', {}))
        if productName == "Digital Video Manager":
            populate_dvm()

else:
    
    Product.Attr('R2QRequest').AssignValue('')
    if productName in PRDT.products:
        hideAttr(PRDT.products[productName].get('nonR2QHideAttrList', []))