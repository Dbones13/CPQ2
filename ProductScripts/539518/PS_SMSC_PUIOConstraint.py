import ProductUtil as pu
error_msgs = []

idModForSMSC = ''
if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows.Count > 0:
    idModForSMSC = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue

if idModForSMSC=="Yes":
    code=str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
    Trace.Write(code)
    if len(code) >= 23:
        if (code[8] == "X"):
            if (code[9]=="X"):
                error_msgs.append('PUIO is 0 then PDIO is 32 or 64 or 96')
                pu.addMessage(Product , 'PUIO is 0 then PDIO is 32 or 64 or 96')
        if (code[8]== "A"):
            if code[9]=="C":
                error_msgs.append('PUIO is 32 then PDIO is 0 or 32 or 64')
                pu.addMessage(Product , 'PUIO is 32 then PDIO is 0 or 32 or 64')
        if (code[8]== "B"):
            if (code[9]=="C" or code[9]=="B"):
                error_msgs.append('PUIO is 64 then PDIO is 0 or 32')
                pu.addMessage(Product , 'PUIO is 64 then PDIO is 0 or 32')
        if (code[8]== "C"):
            if (code[9]=="A" or code[9]=="C" or code[9]=="B"):
                error_msgs.append('PUIO is 96 then PDIO is 0')
                pu.addMessage(Product , 'PUIO is 96 then PDIO is 0')
         
        if (code[9] == "X"):
            if (code[8]=="X"):
                error_msgs.append('PDIO is 0 then PUIO is 32 or 64 or 96')
                pu.addMessage(Product , 'PDIO is 0 then PUIO is 32 or 64 or 96')
        if (code[9]== "A"):
            if (code[8]=="C"):
                error_msgs.append('PDIO is 32 then PUIO is 0 or 32 or 64')
                pu.addMessage(Product , 'PDIO is 32 then PUIO is 0 or 32 or 64')
        if (code[9]== "B"):
            if (code[8]=="C" or code[8]=="B"):
                error_msgs.append('PDIO is 64 then PUIO is 0 or 32')
                pu.addMessage(Product , 'PDIO is 64 then PUIO is 0 or 32')
        if (code[9]== "C"):
            if (code[8]=="A" or code[8]=="C" or code[8]=="B"):
                error_msgs.append('PDIO is 96 then PUIO is 0')
                pu.addMessage(Product , 'PDIO is 96 then PUIO is 0')
        
if idModForSMSC=="No":
    puio = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
    pdio = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
    if puio=="0" and pdio=="0":
        error_msgs.append('PUIO is 0 then PDIO is 32 or 64 or 96')
        pu.addMessage(Product , 'PUIO is 0 then PDIO is 32 or 64 or 96')
    else:
        error_msgs.append('')
        pu.addMessage(Product , '')
    if puio=="32" and pdio=="96":
        error_msgs.append('PUIO is 32 then PDIO is 0 or 32 or 64')
        pu.addMessage(Product , 'PUIO is 32 then PDIO is 0 or 32 or 64')
    if puio=="64" and (pdio=="96" or pdio=="64"):
        error_msgs.append('PUIO is 64 then PDIO is 0 or 32')
        pu.addMessage(Product , 'PUIO is 64 then PDIO is 0 or 32')
    if puio=="96" and (pdio=="32" or pdio=="96" or pdio=="64"):
        error_msgs.append('PUIO is 96 then PDIO is 0')
        pu.addMessage(Product , 'PUIO is 96 then PDIO is 0')
        
    if puio=="0" and pdio=="0":
        error_msgs.append('PDIO is 0 then PUIO is 32 or 64 or 96')
        pu.addMessage(Product , 'PDIO is 0 then PUIO is 32 or 64 or 96')
    if pdio=="32" and puio=="96":
        error_msgs.append('PDIO is 32 then PUIO is 0 or 32 or 64')
        pu.addMessage(Product , 'PDIO is 32 then PUIO is 0 or 32 or 64')
    if pdio=="64" and (puio=="96" or puio=="64"):
        error_msgs.append('PDIO is 64 then PUIO is 0 or 32')
        pu.addMessage(Product , 'PDIO is 64 then PUIO is 0 or 32')
    if pdio=="96" and (puio=="32" or puio=="96" or puio=="64"):
        error_msgs.append('PDIO is 96 then PUIO is 0')
        pu.addMessage(Product , 'PDIO is 96 then PUIO is 0')
error_msg = ''
for msg in error_msgs:
    if not error_msg:
        error_msg +=msg
    else:
        error_msg += '<br/>' + msg
Trace.Write('Error Message: ' + str(error_msg))
Product.Attr('ErrorMsg_eng2').AssignValue(error_msg)