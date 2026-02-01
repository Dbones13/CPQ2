# Script Added by Saqlain Malik to Hide dropdown options in Series-C Control Group.
familyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
Cab_Type = Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
if familyType == 'Series C':
    mountSol = Product.Attr('Dummy_CG_IO_Mounting_Solution').GetValue()
    conType = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    modType = Product.Attr('SerC_CG_C300_Controller_Module_Type').Values
    if mountSol == 'Cabinet' and Cab_Type !='Generic Cabinet':
        cabAccess = Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Trace.Write(cabAccess)
        IMC = Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
        Trace.Write(IMC)
        mar_CabType = Product.Attr('SerC_Integrated_Marshalling_Cabinet').Values
        if cabAccess == 'Single Access' and IMC =='Yes':
            if mar_CabType:
                for value in mar_CabType:
                    if value.Display in ('Front To Back'):
                        value.Allowed = False
                    else:
                        value.Allowed = True
                #Product.Attributes.GetByName('SerC_Integrated_Marshalling_Cabinet').SelectDisplayValue('Top To Bottom')
        else:
            for value in mar_CabType:
                value.Allowed = True

    if conType:
        if conType == 'CN100 CEE':
            for value in modType:
                if value.Display == 'C300(PCNT02)':
                    value.Allowed = False
                else:
                    value.Allowed = True
        else:
            for value in modType:
                value.Allowed = True


#import GS_DropDown_Implementation
#GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)