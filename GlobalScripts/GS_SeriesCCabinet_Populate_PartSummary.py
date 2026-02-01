def setAtvQty(AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=True
            av.Quantity=qty
            Trace.Write('Selected ' + sv + ' in  attribute ' + AttrName + ' at Qty ' + str(qty))
            break
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

SPARE_PARTS_CABINET_LIST=SqlHelper.GetList("Select * from SPARE_PARTS_CABINET Where Model_Number='{}'".format(Model_ID))
List_TobePopulated= [x for x in SPARE_PARTS_CABINET_LIST if((x.Attribute == 'Spare_Parts_Cabinet_Thermostat_Required' and x.Option == Product.Attr('Spare_Parts_Cabinet_Thermostat_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Power_Entry' and x.Option ==Product.Attr('Spare_Parts_Cabinet_Power_Entry').GetValue()) or (x.Attribute =='Spare_Parts_Cabinet_Fan_Required?' and x.Option == Product.Attr('Spare_Parts_Cabinet_Fan_Required?').GetValue() and x.Rule_Attribute_Value == Product.Attr('Spare_Parts_Cabinet_Fan_Voltage').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Fan_Voltage' and x.Option== Product.Attr('Spare_Parts_Cabinet_Fan_Voltage').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Light_Required' and x.Option ==Product.Attr('Spare_Parts_Cabinet_Light_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Door_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Door_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Keylock_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Keylock_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length' and x.Option == Product.Attr('Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Color' and x.Option == Product.Attr('Spare_Parts_Cabinet_Color').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Hinge_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Hinge_Type').GetValue()) or (x.Attribute == 'Series_C_Cabinet_Base_Required' and x.Option == Product.Attr('Series_C_Cabinet_Base_Required').GetValue()) or (x.Attribute == 'Series_C_Power_System_Vendor' and x.Option == Product.Attr('Series_C_Power_System_Vendor').GetValue() and x.Rule_Attribute_Value == Product.Attr('Series_C_Power_System_Type').GetValue()) or (x.Default == 'TRUE'))]
Trace.Write(RestClient.SerializeToJson(List_TobePopulated))
Product.DisallowAttr('Spare_Parts_Series_C_Cabinet_Part_Summary')
for Row in List_TobePopulated:
    Trace.Write(Row.Part_Number)
    if Row.Part_Number!= "" and Row.Qty and int(Row.Qty):
        setAtvQty('Spare_Parts_Series_C_Cabinet_Part_Summary',Row.Part_Number,int(Row.Qty))