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

SPARE_PARTS_CABINET_LIST=SqlHelper.GetList("Select * from SPARE_PARTS_CABINET Where Model_Number='{}'".format(Model_ID)).ToList()
List_TobePopulated=SPARE_PARTS_CABINET_LIST.Where(lambda x:(x.Attribute == 'Spare_Parts_Cabinet_Thermostat_Required' and x.Option == Product.Attr('Spare_Parts_Cabinet_Thermostat_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Power_Entry' and x.Option ==Product.Attr('Spare_Parts_Cabinet_Power_Entry').GetValue()) or (x.Attribute =='Spare_Parts_Cabinet_Fan_Required?' and x.Option == Product.Attr('Spare_Parts_Cabinet_Fan_Required?').GetValue() and x.Rule_Attribute_Value == Product.Attr('Spare_Parts_Cabinet_Fan_Voltage').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Fan_Voltage' and x.Option== Product.Attr('Spare_Parts_Cabinet_Fan_Voltage').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Light_Required' and x.Option ==Product.Attr('Spare_Parts_Cabinet_Light_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Door_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Door_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Keylock_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Keylock_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length' and x.Option == Product.Attr('Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Color' and x.Option == Product.Attr('Spare_Parts_Cabinet_Color').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Hinge_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Hinge_Type').GetValue()) or (x.Attribute == 'Series_C_Cabinet_Base_Required' and x.Option == Product.Attr('Series_C_Cabinet_Base_Required').GetValue()) or (x.Attribute == 'Series_C_Power_System_Vendor' and x.Option == Product.Attr('Series_C_Power_System_Vendor').GetValue() and x.Rule_Attribute_Value == Product.Attr('Series_C_Power_System_Type').GetValue()) or (x.Default == 'TRUE')).Select(lambda y: y)
cont = Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary')
attr_map = dict()
Price_map = dict()
Description_map = dict()
for av in Product.Attr('Spare_Parts_Series_C_Cabinet_Part_Summary').SelectedValues:
    attr_map[av.Display] = av.Quantity
for p in List_TobePopulated:
    Price_map[p.Part_Number] = p.Price
    Description_map[p.Part_Number] = p.Description
if cont.Rows.Count > 0:
    for row in cont.Rows:
        row.IsSelected = True
        row['Quantity'] = str(attr_map[row['PartNumber']])
        row['Price'] = str(Price_map[row['PartNumber']])
        row['Part_Number_Description'] = str(Description_map[row['PartNumber']])
        row.Calculate()
        for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
            if attr.Name == "ItemQuantity":
                attr.AssignValue(str(attr_map[row['PartNumber']]))
        row.ApplyProductChanges()
    cont.Calculate()