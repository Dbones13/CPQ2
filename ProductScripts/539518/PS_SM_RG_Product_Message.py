#CXCPQ-34773
import ProductUtil as pu
Product.Attr('ErrorMessage').AssignValue('')
error_msgs = []

 

Specify_IM_SM = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
Trace.Write(Specify_IM_SM)
SM_RT_ID_MOD_SM_SC_Cabinet = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value           
if Specify_IM_SM=='Yes' and len(str(SM_RT_ID_MOD_SM_SC_Cabinet)) != 21:
    pu.addMessage(Product , '''Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier.

Identifier should include alphabetic characters of length 17. Modifiers should

include numbers of length 3. Identifier Modifier should be separated by hyphen.

Please refer the info icon for valid & detailed Identifier-Modifier structure.''')
    error_msgs.append('''Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier.

Identifier should include alphabetic characters of length 17. Modifiers should

include numbers of length 3. Identifier Modifier should be separated by hyphen.

Please refer the info icon for valid & detailed Identifier-Modifier structure.''')
if Specify_IM_SM=='Yes' and len(str(SM_RT_ID_MOD_SM_SC_Cabinet)) == 21 and (SM_RT_ID_MOD_SM_SC_Cabinet[0] !='S' or SM_RT_ID_MOD_SM_SC_Cabinet[1] !='S' or (SM_RT_ID_MOD_SM_SC_Cabinet[2] !='A' and SM_RT_ID_MOD_SM_SC_Cabinet[2] !='B') or (SM_RT_ID_MOD_SM_SC_Cabinet[3] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[3] !='S' and SM_RT_ID_MOD_SM_SC_Cabinet[3] !='N') or (SM_RT_ID_MOD_SM_SC_Cabinet[4] !='S' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='T' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='M' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='N' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='U' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='V' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='W' and SM_RT_ID_MOD_SM_SC_Cabinet[4] !='Y')or (SM_RT_ID_MOD_SM_SC_Cabinet[5] !='M' and SM_RT_ID_MOD_SM_SC_Cabinet[5] !='U' and SM_RT_ID_MOD_SM_SC_Cabinet[5] !='I' and SM_RT_ID_MOD_SM_SC_Cabinet[5] !='A' and SM_RT_ID_MOD_SM_SC_Cabinet[5] !='B' and SM_RT_ID_MOD_SM_SC_Cabinet[5] !='C')or (SM_RT_ID_MOD_SM_SC_Cabinet[6] !='M' and SM_RT_ID_MOD_SM_SC_Cabinet[6] !='U' and SM_RT_ID_MOD_SM_SC_Cabinet[6] !='I' and SM_RT_ID_MOD_SM_SC_Cabinet[6] !='A' and SM_RT_ID_MOD_SM_SC_Cabinet[6] !='B' and SM_RT_ID_MOD_SM_SC_Cabinet[6] !='C')or (SM_RT_ID_MOD_SM_SC_Cabinet[7] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[7] !='P')or (SM_RT_ID_MOD_SM_SC_Cabinet[8] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[8] !='A' and SM_RT_ID_MOD_SM_SC_Cabinet[8] !='B' and SM_RT_ID_MOD_SM_SC_Cabinet[8] !='C')or (SM_RT_ID_MOD_SM_SC_Cabinet[9] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[9] !='A' and SM_RT_ID_MOD_SM_SC_Cabinet[9] !='B' and SM_RT_ID_MOD_SM_SC_Cabinet[9] !='C')or (SM_RT_ID_MOD_SM_SC_Cabinet[10] !='Q' and SM_RT_ID_MOD_SM_SC_Cabinet[10] !='A' and SM_RT_ID_MOD_SM_SC_Cabinet[10] !='E' and SM_RT_ID_MOD_SM_SC_Cabinet[10] !='D')or SM_RT_ID_MOD_SM_SC_Cabinet[11] !='R'or (SM_RT_ID_MOD_SM_SC_Cabinet[12] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[12] !='F')or (SM_RT_ID_MOD_SM_SC_Cabinet[13] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[13] !='R')or (SM_RT_ID_MOD_SM_SC_Cabinet[14] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[14] !='Y')):
    pu.addMessage(Product , '''Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier.

Identifier should include alphabetic characters of length 17. Modifiers should

include numbers of length 3. Identifier Modifier should be separated by hyphen.

Please refer the info icon for valid & detailed Identifier-Modifier structure.''')
    error_msgs.append('''Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier.

Identifier should include alphabetic characters of length 17. Modifiers should

include numbers of length 3. Identifier Modifier should be separated by hyphen.

Please refer the info icon for valid & detailed Identifier-Modifier structure.''')
if Specify_IM_SM=='Yes' and len(str(SM_RT_ID_MOD_SM_SC_Cabinet)) == 21 and ((SM_RT_ID_MOD_SM_SC_Cabinet[15] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[15] !='Y') or (SM_RT_ID_MOD_SM_SC_Cabinet[16] !='X' and SM_RT_ID_MOD_SM_SC_Cabinet[16] !='Y')or (SM_RT_ID_MOD_SM_SC_Cabinet[17] !='-')or (SM_RT_ID_MOD_SM_SC_Cabinet[18] !='0' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='1' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='2' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='3' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='4' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='5'and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='6' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='7' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='8' and SM_RT_ID_MOD_SM_SC_Cabinet[18] !='9')or (SM_RT_ID_MOD_SM_SC_Cabinet[19] !='0' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='1' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='2' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='3' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='4' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='5'and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='6' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='7' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='8' and SM_RT_ID_MOD_SM_SC_Cabinet[19] !='9')or (SM_RT_ID_MOD_SM_SC_Cabinet[20] !='0' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='1' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='2' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='3' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='4' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='5'and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='6' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='7' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='8' and SM_RT_ID_MOD_SM_SC_Cabinet[20] !='9')):
    pu.addMessage(Product , '''Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier.

Identifier should include alphabetic characters of length 17. Modifiers should

include numbers of length 3. Identifier Modifier should be separated by hyphen.

Please refer the info icon for valid & detailed Identifier-Modifier structure.''')
    error_msgs.append('''Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier.

Identifier should include alphabetic characters of length 17. Modifiers should

include numbers of length 3. Identifier Modifier should be separated by hyphen.

Please refer the info icon for valid & detailed Identifier-Modifier structure.''')

error_msg = ''
for msg in error_msgs:
    if not error_msg:
        error_msg +=msg
    else:
        error_msg += '<br/>' + msg
Trace.Write('Error Message: ' + str(error_msg))
Product.Attr('ErrorMessage').AssignValue(error_msg)