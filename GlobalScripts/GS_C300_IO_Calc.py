#GS_C300_IO_Calc
import System.Decimal as D
import GS_Get_Set_AtvQty
import GS_C300_IO_Calc2

def getFloat(val):
    if val:
        return float(val)
    return 0.00

def roundUp(n):
    res = int(n)
    return res if round(res,2) == round(n,2) else res+1

def removeUnwantedSpaces(input_string):
    input_string =  " ".join(input_string.split())
    return input_string

def getIOCount(Product, AttrName, params):
    resDict = dict()
    for sv in params:
        resDict[sv] = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, sv)
    return resDict

def setIOCount(Product, AttrName, qtyDict):
    for sv in qtyDict.keys():
        GS_Get_Set_AtvQty.setAtvQty(Product, AttrName, sv, qtyDict[sv])


def percentInstalledSpareCalc(Product, AttrName, IO_Count):
    percentInstalledSpare = Product.Attr(AttrName).GetValue()
    IO_Count = getFloat(IO_Count)
    if IO_Count > 0:
        return roundUp(IO_Count * (1 + (getFloat(percentInstalledSpare) * 0.01)))
    else:
        return 0

def updateParam(Product, cont, iOType, column, modules):
    for row in cont.Rows:
        if row['IO_Type'] in iOType:
            for changedColumn in column:
                newValue = getFloat(row[changedColumn])
                if newValue > 0:
                    if '40833' in modules:
                        calcIOModule40833(Product, row['IO_Type'], changedColumn, newValue)
                    elif '40859' in modules:
                        calcIOModule40859(Product, row['IO_Type'], changedColumn, newValue)
                    elif '40872' in modules:
                        calcIOModule40872(Product, row['IO_Type'], changedColumn, newValue)
                    elif '41229' in modules:
                        calcIOModule41229(Product, row['IO_Type'], changedColumn, newValue)  #Newly Added
                    elif '40887' in modules:
                        calcIOModule40887(Product, row['IO_Type'], changedColumn, newValue)
                    elif '40972' in modules:
                        calcIOModule40972(Product, row['IO_Type'], changedColumn, newValue)
                    elif '41449' in modules:
                        calcIOModule41449(Product, row['IO_Type'], changedColumn, newValue)
                    elif '44474' in modules:
                        calcIOModule44474(Product, row['IO_Type'], changedColumn, newValue)
                    elif '44488' in modules:
                        GS_C300_IO_Calc2.calcIOModule44488(Product, row['IO_Type'], changedColumn, newValue)
                    elif '44490' in modules:
                        GS_C300_IO_Calc2.calcIOModule44490(Product, row['IO_Type'], changedColumn, newValue)
                elif newValue == 0 and '44488' in modules:
                    GS_C300_IO_Calc2.calcIOModule44488(Product, row['IO_Type'], changedColumn, newValue)

def applyPercentage(Product, percentInstalledSpare, IO_Family_Type, IO_Mounting_Solution, Universal_Marshalling_Cabinet, contName1, contName2, contName3):
    if IO_Family_Type == 'Series C':
        paramDict = {'D21':0, 'E21':0, 'F21':0, 'D22':0, 'E22':0, 'F22':0, 'D23':0, 'E23':0, 'F23':0, 'D31':0, 'E31':0, 'F31':0, 'D32':0, 'E32':0, 'F32':0, 'D33':0, 'E33':0, 'F33':0,'F41': 0, 'F42': 0, 'F43': 0, 'F51': 0, 'F52': 0, 'F53': 0, 'F61': 0, 'F62': 0, 'F63': 0, 'D71':0, 'E71':0, 'F71':0, 'D72':0, 'E72':0, 'F72':0, 'D73':0, 'E73':0, 'F73':0, 'G41':0, 'H41':0, 'I41':0, 'G42':0, 'H42':0, 'I42':0, 'G43':0, 'H43':0, 'I43':0, 'G44':0, 'H44':0, 'I44':0, 'G51':0, 'H51':0, 'I51':0, 'G52':0, 'H52':0, 'I52':0, 'G53':0, 'H53':0, 'I53':0, 'G54':0, 'H54':0, 'I54':0, 'G64':0, 'H64':0, 'I64':0, 'G74':0, 'H74':0, 'I74':0, 'P31':0, 'Q31':0, 'D81':0, 'E81':0, 'F81':0, 'D82':0, 'E82':0, 'F82':0, 'D83':0, 'E83':0, 'F83':0, 'D84':0, 'E84':0, 'F84':0, 'D91':0, 'E91':0, 'F91':0, 'D92':0, 'E92':0, 'F92':0, 'D93':0, 'E93':0, 'F93':0, 'D94':0, 'E94':0, 'F94':0, 'O41':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'O71':0, 'O81':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'R21':0,'R21':0,'G12':0,'H12':0,'I12':0,'I22':0,'G32':0,'H32':0,'I32':0,'Z11':0,'Z12':0,'Z13':0,'Z23':0,'Z31':0,'Z32':0,'Z33':0,'G81':0,'G82':0,'G83':0,'G91':0,'G92':0,'G93':0,'H81':0,'H82':0,'H83':0,'H91':0,'H92':0,'H93':0,'J11':0,'J12':0,'J13':0,'K11':0,'K12':0,'K13':0,'GG51':0,'HH51':0,'II51':0,'GG81':0,'HH81':0,'II81':0, 'GG61':0, 'HH61':0, 'II61':0, 'GG71':0, 'HH71':0, 'II71':0}  #Newly added
        if IO_Mounting_Solution == 'Cabinet' and Universal_Marshalling_Cabinet == 'No':
            paramDict = {'D21':0, 'E21':0, 'F21':0, 'D22':0, 'E22':0, 'F22':0, 'D23':0, 'E23':0, 'F23':0, 'D31':0, 'E31':0, 'F31':0, 'D32':0, 'E32':0, 'F32':0, 'D33':0, 'E33':0, 'F33':0, 'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0,'F41': 0, 'F42': 0, 'F43': 0, 'F51': 0, 'F52': 0, 'F53': 0, 'F61': 0, 'F62': 0, 'F63': 0,'D71':0, 'E71':0, 'F71':0, 'D72':0, 'E72':0, 'F72':0, 'D73':0, 'E73':0, 'F73':0, 'O11': 0, 'M21': 0, 'N21': 0, 'M31': 0, 'N31': 0, 'G41':0, 'H41':0, 'I41':0, 'G42':0, 'H42':0, 'I42':0, 'G43':0, 'H43':0, 'I43':0, 'G44':0, 'H44':0, 'I44':0, 'G51':0, 'H51':0, 'I51':0, 'G52':0, 'H52':0, 'I52':0, 'G53':0, 'H53':0, 'I53':0, 'G54':0, 'H54':0, 'I54':0, 'G64':0, 'H64':0, 'I64':0, 'G74':0, 'H74':0, 'I74':0, 'P31':0, 'Q31':0, 'D81':0, 'E81':0, 'F81':0, 'D82':0, 'E82':0, 'F82':0, 'D83':0, 'E83':0, 'F83':0, 'D84':0, 'E84':0, 'F84':0, 'D91':0, 'E91':0, 'F91':0, 'D92':0, 'E92':0, 'F92':0, 'D93':0, 'E93':0, 'F93':0, 'D94':0, 'E94':0, 'F94':0, 'O41':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'O71':0, 'O81':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'R21':0,'G12':0,'H12':0,'I12':0,'I22':0,'G32':0,'H32':0,'I32':0,'Z11':0,'Z12':0,'Z13':0,'Z23':0,'Z31':0,'Z32':0,'Z33':0,'GG51':0,'HH51':0,'II51':0,'GG81':0,'HH81':0,'II81':0, 'GG61':0, 'HH61':0, 'II61':0, 'GG71':0, 'HH71':0, 'II71':0}  #Newly added
        else:
            #Reset all GIIS IO paramters to 0
            paramDict2 = {'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0, 'O11': 0, 'M21': 0, 'N21': 0, 'M31': 0, 'N31': 0, 'O41':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'O71':0, 'O81':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'R21':0}  #Newly added
            setIOCount(Product, 'SerC_IO_Params', paramDict2)
        if percentInstalledSpare >= 0:
            cont = Product.GetContainerByName(contName1)
            iOType = ['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)']
            column = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
            updateParam(Product, cont, iOType, column, ['40833'])

            iOType40859 = ['Series-C: LLAI (1) Mux RTD (0-5000)','Series-C: LLAI (1) Mux TC (0-5000)', 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)']
            column40859 = ['Non_Red_IS', 'Non_Red_NIS', 'Non_Red_ISLTR']
            updateParam(Product, cont, iOType40859, column40859, ['40859'])

            iOType40872 = ['Series-C: AO (16) HART (0-5000)']
            column40872 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
            updateParam(Product, cont, iOType40872, column40872, ['40872'])

            iOType = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']
            column = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR', 'Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY', 'Red_HV_RLY', 'Future_Red_HV_RLY', 'Non_Red_HV_RLY']
            ###updateParam(Product, cont, iOType, column, ['40887'])

            iOType41229 = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)']
            column41229 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR', 'Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY', 'Red_HV_RLY', 'Future_Red_HV_RLY', 'Non_Red_HV_RLY']
            updateParam(Product, cont, iOType41229, column41229, ['41229'])  #Newly added

            if contName2 != '' :
                cont2 = Product.GetContainerByName(contName2)
                iOType = ['Series-C: GI/IS HLAI (16) HART (0-5000)', 'Series-C: GI/IS HLAI (16) HART Single Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) HART Dual Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) HART Temperature Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) (0-5000)', 'Series-C: GI/IS HLAI (16) Single Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) Dual Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) Temperature Isolator (0-5000)']
                column = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
                updateParam(Product, cont2, iOType, column, ['40833'])

                iOType40872_1 = ['Series-C: GI/IS AO (16) HART (0-5000)']
                column40872_1 = ['Non_Red_IS']
                updateParam(Product, cont2, iOType40872_1, column40872_1, ['40872'])

                iOType40872_2 = ['Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)', 'Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)']
                column40872_2 = ['Red_IS', 'Future_Red_IS']
                updateParam(Product, cont2, iOType40872_2, column40872_2, ['40872'])

                iOType41229 = ['Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)']
                column41229 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
                updateParam(Product, cont2, iOType41229, column41229, ['41229'])  #Newly Added

                iOType40887 = ['Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)','Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)','Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)','Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)','Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)','Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)','Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)','Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)']
                column40887 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
                updateParam(Product, cont2, iOType40887, column40887, ['40887'])

            if contName3 != '' :
                cont3 = Product.GetContainerByName(contName3)
                iOType40887 = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']
                column40887 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR', 'Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY', 'Red_HV_RLY', 'Future_Red_HV_RLY', 'Non_Red_HV_RLY']
                updateParam(Product, cont3, iOType40887, column40887, ['40887'])

                iOType41229 = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)']
                column41229 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR', 'Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY', 'Red_HV_RLY', 'Future_Red_HV_RLY', 'Non_Red_HV_RLY']
                updateParam(Product, cont3, iOType41229, column41229, ['41229'])

                iOType41449 = ['Series-C: Pulse Input (8) Single Channel (0-5000)', 'Series-C: Pulse Input (4) Dual Channel (0-5000)', 'Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)']
                column41449 = ['Red_IS', 'Future_Red_IS', 'Red_NIS', 'Future_Red_NIS','Red_ISLTR', 'Future_Red_ISLTR']
                updateParam(Product, cont3, iOType41449, column41449, ['41449'])

                iOType40972 = ['Series-C: DI (32) 110 VAC (0-5000)','Series-C: DI (32) 110 VAC PROX (0-5000)','Series-C: DI (32) 220 VAC (0-5000)']
                column40972 = ['Non_Red_NIS', 'Red_NIS', 'Future_Red_NIS']
                updateParam(Product, cont3, iOType40972, column40972, ['40972'])
        else:
            #Reset all IO paramters to 0
            setIOCount(Product, 'SerC_IO_Params', paramDict)
    elif IO_Family_Type == 'Series-C Mark II':
        if percentInstalledSpare > 0:
            cont = Product.GetContainerByName(contName1)
            iOType = ['SCM: DI (32) 110 VAC (0-5000)', 'SCM: DI (32) 220 VAC (0-5000)']
            column = ['Non_Red_NIS']
            updateParam(Product, cont, iOType, column, ['44474'])
            #CXCPQ-44488 and CXDEV-8813(KAOUSALYA ADALA)
            iOType1 = ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)', 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
            column1 = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR', 'Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY', 'Red_HV_Rly', 'Future_HV_Rly', 'Non_Red_HV_Rly']
            updateParam(Product, cont, iOType1, column1, ['44488'])
            iOType2 = ['SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)']
            column2 = ['Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY']
            updateParam(Product, cont, iOType2, column2, ['44488'])

            iOType3 =['SCM: Pulse Input (8) Single Channel (0-5000)', 'SCM: Pulse Input (4) Dual Channel (0-5000)', 'SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)']
            column3 = ['Red_IS', 'Future_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR']
            updateParam(Product, cont, iOType3, column3, ['44490'])

def divideByX(Product, AttrName, paramList, X):
    res = 0
    if X == 0:
        return res
    resDict = getIOCount(Product, AttrName, paramList)
    for key in resDict.keys():
        if resDict[key] > 0:
            res += roundUp(getFloat(resDict[key]/X))
    return res

#CXCPQ-40833
def calcIOModule40833(Product, IO_Type, changedColumn, newValue):
    D21 = E21 = F21 = D22 = E22 = F22 = D23 = E23 = F23 = 0
    D31 = E31 = F31 = D32 = E32 = F32 = D33 = E33 = F33 = 0
    L21 = J31 = K31 = J41 = K41 = J51 = K51 = L61 = J71 = K71 = J81 = K81 = J91 = K91 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: HLAI (16) with HART with differential inputs (0-5000)':
        colMapping = {'Red_IS': 'D21', 'Future_Red_IS': 'E21', 'Non_Red_IS': 'F21', 'Red_NIS': 'D22', 'Future_Red_NIS': 'E22', 'Non_Red_NIS': 'F22', 'Red_ISLTR': 'D23', 'Future_Red_ISLTR': 'E23',  'Non_Red_ISLTR': 'F23'}
    elif IO_Type == 'Series-C: HLAI (16) without HART with differential inputs (0-5000)':
        colMapping = {'Red_IS': 'D31', 'Future_Red_IS': 'E31', 'Non_Red_IS': 'F31', 'Red_NIS': 'D32', 'Future_Red_NIS': 'E32', 'Non_Red_NIS': 'F32', 'Red_ISLTR': 'D33', 'Future_Red_ISLTR': 'E33',  'Non_Red_ISLTR': 'F33'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) HART (0-5000)':
        colMapping = {'Non_Red_IS': 'L21'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) HART Single Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'J31', 'Future_Red_IS': 'K31'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) HART Dual Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'J41', 'Future_Red_IS': 'K41'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) HART Temperature Isolator (0-5000)':
        colMapping = {'Red_IS': 'J51', 'Future_Red_IS': 'K51'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) (0-5000)':
        colMapping = {'Non_Red_IS': 'L61'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) Single Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'J71', 'Future_Red_IS': 'K71'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) Dual Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'J81', 'Future_Red_IS': 'K81'}
    elif IO_Type == 'Series-C: GI/IS HLAI (16) Temperature Isolator (0-5000)':
        colMapping = {'Red_IS': 'J91', 'Future_Red_IS': 'K91'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


def getParts40833(Product, parts_dict):
    paramDict = dict()
    paramDict['Y21'] = divideByX(Product, 'SerC_IO_Params', ['D21', 'D22', 'D23'], 16.0)
    paramDict['Y22'] = divideByX(Product, 'SerC_IO_Params', ['E21', 'E22', 'E23'], 16.0)
    paramDict['Y23'] = divideByX(Product, 'SerC_IO_Params', ['F21', 'F22', 'F23'], 16.0)
    paramDict['Y31'] = divideByX(Product, 'SerC_IO_Params', ['D31', 'D32', 'D33'], 16.0)
    paramDict['Y32'] = divideByX(Product, 'SerC_IO_Params', ['E31', 'E32', 'E33'], 16.0)
    paramDict['Y33'] = divideByX(Product, 'SerC_IO_Params', ['F31', 'F32', 'F33'], 16.0)
    paramDict['Z91'] =  divideByX(Product, 'SerC_IO_Params', ['L21'], 16.0)
    paramDict['W11'] =  divideByX(Product, 'SerC_IO_Params', ['J31'], 16.0)
    paramDict['W12'] =  divideByX(Product, 'SerC_IO_Params', ['K31'], 16.0)
    paramDict['W21'] =  divideByX(Product, 'SerC_IO_Params', ['J41'], 16.0)
    paramDict['W22'] =  divideByX(Product, 'SerC_IO_Params', ['K41'], 16.0)
    paramDict['W31'] =  divideByX(Product, 'SerC_IO_Params', ['J51'], 16.0)
    paramDict['W32'] =  divideByX(Product, 'SerC_IO_Params', ['K51'], 16.0)
    paramDict['W23'] =  divideByX(Product, 'SerC_IO_Params', ['L61'], 16.0)
    paramDict['W41'] =  divideByX(Product, 'SerC_IO_Params', ['J71'], 16.0)
    paramDict['W42'] =  divideByX(Product, 'SerC_IO_Params', ['K71'], 16.0)
    paramDict['W51'] =  divideByX(Product, 'SerC_IO_Params', ['J81'], 16.0)
    paramDict['W52'] =  divideByX(Product, 'SerC_IO_Params', ['K81'], 16.0)
    paramDict['W61'] =  divideByX(Product, 'SerC_IO_Params', ['J91'], 16.0)
    paramDict['W62'] =  divideByX(Product, 'SerC_IO_Params', ['K91'], 16.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PAIH02'] = 2 *(paramDict['Y21']) + paramDict['Y22'] + paramDict['Y23'] + (2*(paramDict['W11']+paramDict['W21']+paramDict['W31'])) + (paramDict['W12']+paramDict['W22']+paramDict['W32']+paramDict['Z91'])
    parts_dict['CC-PAIX02'] = 2 *(paramDict['Y31']) + paramDict['Y32'] + paramDict['Y33'] + (2*(paramDict['W41']+paramDict['W51']+paramDict['W61'])) + (paramDict['W42']+paramDict['W52']+paramDict['W62']+paramDict['W23'])
    return parts_dict

#CXCPQ-40859
def calcIOModule40859(Product, IO_Type, changedColumn, newValue):
    F41 = F42 = F43 = F51 = F52 = F53 = F61 = F62 = F63 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: LLAI (1) Mux RTD (0-5000)':
        colMapping = {'Non_Red_IS': 'F41', 'Non_Red_NIS': 'F42', 'Non_Red_ISLTR': 'F43'}
    elif IO_Type == 'Series-C: LLAI (1) Mux TC (0-5000)':
        colMapping = {'Non_Red_IS': 'F51', 'Non_Red_NIS': 'F52', 'Non_Red_ISLTR': 'F53'}
    elif IO_Type == 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)':
        colMapping = {'Non_Red_IS': 'F61', 'Non_Red_NIS': 'F62', 'Non_Red_ISLTR': 'F63'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


def getParts40859(Product, parts_dict):
    paramDict = dict()
    paramDict['Y43'] = divideByX(Product, 'SerC_IO_Params', ['F41', 'F42', 'F43'], 64.0)
    paramDict['Y53'] = divideByX(Product, 'SerC_IO_Params', ['F51', 'F52', 'F53'], 64.0)
    paramDict['Y63'] = divideByX(Product, 'SerC_IO_Params', ['F61', 'F62', 'F63'], 64.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PAIM01'] = paramDict['Y43'] + paramDict['Y53'] + paramDict['Y63']
    parts_dict['CC-TAIM01'] = paramDict['Y43'] + paramDict['Y53'] + paramDict['Y63']
    return parts_dict

#CXCPQ-40872
def calcIOModule40872(Product, IO_Type, changedColumn, newValue):
    D71 = E71 = F71 = D72 = E72 = F72 = D73 = E73 = F73 = 0
    O11 = M21 = N21 = M31 = N31 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: AO (16) HART (0-5000)':
        colMapping = {'Red_IS': 'D71', 'Future_Red_IS': 'E71', 'Non_Red_IS': 'F71', 'Red_NIS': 'D72', 'Future_Red_NIS': 'E72', 'Non_Red_NIS': 'F72', 'Red_ISLTR': 'D73', 'Future_Red_ISLTR': 'E73',  'Non_Red_ISLTR': 'F73'}
    elif IO_Type == 'Series-C: GI/IS AO (16) HART (0-5000)':
        colMapping = {'Non_Red_IS': 'O11'}
    elif IO_Type == 'Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'M21', 'Future_Red_IS': 'N21'}
    elif IO_Type == 'Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'M31', 'Future_Red_IS': 'N31'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])



def getParts40872(Product, parts_dict):
    paramDict = dict()
    paramDict['Y71'] = divideByX(Product, 'SerC_IO_Params', ['D71', 'D72', 'D73'], 16.0)
    paramDict['Y72'] = divideByX(Product, 'SerC_IO_Params', ['E71', 'E72', 'E73'], 16.0)
    paramDict['Y73'] = divideByX(Product, 'SerC_IO_Params', ['F71', 'F72', 'F73'], 16.0)
    paramDict['W73'] =  divideByX(Product, 'SerC_IO_Params', ['O11'], 16.0)
    paramDict['W81'] =  divideByX(Product, 'SerC_IO_Params', ['M21'], 16.0)
    paramDict['W82'] =  divideByX(Product, 'SerC_IO_Params', ['N21'], 16.0)
    paramDict['W91'] =  divideByX(Product, 'SerC_IO_Params', ['M31'], 16.0)
    paramDict['W92'] =  divideByX(Product, 'SerC_IO_Params', ['N31'], 16.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PAOH01'] = 2 *(paramDict['Y71']) + paramDict['Y72'] + paramDict['Y73'] + (2*(paramDict['W81']+paramDict['W91'])) + (paramDict['W82']+paramDict['W92']+paramDict['W73'])
    parts_dict['CC-TAOX11'] = paramDict['Y71'] + paramDict['Y72']
    parts_dict['CC-TAOX01'] = paramDict['Y73']
    return parts_dict


#CXCPQ-40887
def calcIOModule40887(Product, IO_Type, changedColumn, newValue):
    D81 = E81 = F81 = D82 = E82 = F82 = D83 = E83 = F83 = D84 = E84 = F84 = GG51 = HH51 = II51 = 0
    D91 = E91 = F91 = D92 = E92 = F92 = D93 = E93 = F93 = D94 = E94 = F94 = GG81 = HH81 = II81 = 0
    O41 = M51 = N51 = M61 = N61 = O71 = O81 = M91 = N91 = P11 = Q11 = R21 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)':
        colMapping = {'Red_IS': 'D81', 'Future_Red_IS': 'E81', 'Non_Red_IS': 'F81', 'Red_NIS': 'D82', 'Future_Red_NIS': 'E82', 'Non_Red_NIS': 'F82', 'Red_ISLTR': 'D83', 'Future_Red_ISLTR': 'E83',  'Non_Red_ISLTR': 'F83',  'Red_RLY': 'D84',  'Future_Red_RLY': 'E84', 'Non_Red_RLY': 'F84', 'Red_HV_RLY':'GG51', 'Future_Red_HV_RLY':'HH51', 'Non_Red_HV_RLY':'II51'}
    elif IO_Type == 'Series-C: DI (32) 24VDC SOE (0-5000)':
        colMapping = {'Red_IS': 'D91', 'Future_Red_IS': 'E91', 'Non_Red_IS': 'F91', 'Red_NIS': 'D92', 'Future_Red_NIS': 'E92', 'Non_Red_NIS': 'F92', 'Red_ISLTR': 'D93', 'Future_Red_ISLTR': 'E93',  'Non_Red_ISLTR': 'F93',  'Red_RLY': 'D94',  'Future_Red_RLY': 'E94',  'Non_Red_RLY': 'F94', 'Red_HV_RLY':'GG81', 'Future_Red_HV_RLY':'HH81', 'Non_Red_HV_RLY':'II81'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)':
        colMapping = {'Non_Red_IS': 'O41'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)':
        colMapping = {'Red_IS': 'M51', 'Future_Red_IS': 'N51'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)':
        colMapping = {'Red_IS': 'M61', 'Future_Red_IS': 'N61'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)':
        colMapping = {'Non_Red_IS': 'O71'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)':
        colMapping = {'Non_Red_IS': 'O81'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)':
        colMapping = {'Red_IS': 'M91', 'Future_Red_IS': 'N91'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)':
        colMapping = {'Red_IS': 'P11', 'Future_Red_IS': 'Q11'}
    elif IO_Type == 'Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)':
        colMapping = {'Non_Red_IS': 'R21'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts40887(Product, parts_dict):
    paramDict = dict()
    paramDict['Y81'] = divideByX(Product, 'SerC_IO_Params', ['D81', 'D82', 'D83', 'D84', 'GG51'], 32.0)
    paramDict['Y82'] = divideByX(Product, 'SerC_IO_Params', ['E81', 'E82', 'E83', 'E84', 'HH51'], 32.0)
    paramDict['Y83'] = divideByX(Product, 'SerC_IO_Params', ['F81', 'F82', 'F83', 'F84', 'II51'], 32.0)
    paramDict['Y91'] = divideByX(Product, 'SerC_IO_Params', ['D91', 'D92', 'D93', 'D94', 'GG81'], 32.0)
    paramDict['Y92'] = divideByX(Product, 'SerC_IO_Params', ['E91', 'E92', 'E93', 'E94', 'HH81'], 32.0)
    paramDict['Y93'] = divideByX(Product, 'SerC_IO_Params', ['F91', 'F92', 'F93', 'F94', 'II81'], 32.0)
    paramDict['V13'] =  divideByX(Product, 'SerC_IO_Params', ['O41'], 32.0)
    paramDict['V21'] =  divideByX(Product, 'SerC_IO_Params', ['M51'], 32.0)
    paramDict['V22'] =  divideByX(Product, 'SerC_IO_Params', ['N51'], 32.0)
    paramDict['V31'] =  divideByX(Product, 'SerC_IO_Params', ['M61'], 32.0)
    paramDict['V32'] =  divideByX(Product, 'SerC_IO_Params', ['N61'], 32.0)
    paramDict['V43'] =  divideByX(Product, 'SerC_IO_Params', ['O71'], 32.0)
    paramDict['V53'] =  divideByX(Product, 'SerC_IO_Params', ['O81'], 32.0)
    paramDict['V61'] =  divideByX(Product, 'SerC_IO_Params', ['M91'], 32.0)
    paramDict['V62'] =  divideByX(Product, 'SerC_IO_Params', ['N91'], 32.0)
    paramDict['V71'] =  divideByX(Product, 'SerC_IO_Params', ['P11'], 32.0)
    paramDict['V72'] =  divideByX(Product, 'SerC_IO_Params', ['Q11'], 32.0)
    paramDict['V83'] =  divideByX(Product, 'SerC_IO_Params', ['R21'], 32.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PDIL01'] = 2 *(paramDict['Y81']) + paramDict['Y82'] + paramDict['Y83'] + (2*(paramDict['V21']+paramDict['V31'])) + (paramDict['V13']+paramDict['V22']+paramDict['V32']+paramDict['V43'])
    parts_dict['CC-PDIS01'] = 2 *(paramDict['Y91']) + paramDict['Y92'] + paramDict['Y93'] + (2*(paramDict['V61']+paramDict['V71'])) + (paramDict['V53']+paramDict['V62']+paramDict['V72']+paramDict['V83'])
    parts_dict['CC-TDIL11'] = paramDict['Y81']+paramDict['Y82']+paramDict['Y91']+paramDict['Y92']
    parts_dict['CC-TDIL01'] = paramDict['Y83']+paramDict['Y93']
    return parts_dict

#CXCPQ-40972
#CXCPQ-40972
def calcIOModule40972(Product, IO_Type, changedColumn, newValue):
    G12=H12=I12=I22=G32=H32=I32=Z11=Z12=Z13=Z23=Z31=Z32=Z33=0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: DI (32) 110 VAC (0-5000)':
        colMapping = {'Red_NIS': 'G12', 'Future_Red_NIS': 'H12', 'Non_Red_NIS': 'I12'}
    elif IO_Type == 'Series-C: DI (32) 110 VAC PROX (0-5000)':
        colMapping = {'Non_Red_NIS': 'I22'}
    elif IO_Type == 'Series-C: DI (32) 220 VAC (0-5000)':
        colMapping = {'Red_NIS': 'G32', 'Future_Red_NIS': 'H32', 'Non_Red_NIS': 'I32'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts40972(Product, parts_dict):
    paramDict = dict()
    paramDict['Z11'] = divideByX(Product, 'SerC_IO_Params', ['G12'], 32.0)
    paramDict['Z12'] = divideByX(Product, 'SerC_IO_Params', ['H12'], 32.0)
    paramDict['Z13'] = divideByX(Product, 'SerC_IO_Params', ['I12'], 32.0)
    paramDict['Z23'] = divideByX(Product, 'SerC_IO_Params', ['I22'], 32.0)
    paramDict['Z31'] = divideByX(Product, 'SerC_IO_Params', ['G32'], 32.0)
    paramDict['Z32'] = divideByX(Product, 'SerC_IO_Params', ['H32'], 32.0)
    paramDict['Z33'] =  divideByX(Product, 'SerC_IO_Params', ['I32'], 32.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PDIH01'] = 2 *(paramDict['Z11']) + paramDict['Z12'] + paramDict['Z13'] + paramDict['Z23'] + 2 *(paramDict['Z31'])+  paramDict['Z32']+ paramDict['Z33']
    parts_dict['CC-TDI120'] =paramDict['Z11']+paramDict['Z12']
    parts_dict['CC-TDI230'] = paramDict['Z31']+paramDict['Z32']
    parts_dict['CC-TDI110'] = paramDict['Z13']
    parts_dict['CC-TDI151'] = paramDict['Z23']
    parts_dict['CC-TDI220'] = paramDict['Z33']
    return parts_dict

#CXCPQ-41229  (#Newly Added)
def calcIOModule41229(Product, IO_Type, changedColumn, newValue):
    G41 = H41 = I41 = G42 = H42 = I42 = G43 = H43 = I43 = G44 = H44 = I44 = GG61 = HH61 = II61 = 0
    G51 = H51 = I51 = G52 = H52 = I52 = G53 = H53 = I53 = G54 = H54 = I54 = GG71 = HH71 = II71 = 0
    G64 = H64 = I64 = 0
    G74 = H74 = I74 = 0
    P31 = Q31 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)':
        colMapping = {'Red_IS': 'G41', 'Future_Red_IS': 'H41', 'Non_Red_IS': 'I41', 'Red_NIS': 'G42', 'Future_Red_NIS': 'H42', 'Non_Red_NIS': 'I42', 'Red_ISLTR': 'G43', 'Future_Red_ISLTR': 'H43',  'Non_Red_ISLTR': 'I43', 'Red_RLY': 'G44', 'Future_Red_RLY': 'H44', 'Non_Red_RLY': 'I44' , 'Red_HV_RLY':'GG61', 'Future_Red_HV_RLY':'HH61', 'Non_Red_HV_RLY':'II61'}
    elif IO_Type == 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)':
        colMapping = {'Red_IS': 'G51', 'Future_Red_IS': 'H51', 'Non_Red_IS': 'I51', 'Red_NIS': 'G52', 'Future_Red_NIS': 'H52', 'Non_Red_NIS': 'I52', 'Red_ISLTR': 'G53', 'Future_Red_ISLTR': 'H53',  'Non_Red_ISLTR': 'I53', 'Red_RLY': 'G54', 'Future_Red_RLY': 'H54', 'Non_Red_RLY': 'I54', 'Red_HV_RLY':'GG71', 'Future_Red_HV_RLY':'HH71', 'Non_Red_HV_RLY':'II71'}
    elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)':
        colMapping = {'Red_RLY': 'G64', 'Future_Red_RLY': 'H64', 'Non_Red_RLY': 'I64'}
    elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)':
        colMapping = {'Red_RLY': 'G74', 'Future_Red_RLY': 'H74', 'Non_Red_RLY': 'I74'}
    elif IO_Type == 'Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)':
        colMapping = {'Red_IS': 'P31', 'Future_Red_IS': 'Q31'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


def getParts41229(Product, parts_dict):
    paramDict = dict()
    paramDict['Z41'] = divideByX(Product, 'SerC_IO_Params', ['G41', 'G42', 'G43', 'G44', 'GG61'], 32.0)
    paramDict['Z42'] = divideByX(Product, 'SerC_IO_Params', ['H41', 'H42', 'H43', 'H44', 'HH61'], 32.0)
    paramDict['Z43'] = divideByX(Product, 'SerC_IO_Params', ['I41', 'I42', 'I43', 'I44', 'II61'], 32.0)
    paramDict['Z51'] = divideByX(Product, 'SerC_IO_Params', ['G51', 'G52', 'G53', 'G54', 'GG71'], 32.0)
    paramDict['Z52'] = divideByX(Product, 'SerC_IO_Params', ['H51', 'H52', 'H53', 'H54', 'HH71'], 32.0)
    paramDict['Z53'] = divideByX(Product, 'SerC_IO_Params', ['I51', 'I52', 'I53', 'I54', 'II71'], 32.0)
    paramDict['Z61'] =  divideByX(Product, 'SerC_IO_Params', ['G64'], 32.0)
    paramDict['Z62'] =  divideByX(Product, 'SerC_IO_Params', ['H64'], 32.0)
    paramDict['Z63'] =  divideByX(Product, 'SerC_IO_Params', ['I64'], 32.0)
    paramDict['Z71'] =  divideByX(Product, 'SerC_IO_Params', ['G74'], 32.0)
    paramDict['Z72'] =  divideByX(Product, 'SerC_IO_Params', ['H74'], 32.0)
    paramDict['Z73'] =  divideByX(Product, 'SerC_IO_Params', ['I74'], 32.0)
    paramDict['V91'] =  divideByX(Product, 'SerC_IO_Params', ['P31'], 32.0)
    paramDict['V92'] =  divideByX(Product, 'SerC_IO_Params', ['Q31'], 32.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PDOB01'] =  (2 *(paramDict['Z41'] + paramDict['Z51'] + paramDict['Z61'] + paramDict['Z71'])) + (paramDict['Z42'] + paramDict['Z43'] + paramDict['Z52'] + paramDict['Z53'] + paramDict['Z62'] + paramDict['Z63'] + paramDict['Z72'] + paramDict['Z73']) + (2*(paramDict['V91'])) + paramDict['V92']
    parts_dict['CC-TDOB11'] = paramDict['Z41'] + paramDict['Z42'] + paramDict['Z51'] + paramDict['Z52']
    parts_dict['CC-TDOB01'] = paramDict['Z43'] + paramDict['Z53']
    parts_dict['CC-TDOR11'] = paramDict['Z61'] + paramDict['Z62'] + paramDict['Z71'] + paramDict['Z72']
    parts_dict['CC-TDOR01'] = paramDict['Z63'] + paramDict['Z73']
    parts_dict['CC-GDOL11'] = paramDict['V91'] + paramDict['V92']
    return parts_dict

#CXCPQ-41449
def calcIOModule41449(Product, IO_Type, changedColumn, newValue):
    G81=H81=G82=H82=G83=H83=G91=H91=G92=H92=G93=H93=J11=K11=J12=K12=J13=K13=0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'Series-C: Pulse Input (8) Single Channel (0-5000)':
        colMapping = {'Red_IS': 'G81', 'Future_Red_IS': 'H81', 'Red_NIS': 'G82', 'Future_Red_NIS': 'H82', 'Red_ISLTR': 'G83', 'Future_Red_ISLTR': 'H83'}
    elif IO_Type == 'Series-C: Pulse Input (4) Dual Channel (0-5000)':
        colMapping = {'Red_IS': 'G91', 'Future_Red_IS': 'H91', 'Red_NIS': 'G92', 'Future_Red_NIS': 'H92', 'Red_ISLTR': 'G93', 'Future_Red_ISLTR': 'H93'}
    elif IO_Type == 'Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)':
        colMapping = {'Red_IS': 'J11', 'Future_Red_IS': 'K11', 'Red_NIS': 'J12', 'Future_Red_NIS': 'K12', 'Red_ISLTR': 'J13', 'Future_Red_ISLTR': 'K13'}
    locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
    GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts41449(Product, parts_dict):
    G81 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G81')
    G82 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G82')
    G83 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G83')
    G91 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G91')
    G92 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G92')
    G93 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G93')
    H81 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H81')
    H82 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H82')
    H83 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H83')
    H91 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H91')
    H92 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H92')
    H93 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H93')
    J11 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J11')
    J12 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J12')
    J13 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J13')
    K11 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K11')
    K12 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K12')
    K13 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K13')
    paramDict = dict()
    paramDict['Z81']=max(D.Ceiling((G81+G91*2+J11)/8),D.Ceiling(J11/2))
    paramDict['Z82']=max(D.Ceiling((G82+G92*2+J12)/8),D.Ceiling(J12/2))
    paramDict['Z83']=max(D.Ceiling((G83+G93*2+J13)/8),D.Ceiling(J13/2))
    paramDict['Z84']=max(D.Ceiling((H81+H91*2+K11)/8),D.Ceiling(K11/2))
    paramDict['Z85']=max(D.Ceiling((H82+H92*2+K12)/8),D.Ceiling(K12/2))
    paramDict['Z86']=max(D.Ceiling((H83+H93*2+K13)/8),D.Ceiling(K13/2))
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    Trace.Write("TotalLoad Called getParts41449")
    parts_dict['CC-PPIX01']=(2*(paramDict['Z81']+paramDict['Z82']+paramDict['Z83'])) + (paramDict['Z84']+ paramDict['Z85']+ paramDict['Z86'])
    parts_dict['CC-TPIX11']= paramDict['Z81']+ paramDict['Z82']+ paramDict['Z83']+ paramDict['Z84']+ paramDict['Z85']+ paramDict['Z86']
    return parts_dict

#CXCPQ-44474
def calcIOModule44474(Product, IO_Type, changedColumn, newValue):
    I12 = I32 = 0
    colMapping = dict()
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ["Series-C Control Group","R2Q Series-C Control Group"] else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'SCM: DI (32) 110 VAC (0-5000)':
        colMapping = {'Non_Red_NIS': 'I12'}
    elif IO_Type == 'SCM: DI (32) 220 VAC (0-5000)':
        colMapping = {'Non_Red_NIS': 'I32'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


def getParts44474(Product, parts_dict):
    paramDict = dict()
    paramDict['Z13'] = divideByX(Product, 'SerC_IO_Params', ['I12'], 32.0)
    paramDict['Z33'] = divideByX(Product, 'SerC_IO_Params', ['I32'], 32.0)
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PDIH01']= paramDict['Z13'] + paramDict['Z33']
    parts_dict['DC-TDI110']= paramDict['Z13']
    parts_dict['DC-TDI220']= paramDict['Z33']
    return parts_dict