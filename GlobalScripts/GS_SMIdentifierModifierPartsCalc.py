def postionalChar(inputString, pos):
    if len(inputString) >= pos and pos > 0:
        pos -= 1
        return inputString[pos]
    else:
        return ''

def getParams(Product):
    EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
    cont = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont')
    cont2 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont')
    NoOfSMSCUniversalSafetyCabinet = 0
    posString1 = posString2 = ''
    if EnclosureType == "Universal Safety Cab-1.3M":
        if cont.Rows.Count > 0:
            SMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            IDModSMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value.strip()
            cainetCount = cont.Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
            if cainetCount != '':
                NoOfSMSCUniversalSafetyCabinet = int(cainetCount)
            if SMSCUniversalSafetyCabinet == "Yes" and IDModSMSCUniversalSafetyCabinet != '':
                for pos in [4, 7, 9, 10, 14]:
                    posString1 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)
                for pos in [4, 6, 7, 9, 10, 14]:
                    posString2 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)

        if cont2.Rows.Count > 0 and SMSCUniversalSafetyCabinet == "No":
            #No S300: X, Redundant S300: S, Non Redundant S300: N
            S300 = cont2.Rows[0].GetColumnByName('S300').Value
            #Default Marshalling FC-TUIO51/52: M, Universal Marshalling, PTA: U, Intrinsically Safe: I, 32 IS, 64 Non-IS: A, 64 IS, 32 Non-IS: B, 32 IS, 32 Non-IS:C
            FTA_PUIO = cont2.Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').Value
            #Default Marshalling FC-TDIO51/52: M, Universal Marshalling, PTA: U, Intrinsically Safe: I, 32 IS, 64 Non-IS: A, 64 IS, 32 Non-IS: B, 32 IS, 32 Non-IS:C
            FTA_PDIO = cont2.Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').Value
            #96: C, 64: B, 32: A, 0:X
            PUIO = cont2.Rows[0].GetColumnByName('PUIO_Count').Value
            #96: C, 64: B, 32: A, 0:X
            PDIO = cont2.Rows[0].GetColumnByName('PDIO_Count').Value
            #Redundant IO: R, Non Redundant IO: X
            IO_Redundancy = cont2.Rows[0].GetColumnByName('IO_Redundancy').Value
            posString1 = "{}{}{}{}{}".format(S300,FTA_PDIO,PUIO,PDIO,IO_Redundancy)
            posString2 = "{}{}{}{}{}{}".format(S300,FTA_PUIO,FTA_PDIO,PUIO,PDIO,IO_Redundancy)
    return posString1, posString2, NoOfSMSCUniversalSafetyCabinet

#CXCPQ-33310
def getFCTDIO11(Product, parts_dict):
    posString1, posString2, NoOfSMSCUniversalSafetyCabinet = getParams(Product)
    qty = 0
    if posString1 != '' and NoOfSMSCUniversalSafetyCabinet > 0:
        if posString1 in ['SMXAR', 'XMXAR', 'SMXAX', 'XMXAX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SMXBR', 'XMXBR', 'SMXBX', 'XMXBX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SMXCR', 'XMXCR', 'SMXCX', 'XMXCX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SUXCR', 'XUXCR', 'SUXCX', 'XUXCX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SUXAR', 'XUXAR', 'SUXAX', 'XUXAX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SUXBR', 'XUXBR', 'SUXBX', 'XUXBX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMAAR', 'XMMAAR', 'SMMAAX', 'XMMAAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMABR', 'XMMABR', 'SMMABX', 'XMMABX']:
            qty =  2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMBAR', 'XMMBAR', 'SMMBAX', 'XMMBAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMAAR', 'XUMAAR', 'SUMAAX', 'XUMAAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMABR', 'XUMABR', 'SUMABX', 'XUMABX']:
            qty =  2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMBAR', 'XUMBAR', 'SUMBAX', 'XUMBAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUUABR', 'XUUABR', 'SUUABX', 'XUUABX']:
            qty =  2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMUBAR', 'XMUBAR', 'SMUBAX', 'XMUBAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUUBAR', 'XUUBAR', 'SUUBAX', 'XUUBAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMUAAR', 'XMUAAR', 'SMUAAX', 'XMUAAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUUAAR', 'XUUAAR', 'SUUAAX', 'XUUAAX']:
            qty =  NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMUABR', 'XMUABR', 'SMUABX', 'XMUABX']:
            qty =  2 * NoOfSMSCUniversalSafetyCabinet
    if qty > 0:
        parts_dict["FC-TDIO11"] = {'Quantity' : qty , 'Description': 'SC IOTA SDIO REDUNDANT'}
    return parts_dict

#CXCPQ-33321
def getFCTDIO51(Product, parts_dict):
    posString1, posString2, NoOfSMSCUniversalSafetyCabinet = getParams(Product)
    qty = 0
    if posString1 != '' and NoOfSMSCUniversalSafetyCabinet > 0:
        if posString1 in ['SMXAR', 'XMXAR', 'SMXAX', 'XMXAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SMXBR', 'XMXBR', 'SMXBX', 'XMXBX']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMAAR', 'XMMAAR', 'SMMAAX', 'XMMAAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMABR', 'XMMABR', 'SMMABX', 'XMMABX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SMXCR', 'XMXCR', 'SMXCX', 'XMXCX']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMAAR', 'XUMAAR', 'SUMAAX', 'XUMAAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMABR', 'XUMABR', 'SUMABX', 'XUMABX']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet
    if qty > 0:
        parts_dict["FC-TDIO51"] = {'Quantity' : qty , 'Description': 'SC SAFETY FTA KNIFE, EOL, 24VDC, 16CH, L'}
    return parts_dict

#CXCPQ-32664
def getFCTUIO11(Product, parts_dict):
    posString1, posString2, NoOfSMSCUniversalSafetyCabinet = getParams(Product)

    #Updating the Pos String1 as it is differ for this story
    if NoOfSMSCUniversalSafetyCabinet > 0:
        SMSCUniversalSafetyCabinet = IDModSMSCUniversalSafetyCabinet = ''
        cont = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont')
        cont2 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont')
        if cont.Rows.Count > 0:
            SMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            IDModSMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value.strip()
        if SMSCUniversalSafetyCabinet == "Yes" and IDModSMSCUniversalSafetyCabinet != '':
            posString1 = ''
            for pos in [4, 6, 9, 10, 14]:
                posString1 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)
        if cont2.Rows.Count > 0 and SMSCUniversalSafetyCabinet == "No":
            #No S300: X, Redundant S300: S, Non Redundant S300: N
            S300 = cont2.Rows[0].GetColumnByName('S300').Value
            #Default Marshalling FC-TUIO51/52: M, Universal Marshalling, PTA: U, Intrinsically Safe: I, 32 IS, 64 Non-IS: A, 64 IS, 32 Non-IS: B, 32 IS, 32 Non-IS:C
            FTA_PUIO = cont2.Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').Value
            #Default Marshalling FC-TDIO51/52: M, Universal Marshalling, PTA: U, Intrinsically Safe: I, 32 IS, 64 Non-IS: A, 64 IS, 32 Non-IS: B, 32 IS, 32 Non-IS:C
            FTA_PDIO = cont2.Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').Value
            #96: C, 64: B, 32: A, 0:X
            PUIO = cont2.Rows[0].GetColumnByName('PUIO_Count').Value
            #96: C, 64: B, 32: A, 0:X
            PDIO = cont2.Rows[0].GetColumnByName('PDIO_Count').Value
            #Redundant IO: R, Non Redundant IO: X
            IO_Redundancy = cont2.Rows[0].GetColumnByName('IO_Redundancy').Value
            posString1 = "{}{}{}{}{}".format(S300,FTA_PUIO,PUIO,PDIO,IO_Redundancy)

    qty = 0
    if posString1 != '' and NoOfSMSCUniversalSafetyCabinet > 0:
        if posString1 in ['SMAXR', 'XMAXR', 'SMAXX', 'XMAXX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SMBXR', 'XMBXR', 'SMBXX', 'XMBXX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMAAR', 'XMMAAR', 'SMMAAX', 'XMMAAX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMABR', 'XMMABR', 'SMMABX', 'XMMABX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMMBAR', 'XMMBAR', 'SMMBAX', 'XMMBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SMCXR', 'XMCXR', 'SMCXX', 'XMCXX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SUAXR', 'XUAXR', 'SUAXX', 'XUAXX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SUBXR', 'XUBXR', 'SUBXX', 'XUBXX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMAAR', 'XUMAAR', 'SUMAAX', 'XUMAAX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMABR', 'XUMABR', 'SUMABX', 'XUMABX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUMBAR', 'XUMBAR', 'SUMBAX', 'XUMBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUUABR', 'XUUABR', 'SUUABX', 'XUUABX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMUBAR', 'XMUBAR', 'SMUBAX', 'XMUBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUUBAR', 'XUUBAR', 'SUUBAX', 'XUUBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMUAAR', 'XMUAAR', 'SMUAAX', 'XMUAAX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SUUAAR', 'XUUAAR', 'SUUAAX', 'XUUAAX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString2 in ['SMUABR','SMIABR','SMCABR','XMUABR','XMIABR','XMCABR', 'SMUABX','SMIABX','SMCABX','XMUABX','XMIABX','XMCABX']:
            qty = NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['SUCXR', 'XUCXR', 'SUCXX', 'XUCXX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet
    if qty > 0:
        parts_dict["FC-TUIO11"] = {'Quantity' : qty , 'Description': 'SC IOTA SAFETY UIO REDUNDANT'}
    return parts_dict

def getFCPUIO01Params(Product):
    EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
    cont = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont')
    cont2 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont')
    NoOfSMSCUniversalSafetyCabinet = 0
    posString1 = posString2 = ''
    if EnclosureType == "Universal Safety Cab-1.3M":
        if cont.Rows.Count > 0:
            SMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            IDModSMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value.strip()
            cainetCount = cont.Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
            if cainetCount != '':
                NoOfSMSCUniversalSafetyCabinet = int(cainetCount)
            if SMSCUniversalSafetyCabinet == "Yes" and IDModSMSCUniversalSafetyCabinet != '':
                for pos in [4, 6, 9, 10, 14]:
                    posString1 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)
                for pos in [4, 6, 7, 9, 10, 14]:
                    posString2 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)

        if cont2.Rows.Count > 0 and SMSCUniversalSafetyCabinet == "No":
            #No S300: X, Redundant S300: S, Non Redundant S300: N
            S300 = cont2.Rows[0].GetColumnByName('S300').Value
            #Default Marshalling FC-TUIO51/52: M, Universal Marshalling, PTA: U, Intrinsically Safe: I, 32 IS, 64 Non-IS: A, 64 IS, 32 Non-IS: B, 32 IS, 32 Non-IS:C
            FTA_PUIO = cont2.Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').Value
            #Default Marshalling FC-TDIO51/52: M, Universal Marshalling, PTA: U, Intrinsically Safe: I, 32 IS, 64 Non-IS: A, 64 IS, 32 Non-IS: B, 32 IS, 32 Non-IS:C
            FTA_PDIO = cont2.Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').Value
            #96: C, 64: B, 32: A, 0:X
            PUIO = cont2.Rows[0].GetColumnByName('PUIO_Count').Value
            #96: C, 64: B, 32: A, 0:X
            PDIO = cont2.Rows[0].GetColumnByName('PDIO_Count').Value
            #Redundant IO: R, Non Redundant IO: X
            IO_Redundancy = cont2.Rows[0].GetColumnByName('IO_Redundancy').Value
            posString1 = "{}{}{}{}{}".format(S300,FTA_PUIO,PUIO,PDIO,IO_Redundancy)
            posString2 = "{}{}{}{}{}{}".format(S300,FTA_PUIO,FTA_PDIO,PUIO,PDIO,IO_Redundancy)
    return posString1, posString2, NoOfSMSCUniversalSafetyCabinet

def getFCPUIO01(Product, parts_dict):
    posString1, posString2, NoOfSMSCUniversalSafetyCabinet = getFCPUIO01Params(Product)
    qty = 0
    if posString1 != '' and NoOfSMSCUniversalSafetyCabinet > 0:
        if posString1 in ['SMAXR','XMAXR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 1
        elif posString1 in ['SMAXX','XMAXX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 2
        elif posString1 in ['SMBXR','XMBXR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 3
        elif posString1 in ['SMBXX','XMBXX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 4
        elif posString2 in ['SMMAAR','XMMAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 5
        elif posString2 in ['SMMAAX','XMMAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 6
        elif posString2 in ['SMMABR','XMMABR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 7
        elif posString2 in ['SMMABX','XMMABX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 8
        elif posString2 in ['SMMBAR','XMMBAR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 9
        elif posString2 in ['SMMBAX','XMMBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 10
        elif posString1 in ['SMCXR','XMCXR']:
            qty = 6 * NoOfSMSCUniversalSafetyCabinet # 11
        elif posString1 in ['SMCXX','XMCXX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet # 12
        elif posString1 in ['SUAXR','XUAXR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 13
        elif posString1 in ['SUAXX','XUAXX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 14
        elif posString1 in ['SUBXR','XUBXR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 15
        elif posString1 in ['SUBXX','XUBXX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 16
        elif posString2 in ['SUMAAR','XUMAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 17
        elif posString2 in ['SUMAAX','XUMAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 18
        elif posString2 in ['SUMABR','XUMABR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 19
        elif posString2 in ['SUMABX','XUMABX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 20
        elif posString2 in ['SUMBAR','XUMBAR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 21
        elif posString2 in ['SUMBAX','XUMBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 22
        elif posString2 in ['SUUABR','XUUABR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 23
        elif posString2 in ['SUUABX','XUUABX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 24
        elif posString2 in ['SMUBAR','XMUBAR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 25
        elif posString2 in ['SMUBAX','XMUBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 26
        elif posString2 in ['SUUBAR','XUUBAR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 27
        elif posString2 in ['SUUBAX','XUUBAX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 28
        elif posString2 in ['SMUAAR','XMUAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 29
        elif posString2 in ['SMUAAX','XMUAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 30
        elif posString2 in ['SUUAAR','XUUAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 31
        elif posString2 in ['SUUAAX','XUUAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 32
        elif posString2 in ['SMUABR','XMUABR','SMIABR','XMIABR','SMCABR','XMCABR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 33
        elif posString2 in ['SMUABX','XMUABX','SMIABX','XMIABX','SMCABX','XMCABX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 34
        elif posString1 in ['SUCXR','XUCXR']:
            qty = 6 * NoOfSMSCUniversalSafetyCabinet # 35
        elif posString1 in ['SUCXX','XUCXX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet # 36
    if qty > 0:
        parts_dict["FC-PUIO01"] = {'Quantity' : qty , 'Description': 'SC SAFETY UIO'}
    return parts_dict

def getFCPDIO01(Product, parts_dict):
    posString1, posString2, NoOfSMSCUniversalSafetyCabinet = getParams(Product)
    qty = 0
    if posString1 != '' and NoOfSMSCUniversalSafetyCabinet > 0:
        if posString1 in ['SMXAR','XMXAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 1
        elif posString1 in ['SMXAX','XMXAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 2
        elif posString1 in ['SMXBR','XMXBR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 3
        elif posString1 in ['SMXBX','XMXBX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 4
        elif posString2 in ['SMMAAR','XMMAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 5
        elif posString2 in ['SMMAAX','XMMAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 6
        elif posString2 in ['SMMABR','XMMABR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 7
        elif posString2 in ['SMMABX','XMMABX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 8
        elif posString2 in ['SMMBAR','XMMBAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 9
        elif posString2 in ['SMMBAX','XMMBAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 10
        elif posString1 in ['SMXCR','XMXCR']:
            qty = 6 * NoOfSMSCUniversalSafetyCabinet # 11
        elif posString1 in ['SMXCX','XMXCX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet # 12
        elif posString2 in ['SUMAAR','XUMAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 13
        elif posString2 in ['SUMAAX','XUMAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 14
        elif posString2 in ['SUMABR','XUMABR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 15
        elif posString2 in ['SUMABX','XUMABX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 16
        elif posString2 in ['SUMBAR','XUMBAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 17
        elif posString2 in ['SUMBAX','XUMBAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 18
        elif posString1 in ['SUXCR','XUXCR']:
            qty = 6 * NoOfSMSCUniversalSafetyCabinet # 19
        elif posString1 in ['SUXCX','XUXCX']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet # 20
        elif posString2 in ['SUUABR','XUUABR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 21
        elif posString2 in ['SUUABX','XUUABX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 22
        elif posString2 in ['SMUBAR','XMUBAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 23
        elif posString2 in ['SMUBAX','XMUBAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 24
        elif posString2 in ['SUUBAR','XUUBAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 25
        elif posString2 in ['SUUBAX','XUUBAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 26
        elif posString2 in ['SMUAAR','XMUAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 27
        elif posString2 in ['SMUAAX','XMUAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 28
        elif posString1 in ['SUXAR','XUXAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 29
        elif posString1 in ['SUXAX','XUXAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 30
        elif posString1 in ['SUXBR','XUXBR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 31
        elif posString1 in ['SUXBX','XUXBX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 32
        elif posString2 in ['SUUAAR','XUUAAR']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 33
        elif posString2 in ['SUUAAX','XUUAAX']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet # 34
        elif posString2 in ['SMUABR','XMUABR']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet # 35
        elif posString2 in ['SMUABX','XMUABX']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet # 36
    if qty:
        parts_dict["FC-PDIO01"] = {'Quantity' : qty , 'Description': 'SDIO Module Assembly'}
    return parts_dict

def getFCMCC003(Product, parts_dict):
    EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
    cont = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont')
    cont2 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont')
    NoOfSMSCUniversalSafetyCabinet = 0
    posString1 = ''
    posString2 = ''
    posString3 = ''
    if EnclosureType == "Universal Safety Cab-1.3M":
        if cont.Rows.Count > 0:
            SMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            IDModSMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value.strip()
            cainetCount = cont.Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
            if cainetCount != '':
                NoOfSMSCUniversalSafetyCabinet = int(cainetCount)
            if SMSCUniversalSafetyCabinet == "Yes" and IDModSMSCUniversalSafetyCabinet != '':
                #CXCPQ-54369 - Start modified
                for pos3 in [4,18]:
                    posString3 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos3)
                for pos in [9, 10, 18]:
                    posString1 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)
                for pos1 in [4,9,10,18]:
                    posString2 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos1)

        if cont2.Rows.Count > 0 and SMSCUniversalSafetyCabinet == "No":
            #96: C, 64: B, 32: A, 0:X
            PUIO = cont2.Rows[0].GetColumnByName('PUIO_Count').Value
            #96: C, 64: B, 32: A, 0:X
            s_300 = cont2.Rows[0].GetColumnByName("S300").DisplayValue
            PDIO = cont2.Rows[0].GetColumnByName('PDIO_Count').Value
            CNM = cont2.Rows[0].GetColumnByName('Number_of_Control_Network_Module_0-100').Value
            posString1 = "{}{}{}".format(PUIO,PDIO,CNM)
            posString2 = "{}{}{}{}".format(s_300,PUIO,PDIO,CNM)
            posString3 = "{}{}".format(s_300,CNM)
    qty = 0
    if NoOfSMSCUniversalSafetyCabinet:
        if posString3 in ['S0']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet
        if posString3 in ['S4']:
            qty = 3 * NoOfSMSCUniversalSafetyCabinet
        if posString2 in ['XAB2','XBA2','XCX2','XXC2']:
            qty = 2 * NoOfSMSCUniversalSafetyCabinet
        if posString1 in ['AX0', 'XA0']:
            qty = 8 * NoOfSMSCUniversalSafetyCabinet
        elif posString1 in ['BX0', 'XB0', 'AA0']:
            qty = 4 * NoOfSMSCUniversalSafetyCabinet
            #CXCPQ-54369 - End modified
    if qty:
        parts_dict["FC-MCC003"] = {'Quantity' : qty , 'Description': 'Filler panel'}
    return parts_dict

def getFCMCAR01(Product, parts_dict):
    EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
    cont = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont')
    cont2 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont')
    NoOfSMSCUniversalSafetyCabinet = 0
    posString1 = ''
    posString2 = ''
    if EnclosureType == "Universal Safety Cab-1.3M":
        if cont.Rows.Count > 0:
            SMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            IDModSMSCUniversalSafetyCabinet = cont.Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value.strip()
            cainetCount = cont.Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
            if cainetCount != '':
                NoOfSMSCUniversalSafetyCabinet = int(cainetCount)
            if SMSCUniversalSafetyCabinet == "Yes" and IDModSMSCUniversalSafetyCabinet != '':
                #CXCPQ-54369 - Start modified
                for pos in [4,18]:
                    posString1 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos)
                for pos1 in [4,9,10,18]:
                    posString2 += postionalChar(IDModSMSCUniversalSafetyCabinet, pos1)

        if cont2.Rows.Count > 0 and SMSCUniversalSafetyCabinet == "No":
            #96: C, 64: B, 32: A, 0:X
            PUIO = cont2.Rows[0].GetColumnByName('PUIO_Count').Value
            #96: C, 64: B, 32: A, 0:X
            s_300 = cont2.Rows[0].GetColumnByName("S300").DisplayValue
            PDIO = cont2.Rows[0].GetColumnByName('PDIO_Count').Value
            CNM = cont2.Rows[0].GetColumnByName('Number_of_Control_Network_Module_0-100').Value
            posString2 = "{}{}{}{}".format(s_300,PUIO,PDIO,CNM)
            posString1 = "{}{}".format(s_300,CNM)

    qty = 0
    if NoOfSMSCUniversalSafetyCabinet:
        if posString1 in ['S0','S4']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet
        if posString2 in ['XAB2','XBA2','XAA2','XXC2','XCX2','XBX2','XAX2','XXA2','XXB2']:
            qty = 1 * NoOfSMSCUniversalSafetyCabinet
    if qty:
        parts_dict["FC-MCAR-01"] = {'Quantity' : qty , 'Description': 'Filler panel'}
    return parts_dict