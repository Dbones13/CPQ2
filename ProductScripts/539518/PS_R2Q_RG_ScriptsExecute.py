saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
if saveAction != 'Save' and isR2Qquote:
    smRemoteGroup = ['PS_Distance_SM_SC_UIO_DIO_modules','PS_SM_RG_Constraints','PS_Identifier_Modifier_Backend_String_Update','PS_Identifier_Modifier_Constraints','PS_SM_RG_ IOTAs_Component_Calcs','PS_SM_RG_Part_Components','PS_SM_RG_Component_Calcs','PS_SM_remote_Sys_Cabinets_Qty','PS_SM_RG_IMCode_validation','PS_Identifier_Modifier_Constraints_2','PS_SM_RG_Part_Summary','PS_SM_IO_Cnt_Cabinet_1.3','PS_SM_RG_LI_Part_Summary']
    for scr in smRemoteGroup:
        Product.ParseString('<* ExecuteScript({}) *>'.format(scr))