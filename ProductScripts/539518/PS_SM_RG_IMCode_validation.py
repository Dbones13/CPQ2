idModForSMSC = ''
if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows.Count > 0:
    idModForSMSC = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue
if idModForSMSC=="Yes":
    import ProductUtil as pu
    errorlist=[]
    Trace.Write(str(errorlist))
    rlst=str(errorlist)[1:-1]
    Trace.Write(str(rlst))

    list1=["S"]
    list2=["S"]
    list3=["A","B"]
    list4=["X","S","N"]
    list5=["S","T","M","N","U","V","W","Y"]
    list6=["M","U","I","A","B","C"]
    list7=["M","U","I","A","B","C"]
    list8=["X","P"]
    list9=["X","A","B","C"]
    list10=["X","A","B","C"]
    list11=["Q","A","E","D"]
    list12=["R"]
    list13=["X","F"]
    list14=["X","R"]
    list15=["X","Y"]
    list16=["X","Y","V"]
    list17=["X","Y"]
    list18=["0","2","4"]
    list19=["A","B","C","D","E"]
    list20=["-"]
    list21=["0","1","2","3","4","5","6","7","8","9"]
    list22=["0","1","2","3","4","5","6","7","8","9"]
    list23=["0","1","2","3","4","5","6","7","8","9"]

    code=str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
    if len(code)>=23 :
        if code[0] not in list1:
            errorlist.append(1)
        if code[1] not in list2:
            errorlist.append(2)
        if code[2] not in list3:
            errorlist.append(3)
        if code[3] not in list4:
            errorlist.append(4)
        if code[4] not in list5:
            errorlist.append(5)
        if code[5] not in list6:
            errorlist.append(6)
        if code[6] not in list7:
            errorlist.append(7)
        if code[7] not in list8:
            errorlist.append(8)
        if code[8] not in list9:
            errorlist.append(9)
        if code[9] not in list10:
            errorlist.append(10)
        if code[10] not in list11:
            errorlist.append(11)
        if code[11] not in list12:
            errorlist.append(12)
        if code[12] not in list13:
            errorlist.append(13)
        if code[13] not in list14:
            errorlist.append(14)
        if code[14] not in list15:
            errorlist.append(15)
        if code[15] not in list16:
            errorlist.append(16)
        if code[16] not in list17:
            errorlist.append(17)
        if code[17] not in list18:
            errorlist.append(18)
        if code[18] not in list19:
            errorlist.append(19)
        if code[19] not in list20:
            errorlist.append(20)
        if code[20] not in list21:
            errorlist.append(21)
        if code[21] not in list22:
            errorlist.append(22)
        if code[22] not in list23:
            errorlist.append(23)

    Trace.Write(str(errorlist))
    rlst=str(errorlist)[1:-1]
    Trace.Write(str(rlst))

    if len(errorlist) == 1 :
        pu.addMessage(Product ,"Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier. Identifier should include alphabetic characters of length 19. Modifiers should include numbers of length 3. Identifier Modifier should be separated by hyphen. Please refer the info icon for valid & detailed Identifier-Modifier structure. The character entered in position " +str(rlst) + " is invalid.")
        msg="Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier. Identifier should include alphabetic characters of length 19. Modifiers should include numbers of length 3. Identifier Modifier should be separated by hyphen. Please refer the info icon for valid & detailed Identifier-Modifier structure. The character entered in position " +str(rlst) + " is invalid."
    elif len(errorlist) > 1 :
        pu.addMessage(Product ,"Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier. Identifier should include alphabetic characters of length 19. Modifiers should include numbers of length 3. Identifier Modifier should be separated by hyphen. Please refer the info icon for valid & detailed Identifier-Modifier structure. The character entered in positions " +str(rlst) + " are invalid.")
        msg="Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier. Identifier should include alphabetic characters of length 19. Modifiers should include numbers of length 3. Identifier Modifier should be separated by hyphen. Please refer the info icon for valid & detailed Identifier-Modifier structure. The character entered in positions " +str(rlst) + " are invalid."
    elif len(code)!=23:
        pu.addMessage(Product ,"Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier. Identifier should include alphabetic characters of length 19. Modifiers should include numbers of length 3. Identifier Modifier should be separated by hyphen. Please refer the info icon for valid & detailed Identifier-Modifier structure.")
        msg="Identifier Modifier specified is invalid. Please specify valid Identifier-Modifier. Identifier should include alphabetic characters of length 19. Modifiers should include numbers of length 3. Identifier Modifier should be separated by hyphen. Please refer the info icon for valid & detailed Identifier-Modifier structure."
        error_msg = Product.Attr('ErrorMessage').GetValue()
        error_msg += msg
        Trace.Write('Error Message1: ' + str(error_msg))
        Trace.Write(error_msg)
        Product.Attr('ErrorMessage').AssignValue(error_msg)

    if len(rlst) > 0 :
        error_msg = Product.Attr('ErrorMessage').GetValue()
        error_msg += msg
        Trace.Write('Error Message1: ' + str(error_msg))
        Trace.Write(error_msg)
        Product.Attr('ErrorMessage').AssignValue(error_msg)