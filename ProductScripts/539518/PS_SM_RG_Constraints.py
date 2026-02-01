#CXCPQ-31215
import ProductUtil as pu
Product.Attr('ErrorMessage').AssignValue('')
error_msgs = []

Specify_IM_SM = ''
SM_RT_ID_MOD_SM_SC_Cabinet = ''
if Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows.Count > 0:
    Specify_IM_SM = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
    SM_RT_ID_MOD_SM_SC_Cabinet = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
if str(Specify_IM_SM) == 'No':
    Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value = ''
    SM_RT_S300 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300')
    SM_RT_PUIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO')
    SM_RT_PUIO_Count = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PUIO_Count')
    
    SM_RT_PUIO_Count_List = SM_RT_PUIO_Count.ReferencingAttribute.Values
    if SM_RT_S300.Value == 'S' and SM_RT_PUIO.Value == 'M' and SM_RT_PUIO_Count.Value == 'C':
        for i in SM_RT_PUIO_Count_List:
            if i.ValueCode == 'C':
                i.Allowed = False
                pu.addMessage(Product , 'When S300 is selected with default marshalling, max available PUIO channels are 64.')
    elif SM_RT_S300.Value == 'S' and SM_RT_PUIO.Value == 'M':
        for i in SM_RT_PUIO_Count_List:
            if i.ValueCode == 'C':
                i.Allowed = False
            
if len(str(SM_RT_ID_MOD_SM_SC_Cabinet)) > 8:
    if SM_RT_ID_MOD_SM_SC_Cabinet[3] == 'S' and SM_RT_ID_MOD_SM_SC_Cabinet[5] == 'M' and SM_RT_ID_MOD_SM_SC_Cabinet[8] == 'C':
        pu.addMessage(Product , 'When S300 is selected with default marshalling, max available PUIO channels are 64.')
        error_msgs.append('When S300 is selected with default marshalling, max available PUIO channels are 64.')

error_msg = ''
for msg in error_msgs:
    if not error_msg:
        error_msg +=msg
    else:
        error_msg += '<br/>' + msg
Trace.Write('Error Message: ' + str(error_msg))
Product.Attr('ErrorMessage').AssignValue(error_msg)