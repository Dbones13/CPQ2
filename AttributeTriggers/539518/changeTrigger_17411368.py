import GS_Populate_SM_IO_Modules

#Refresh IO Modules based on Marshalling_option
cont_ATEX = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont')
enclosure_type = ''
if cont_ATEX.Rows.Count > 0:
    enclosure_type = cont_ATEX.Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
if enclosure_type == 'Cabinet':
    cont = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
    #Marshalling_option = TagParserProduct.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Row(1).Column(Marshalling_Option).GetDisplayValue )*>')
    Marshalling_option =cont.Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
else:
    Marshalling_option = 'Hardware Marshalling with Other'
"""if Marshalling_option.strip() == '':
    Marshalling_option = 'Universal Marshalling'"""
GS_Populate_SM_IO_Modules.update_modules_by_marshalling(Product, Marshalling_option)

#Refresh IO Modules based on Universal IOTA type
SM_Universal_IOTA_Type = Product.Attr('SM_Universal_IOTA_Type').GetValue()
GS_Populate_SM_IO_Modules.update_modules_universal_iota(Product, "SM_RG_IO_Count_Digital_Output_Cont", SM_Universal_IOTA_Type)