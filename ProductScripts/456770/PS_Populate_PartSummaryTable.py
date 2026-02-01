clr.AddReference('System.Core')
import System
clr.ImportExtensions(System.Linq)
Model_ID=""
Doors=Product.Attr('Spare_Parts_Cabinet_Door_Type').GetValue()
HingeType=Product.Attr('Spare_Parts_Cabinet_Hinge_Type').GetValue()
KeylockType=Product.Attr('Spare_Parts_Cabinet_Keylock_Type').GetValue()
Color=Product.Attr('Spare_Parts_Cabinet_Color').GetValue()
CabinetTypeCustomerPlansToUse=Product.Attr('Spare_Parts_Cabinet_Type_Customer_Plans_To_Use').GetValue()
if Doors == 'Standard' and HingeType == '130 Degree' and KeylockType == 'Standard' and Color == 'Gray-RAL7035':
    if CabinetTypeCustomerPlansToUse == 'Front Access Only':
            Model_ID="CC-C8SS01"
    elif CabinetTypeCustomerPlansToUse == 'Front & Rear Access':
            Model_ID="CC-C8DS01"
if Doors != 'Standard' or HingeType != '130 Degree' or KeylockType != 'Standard' or Color != 'Gray-RAL7035':
    if CabinetTypeCustomerPlansToUse == 'Front Access Only':
            Model_ID="CC-CBDS01"
    elif CabinetTypeCustomerPlansToUse == 'Front & Rear Access':
            Model_ID="CC-CBDD01"
Trace.Write(Model_ID)
SP_PS_Con=Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary')
SPARE_PARTS_CABINET_LIST=SqlHelper.GetList("Select * from SPARE_PARTS_CABINET Where Model_Number='{}'".format(Model_ID)).ToList()
List_TobePopulated=SPARE_PARTS_CABINET_LIST.Where(lambda x:(x.Attribute == 'Spare_Parts_Cabinet_Thermostat_Required' and x.Option == Product.Attr('Spare_Parts_Cabinet_Thermostat_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Power_Entry' and x.Option ==Product.Attr('Spare_Parts_Cabinet_Power_Entry').GetValue()) or (x.Attribute =='Spare_Parts_Cabinet_Fan_Required?' and x.Option == Product.Attr('Spare_Parts_Cabinet_Fan_Required?').GetValue() and x.Rule_Attribute_Value == Product.Attr('Spare_Parts_Cabinet_Fan_Voltage').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Fan_Voltage' and x.Option== Product.Attr('Spare_Parts_Cabinet_Fan_Voltage').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Light_Required' and x.Option ==Product.Attr('Spare_Parts_Cabinet_Light_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Door_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Door_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Keylock_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Keylock_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length' and x.Option == Product.Attr('Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Color' and x.Option == Product.Attr('Spare_Parts_Cabinet_Color').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Hinge_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Hinge_Type').GetValue()) or (x.Attribute == 'Series_C_Cabinet_Base_Required' and x.Option == Product.Attr('Series_C_Cabinet_Base_Required').GetValue()) or (x.Default == 'TRUE')).Select(lambda y: y)
Trace.Write(RestClient.SerializeToJson(List_TobePopulated))
Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary').Clear()
for Row in List_TobePopulated:
    Trace.Write(Row.Part_Number)
    if Row.Part_Number!= "" and Row.Qty and int(Row.Qty):
        ConRow=SP_PS_Con.AddNewRow()
        ConRow["PartNumber"]=Row.Part_Number
        ConRow["Part_Number_Description"]=Row.Description
        ConRow["Quantity"]=Row.Qty
        ConRow["Price"]=Row.Price
    SP_PS_Con.Calculate()
    for row in SP_PS_Con.Rows:
        row.IsSelected = True
    SP_PS_Con.Calculate()