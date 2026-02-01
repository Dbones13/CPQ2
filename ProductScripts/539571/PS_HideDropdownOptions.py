IOMount = Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()
Trace.Write(IOMount)
Cab_Type = Product.Attr('SerC_RG_Cabinet_Type').GetValue()
if IOMount:
    if IOMount == 'Cabinet' and Cab_Type !='Generic Cabinet':
        cabAccess = Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Trace.Write(cabAccess)
        IMC = Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
        Trace.Write(IMC)
        mar_CabType = Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet_Layout_Type').Values
        Trace.Write(mar_CabType)
        if cabAccess == 'Single Access' and IMC =='Yes':
            for value in mar_CabType:
                if value.Display in ('Front To Back'):
                    value.Allowed = False
                else:
                    value.Allowed = True
        else:
            for value in mar_CabType:
                value.Allowed = True

for attr in Product.Attributes:
    if attr.DisplayType=="DropDown" and attr.Required:
        if not attr.GetValue():
            for val in attr.Values:
                attr.SelectValue(val.ValueCode)
                break