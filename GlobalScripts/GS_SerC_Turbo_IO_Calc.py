from GS_C300_IO_Calc import getFloat, percentInstalledSpareCalc, divideByX, setIOCount, roundUp
import GS_Get_Set_AtvQty

def updateTurboIOParam(Product, cont, iOType, column, module):
    for row in cont.Rows:
        if row['IO_Type'] in iOType:
            for changedColumn in column:
                newValue = getFloat(row[changedColumn])
                if newValue >= 0:
                    if module in ['49225', '49225_1']:
                        calcIOModule49225(Product, row['IO_Type'], changedColumn, newValue)
                    elif module == '49227':
                        calcIOModule49227(Product, row['IO_Type'], changedColumn, newValue)
                    elif module in ['49229', '49229_1']:
                        calcIOModule49229(Product, row['IO_Type'], changedColumn, newValue)
                    elif module == '49231':
                        calcIOModule49231(Product, row['IO_Type'], changedColumn, newValue)
                    elif module in ['49233', '49233_1']:
                        calcIOModule49233(Product, row['IO_Type'], changedColumn, newValue)
                    elif module == '50461':
                        calcIOModule50461(Product, row['IO_Type'], changedColumn, newValue)
                    elif module in ['50463', '50463_1']:
                        calcIOModule50463(Product, row['IO_Type'], changedColumn, newValue)
                    elif module in ['49228', '49228_1']:
                        calcIOModule49228(Product, row['IO_Type'], changedColumn, newValue)

def applyPercentageOnTurboIOs(Product, percentInstalledSpare, modules, contList, iOType, column):
    if percentInstalledSpare >= 0:
        if '49225' in modules and '49225' in contList.keys():
            cont = Product.GetContainerByName(contList['49225'])
            updateTurboIOParam(Product, cont, iOType['49225'], column['49225'], '49225')
        if '49225_1' in modules and '49225_1' in contList.keys():
            cont = Product.GetContainerByName(contList['49225_1'])
            updateTurboIOParam(Product, cont, iOType['49225_1'], column['49225_1'], '49225_1')
        if '49227' in modules and '49227' in contList.keys():
            cont = Product.GetContainerByName(contList['49227'])
            updateTurboIOParam(Product, cont, iOType['49227'], column['49227'], '49227')
        if '49229' in modules and '49229' in contList.keys():
            cont = Product.GetContainerByName(contList['49229'])
            updateTurboIOParam(Product, cont, iOType['49229'], column['49229'], '49229')
            cont1 = Product.GetContainerByName(contList['49229_1'])
            updateTurboIOParam(Product, cont1, iOType['49229_1'], column['49229_1'], '49229_1')
        if '49231' in modules and '49231' in contList.keys():
            cont = Product.GetContainerByName(contList['49231'])
            updateTurboIOParam(Product, cont, iOType['49231'], column['49231'], '49231')
        if '49233' in modules and '49233' in contList.keys():
            cont = Product.GetContainerByName(contList['49233'])
            updateTurboIOParam(Product, cont, iOType['49233'], column['49233'], '49233')
            cont1 = Product.GetContainerByName(contList['49233_1'])
            updateTurboIOParam(Product, cont1, iOType['49233_1'], column['49233_1'], '49233_1')
        if '50461' in modules and '50461' in contList.keys():
            cont = Product.GetContainerByName(contList['50461'])
            updateTurboIOParam(Product, cont, iOType['50461'], column['50461'], '50461')
        if '50463' in modules and '50463' in contList.keys():
            cont = Product.GetContainerByName(contList['50463'])
            updateTurboIOParam(Product, cont, iOType['50463'], column['50463'], '50463')
            cont1 = Product.GetContainerByName(contList['50463_1'])
            updateTurboIOParam(Product, cont1, iOType['50463_1'], column['50463_1'], '50463_1')
        if '49228' in modules and '49228' in contList.keys():
            cont = Product.GetContainerByName(contList['49228'])
            updateTurboIOParam(Product, cont, iOType['49228'], column['49228'], '49228')
            cont1 = Product.GetContainerByName(contList['49228_1'])
            updateTurboIOParam(Product, cont1, iOType['49228_1'], column['49228_1'], '49228_1')

#CXCPQ-49225
def calcIOModule49225(Product, IO_Type, changedColumn, newValue):
    D81 = E81 = F81 = D82 = E82 = F82 = D83 = E83 = F83 = D84 = E84 = F84 = 0
    D91 = E91 = F91 = D92 = E92 = F92 = D93 = E93 = F93 = D94 = E94 = F94 = 0
    O41 = M51 = N51 = M61 = N61 = O71 = O81 = M91 = N91 = P11 = Q11 = R21 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)':
        colMapping = {'Red_IS': 'D81', 'Future_Red_IS': 'E81', 'Non_Red_IS': 'F81', 'Red_NIS': 'D82', 'Future_Red_NIS': 'E82', 'Non_Red_NIS': 'F82', 'Red_ISLTR': 'D83', 'Future_Red_ISLTR': 'E83',  'Non_Red_ISLTR': 'F83',  'Red_RLY': 'D84',  'Future_Red_RLY': 'E84',  'Non_Red_RLY': 'F84'}
    elif IO_Type == 'Series-C: DI (32) 24VDC SOE (0-5000)':
        colMapping = {'Red_IS': 'D91', 'Future_Red_IS': 'E91', 'Non_Red_IS': 'F91', 'Red_NIS': 'D92', 'Future_Red_NIS': 'E92', 'Non_Red_NIS': 'F92', 'Red_ISLTR': 'D93', 'Future_Red_ISLTR': 'E93',  'Non_Red_ISLTR': 'F93',  'Red_RLY': 'D94',  'Future_Red_RLY': 'E94',  'Non_Red_RLY': 'F94'}
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
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts49225(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    paramDict['Y81'] = divideByX(Product, AttrName, ['D81', 'D82', 'D83', 'D84'], 32.0)
    paramDict['Y82'] = divideByX(Product, AttrName, ['E81', 'E82', 'E83', 'E84'], 32.0)
    paramDict['Y83'] = divideByX(Product, AttrName, ['F81', 'F82', 'F83', 'F84'], 32.0)
    paramDict['Y91'] = divideByX(Product, AttrName, ['D91', 'D92', 'D93', 'D94'], 32.0)
    paramDict['Y92'] = divideByX(Product, AttrName, ['E91', 'E92', 'E93', 'E94'], 32.0)
    paramDict['Y93'] = divideByX(Product, AttrName, ['F91', 'F92', 'F93', 'F94'], 32.0)
    paramDict['V13'] = divideByX(Product, AttrName, ['O41'], 32.0)
    paramDict['V21'] = divideByX(Product, AttrName, ['M51'], 32.0)
    paramDict['V22'] = divideByX(Product, AttrName, ['N51'], 32.0)
    paramDict['V31'] = divideByX(Product, AttrName, ['M61'], 32.0)
    paramDict['V32'] = divideByX(Product, AttrName, ['N61'], 32.0)
    paramDict['V43'] = divideByX(Product, AttrName, ['O71'], 32.0)
    paramDict['V53'] = divideByX(Product, AttrName, ['O81'], 32.0)
    paramDict['V61'] = divideByX(Product, AttrName, ['M91'], 32.0)
    paramDict['V62'] = divideByX(Product, AttrName, ['N91'], 32.0)
    paramDict['V71'] = divideByX(Product, AttrName, ['P11'], 32.0)
    paramDict['V72'] = divideByX(Product, AttrName, ['Q11'], 32.0)
    paramDict['V83'] = divideByX(Product, AttrName, ['R21'], 32.0)
    setIOCount(Product, AttrName, paramDict)
    parts_dict['CC-PDIL01'] = 2 *(paramDict['Y81']) + paramDict['Y82'] + paramDict['Y83'] + (2*(paramDict['V21'] + paramDict['V31'])) + (paramDict['V13'] + paramDict['V22'] + paramDict['V32'] + paramDict['V43'])
    parts_dict['CC-PDIS01'] = 2 *(paramDict['Y91']) + paramDict['Y92'] + paramDict['Y93'] + (2*(paramDict['V61'] + paramDict['V71'])) + (paramDict['V53'] + paramDict['V62'] + paramDict['V72'] + paramDict['V83'])
    parts_dict['CC-TDIL11'] = paramDict['Y81'] + paramDict['Y82'] + paramDict['Y91'] + paramDict['Y92']
    parts_dict['CC-TDIL01'] = paramDict['Y83'] + paramDict['Y93']
    return parts_dict

#CXCPQ-49227
def calcIOModule49227(Product, IO_Type, changedColumn, newValue):
    A11 = A21 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Number of Servo Position Modules (0-480)':
        colMapping = {'Red_IOM': 'A11'}
    elif IO_Type == 'Number of Speed Protection Modules (0-480)':
        colMapping = {'Red_IOM': 'A21'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts49227(Product, parts_dict):
    AttrName = 'SerC_IO_Params'
    A11 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'A11')
    A21 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'A21')
    parts_dict['CC-PSV201'] = 2 * A11
    parts_dict['CC-PSP401'] = 2 * A21
    parts_dict['CC-TSV211'] = A11
    parts_dict['CC-TSP411'] = A21
    return parts_dict

#CXCPQ-49229
def calcIOModule49229(Product, IO_Type, changedColumn, newValue):
    D21 = E21 = F21 = D22 = E22 = F22 = D23 = E23 = F23 = 0
    D31 = E31 = F31 = D32 = E32 = F32 = D33 = E33 = F33 = 0
    L21 = J31 = K31 = J41 = K41 = J51 = K51 = L61 = J71 = K71 = J81 = K81 = J91 = K91 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
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
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


def getParts49229(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    paramDict['Y21'] = divideByX(Product, AttrName, ['D21', 'D22', 'D23'], 16.0)
    paramDict['Y22'] = divideByX(Product, AttrName, ['E21', 'E22', 'E23'], 16.0)
    paramDict['Y23'] = divideByX(Product, AttrName, ['F21', 'F22', 'F23'], 16.0)
    paramDict['Y31'] = divideByX(Product, AttrName, ['D31', 'D32', 'D33'], 16.0)
    paramDict['Y32'] = divideByX(Product, AttrName, ['E31', 'E32', 'E33'], 16.0)
    paramDict['Y33'] = divideByX(Product, AttrName, ['F31', 'F32', 'F33'], 16.0)
    paramDict['Z91'] = divideByX(Product, AttrName, ['L21'], 16.0)
    paramDict['W11'] = divideByX(Product, AttrName, ['J31'], 16.0)
    paramDict['W12'] = divideByX(Product, AttrName, ['K31'], 16.0)
    paramDict['W21'] = divideByX(Product, AttrName, ['J41'], 16.0)
    paramDict['W22'] = divideByX(Product, AttrName, ['K41'], 16.0)
    paramDict['W31'] = divideByX(Product, AttrName, ['J51'], 16.0)
    paramDict['W32'] = divideByX(Product, AttrName, ['K51'], 16.0)
    paramDict['W23'] = divideByX(Product, AttrName, ['L61'], 16.0)
    paramDict['W41'] = divideByX(Product, AttrName, ['J71'], 16.0)
    paramDict['W42'] = divideByX(Product, AttrName, ['K71'], 16.0)
    paramDict['W51'] = divideByX(Product, AttrName, ['J81'], 16.0)
    paramDict['W52'] = divideByX(Product, AttrName, ['K81'], 16.0)
    paramDict['W61'] = divideByX(Product, AttrName, ['J91'], 16.0)
    paramDict['W62'] = divideByX(Product, AttrName, ['K91'], 16.0)
    setIOCount(Product, AttrName, paramDict)
    parts_dict['CC-PAIH02'] = 2 *(paramDict['Y21']) + paramDict['Y22'] + paramDict['Y23'] + (2*(paramDict['W11'] + paramDict['W21'] + paramDict['W31'])) + (paramDict['W12'] + paramDict['W22'] + paramDict['W32'] + paramDict['Z91'])
    parts_dict['CC-PAIX02'] = 2 *(paramDict['Y31']) + paramDict['Y32'] + paramDict['Y33'] + (2*(paramDict['W41'] + paramDict['W51'] + paramDict['W61'])) + (paramDict['W42'] + paramDict['W52'] + paramDict['W62'] + paramDict['W23'])
    return parts_dict

#CXCPQ-49230
def getParts49230(Product, parts_dict):
    AttrName = 'SerC_IO_Params'
    Y21 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Y21')
    Y22 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Y22')
    Y23 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Y23')
    Y31 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Y31')
    Y32 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Y32')
    Y33 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Y33')
    W11 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W11')
    Z91 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'Z91')
    W21 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W21')
    W31 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W31')
    W12 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W12')
    W22 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W22')
    W23 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W23')
    W32 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W32')
    W41 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W41')
    W51 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W51')
    W61 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W61')
    W42 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W42')
    W52 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W52')
    W62 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'W62')
    parts_dict['CC-TAID11'] = Y21 + Y22+ Y31 + Y32
    parts_dict['CC-TAID01'] = Y23 + Y33
    parts_dict['CC-GAIX11'] = (W11 + W21 + W31) + (W12 + W22 + W32) + (W41 + W51 + W61) + (W42 + W52 + W62)
    parts_dict['CC-GAIX21'] = Z91 + W23
    return parts_dict

#CXCPQ-49231
def calcIOModule49231(Product, IO_Type, changedColumn, newValue):
    F41 = F42 = F43 = F51 = F52 = F53 = F61 = F62 = F63 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Series-C: LLAI (1) Mux RTD (0-5000)':
        colMapping = {'Non_Red_IS': 'F41', 'Non_Red_NIS': 'F42', 'Non_Red_ISLTR': 'F43'}
    elif IO_Type == 'Series-C: LLAI (1) Mux TC (0-5000)':
        colMapping = {'Non_Red_IS': 'F51', 'Non_Red_NIS': 'F52', 'Non_Red_ISLTR': 'F53'}
    elif IO_Type == 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)':
        colMapping = {'Non_Red_IS': 'F61', 'Non_Red_NIS': 'F62', 'Non_Red_ISLTR': 'F63'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts49231(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    paramDict['Y43'] = divideByX(Product, AttrName, ['F41', 'F42', 'F43'], 64.0)
    paramDict['Y53'] = divideByX(Product, AttrName, ['F51', 'F52', 'F53'], 64.0)
    paramDict['Y63'] = divideByX(Product, AttrName, ['F61', 'F62', 'F63'], 64.0)
    setIOCount(Product, AttrName, paramDict)
    qty = paramDict['Y43'] + paramDict['Y53'] + paramDict['Y63']
    parts_dict['CC-PAIM01'] = qty
    parts_dict['CC-TAIM01'] = qty
    return parts_dict

#CXCPQ-49232
def getParts49232(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    parts_dict['MC-TAMR04'] = divideByX(Product, AttrName, ['F41', 'F42', 'F43'], 16.0)
    parts_dict['MC-TAMT04'] = divideByX(Product, AttrName, ['F51', 'F52', 'F53'], 16.0)
    parts_dict['MC-TAMT14'] = divideByX(Product, AttrName, ['F61', 'F62', 'F63'], 16.0)
    parts_dict['MU-KLAM03'] = parts_dict['MC-TAMR04'] + parts_dict['MC-TAMT04'] + parts_dict['MC-TAMT14']
    #The below part number has been removed as per the user story CXCPQ-57396
    ##parts_dict['MU-TMCN01'] = roundUp((parts_dict['MC-TAMR04'] + parts_dict['MC-TAMT04'] + parts_dict['MC-TAMT14'])/3.0)
    return parts_dict

#CXCPQ-49233
def calcIOModule49233(Product, IO_Type, changedColumn, newValue):
    D71 = E71 = F71 = D72 = E72 = F72 = D73 = E73 = F73 = 0
    O11 = M21 = N21 = M31 = N31 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Series-C: AO (16) HART (0-5000)':
        colMapping = {'Red_IS': 'D71', 'Future_Red_IS': 'E71', 'Non_Red_IS': 'F71', 'Red_NIS': 'D72', 'Future_Red_NIS': 'E72', 'Non_Red_NIS': 'F72', 'Red_ISLTR': 'D73', 'Future_Red_ISLTR': 'E73',  'Non_Red_ISLTR': 'F73'}
    elif IO_Type == 'Series-C: GI/IS AO (16) HART (0-5000)':
        colMapping = {'Non_Red_IS': 'O11'}
    elif IO_Type == 'Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'M21', 'Future_Red_IS': 'N21'}
    elif IO_Type == 'Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)':
        colMapping = {'Red_IS': 'M31', 'Future_Red_IS': 'N31'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts49233(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    paramDict['Y71'] = divideByX(Product, AttrName, ['D71', 'D72', 'D73'], 16.0)
    paramDict['Y72'] = divideByX(Product, AttrName, ['E71', 'E72', 'E73'], 16.0)
    paramDict['Y73'] = divideByX(Product, AttrName, ['F71', 'F72', 'F73'], 16.0)
    paramDict['W73'] = divideByX(Product, AttrName, ['O11'], 16.0)
    paramDict['W81'] = divideByX(Product, AttrName, ['M21'], 16.0)
    paramDict['W82'] = divideByX(Product, AttrName, ['N21'], 16.0)
    paramDict['W91'] = divideByX(Product, AttrName, ['M31'], 16.0)
    paramDict['W92'] = divideByX(Product, AttrName, ['N31'], 16.0)
    setIOCount(Product, AttrName, paramDict)
    parts_dict['CC-PAOH01'] = 2 *(paramDict['Y71']) + paramDict['Y72'] + paramDict['Y73'] + (2*(paramDict['W81'] + paramDict['W91'])) + (paramDict['W82'] + paramDict['W92'] + paramDict['W73'])
    parts_dict['CC-TAOX11'] = paramDict['Y71'] + paramDict['Y72']
    parts_dict['CC-TAOX01'] = paramDict['Y73']
    return parts_dict

#CXCPQ-50461
def calcIOModule50461(Product, IO_Type, changedColumn, newValue):
    G12 = H12 = I12 = I22 = G32 = H32 = I32 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Series-C: DI (32) 110 VAC (0-5000)':
        colMapping = {'Red_NIS': 'G12', 'Future_Red_NIS': 'H12', 'Non_Red_NIS': 'I12'}
    elif IO_Type == 'Series-C: DI (32) 110 VAC PROX (0-5000)':
        colMapping = {'Non_Red_NIS': 'I22'}
    elif IO_Type == 'Series-C: DI (32) 220 VAC (0-5000)':
        colMapping = {'Red_NIS': 'G32', 'Future_Red_NIS': 'H32', 'Non_Red_NIS': 'I32'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts50461(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    paramDict['Z11'] = divideByX(Product, AttrName, ['G12'], 32.0)
    paramDict['Z12'] = divideByX(Product, AttrName, ['H12'], 32.0)
    paramDict['Z13'] = divideByX(Product, AttrName, ['I12'], 32.0)
    paramDict['Z23'] = divideByX(Product, AttrName, ['I22'], 32.0)
    paramDict['Z31'] = divideByX(Product, AttrName, ['G32'], 32.0)
    paramDict['Z32'] = divideByX(Product, AttrName, ['H32'], 32.0)
    paramDict['Z33'] = divideByX(Product, AttrName, ['I32'], 32.0)
    setIOCount(Product, AttrName, paramDict)
    parts_dict['CC-PDIH01'] = 2 *(paramDict['Z11']) + paramDict['Z12'] + paramDict['Z13'] + paramDict['Z23'] + 2 *(paramDict['Z31']) +  paramDict['Z32'] + paramDict['Z33']
    parts_dict['CC-TDI120'] = paramDict['Z11'] + paramDict['Z12']
    parts_dict['CC-TDI230'] = paramDict['Z31'] + paramDict['Z32']
    parts_dict['CC-TDI110'] = paramDict['Z13']
    parts_dict['CC-TDI151'] = paramDict['Z23']
    parts_dict['CC-TDI220'] = paramDict['Z33']
    return parts_dict

#CXCPQ-50463
def calcIOModule50463(Product, IO_Type, changedColumn, newValue):
    G41 = H41 = I41 = G42 = H42 = I42 = G43 = H43 = I43 = G44 = H44 = I44 = 0
    G51 = H51 = I51 = G52 = H52 = I52 = G53 = H53 = I53 = G54 = H54 = I54 = 0
    G64 = H64 = I64 = 0
    G74 = H74 = I74 = 0
    P31 = Q31 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)':
        colMapping = {'Red_IS': 'G41', 'Future_Red_IS': 'H41', 'Non_Red_IS': 'I41', 'Red_NIS': 'G42', 'Future_Red_NIS': 'H42', 'Non_Red_NIS': 'I42', 'Red_ISLTR': 'G43', 'Future_Red_ISLTR': 'H43',  'Non_Red_ISLTR': 'I43', 'Red_RLY': 'G44', 'Future_Red_RLY': 'H44', 'Non_Red_RLY': 'I44'}
    elif IO_Type == 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)':
        colMapping = {'Red_IS': 'G51', 'Future_Red_IS': 'H51', 'Non_Red_IS': 'I51', 'Red_NIS': 'G52', 'Future_Red_NIS': 'H52', 'Non_Red_NIS': 'I52', 'Red_ISLTR': 'G53', 'Future_Red_ISLTR': 'H53',  'Non_Red_ISLTR': 'I53', 'Red_RLY': 'G54', 'Future_Red_RLY': 'H54', 'Non_Red_RLY': 'I54'}
    elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)':
        colMapping = {'Red_RLY': 'G64', 'Future_Red_RLY': 'H64', 'Non_Red_RLY': 'I64'}
    elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)':
        colMapping = {'Red_RLY': 'G74', 'Future_Red_RLY': 'H74', 'Non_Red_RLY': 'I74'}
    elif IO_Type == 'Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)':
        colMapping = {'Red_IS': 'P31', 'Future_Red_IS': 'Q31'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

def getParts50463(Product, parts_dict):
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    paramDict['Z41'] = divideByX(Product, AttrName, ['G41', 'G42', 'G43', 'G44'], 32.0)
    paramDict['Z42'] = divideByX(Product, AttrName, ['H41', 'H42', 'H43', 'H44'], 32.0)
    paramDict['Z43'] = divideByX(Product, AttrName, ['I41', 'I42', 'I43', 'I44'], 32.0)
    paramDict['Z51'] = divideByX(Product, AttrName, ['G51', 'G52', 'G53', 'G54'], 32.0)
    paramDict['Z52'] = divideByX(Product, AttrName, ['H51', 'H52', 'H53', 'H54'], 32.0)
    paramDict['Z53'] = divideByX(Product, AttrName, ['I51', 'I52', 'I53', 'I54'], 32.0)
    paramDict['Z61'] = divideByX(Product, AttrName, ['G64'], 32.0)
    paramDict['Z62'] = divideByX(Product, AttrName, ['H64'], 32.0)
    paramDict['Z63'] = divideByX(Product, AttrName, ['I64'], 32.0)
    paramDict['Z71'] = divideByX(Product, AttrName, ['G74'], 32.0)
    paramDict['Z72'] = divideByX(Product, AttrName, ['H74'], 32.0)
    paramDict['Z73'] = divideByX(Product, AttrName, ['I74'], 32.0)
    paramDict['V91'] = divideByX(Product, AttrName, ['P31'], 32.0)
    paramDict['V92'] = divideByX(Product, AttrName, ['Q31'], 32.0)
    setIOCount(Product, AttrName, paramDict)
    parts_dict['CC-PDOB01'] =  (2 *(paramDict['Z41'] + paramDict['Z51'] + paramDict['Z61'] + paramDict['Z71'])) + (paramDict['Z42'] + paramDict['Z43'] + paramDict['Z52'] + paramDict['Z53'] + paramDict['Z62'] + paramDict['Z63'] + paramDict['Z72'] + paramDict['Z73']) + (2*(paramDict['V91'])) + paramDict['V92']
    parts_dict['CC-TDOB11'] = paramDict['Z41'] + paramDict['Z42'] + paramDict['Z51'] + paramDict['Z52']
    parts_dict['CC-TDOB01'] = paramDict['Z43'] + paramDict['Z53']
    parts_dict['CC-TDOR11'] = paramDict['Z61'] + paramDict['Z62'] + paramDict['Z71'] + paramDict['Z72']
    parts_dict['CC-TDOR01'] = paramDict['Z63'] + paramDict['Z73']
    #The qty calculation formula has been changed as per the user story CXCPQ-52467
    ##parts_dict['CC-GDOL11'] = 2 *(paramDict['V91'] + paramDict['V92'])
    parts_dict['CC-GDOL11'] = paramDict['V91'] + paramDict['V92']
    return parts_dict

#CXCPQ-49228
def calcIOModule49228(Product, IO_Type, changedColumn, newValue):
    A61 = B61 = C61 = A62 = B62 = C62 = A63 = B63 = C63 = 0
    A73 = B73 = C73 = 0
    A81 = B81 = C81 = A82 = B82 = C82 = A83 = B83 = C83 = 0
    A91 = B91 = C91 = A92 = B92 = C92 = A93 = B93 = C93 = A94 = B94 = C94 = 0
    D11 = E11 = F11 = D12 = E12 = F12 = D13 = E13 = F13 = D14 = E14 = F14 = 0
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name in ("Series-C Control Group","R2Q Series-C Control Group") else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    colMapping = dict()
    if IO_Type == 'Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)':
        colMapping = {'Red_IS': 'A61', 'Future_Red_IS': 'B61', 'Non_Red_IS': 'C61', 'Red_NIS': 'A62', 'Future_Red_NIS': 'B62', 'Non_Red_NIS': 'C62', 'Red_ISLTR': 'A63', 'Future_Red_ISLTR': 'B63',  'Non_Red_ISLTR': 'C63'}
    elif IO_Type == 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)':
        colMapping = {'Red_ISLTR': 'A73', 'Future_Red_ISLTR': 'B73',  'Non_Red_ISLTR': 'C73'}
    elif IO_Type == 'Series-C: UIO (32) Analog Output (0-5000)':
        colMapping = {'Red_IS': 'A81', 'Future_Red_IS': 'B81', 'Non_Red_IS': 'C81', 'Red_NIS': 'A82', 'Future_Red_NIS': 'B82', 'Non_Red_NIS': 'C82', 'Red_ISLTR': 'A83', 'Future_Red_ISLTR': 'B83',  'Non_Red_ISLTR': 'C83'}
    elif IO_Type == 'Series-C: UIO (32) Digital Input (0-5000)':
        colMapping = {'Red_IS': 'A91', 'Future_Red_IS': 'B91', 'Non_Red_IS': 'C91', 'Red_NIS': 'A92', 'Future_Red_NIS': 'B92', 'Non_Red_NIS': 'C92', 'Red_ISLTR': 'A93', 'Future_Red_ISLTR': 'B93',  'Non_Red_ISLTR': 'C93', 'Red_RLY': 'A94', 'Future_Red_RLY': 'B94', 'Non_Red_RLY': 'C94'}
    elif IO_Type == 'Series-C: UIO (32) Digital Output (0-5000)':
        colMapping = {'Red_IS': 'D11', 'Future_Red_IS': 'E11', 'Non_Red_IS': 'F11', 'Red_NIS': 'D12', 'Future_Red_NIS': 'E12', 'Non_Red_NIS': 'F12', 'Red_ISLTR': 'D13', 'Future_Red_ISLTR': 'E13',  'Non_Red_ISLTR': 'F13', 'Red_RLY': 'D14', 'Future_Red_RLY': 'E14', 'Non_Red_RLY': 'F14'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])

#Intermedidate Calculation
def partCalc49228(var1, var2, var3):
    cal1 = roundUp((var1 + var2)/9600.0)
    cal2 = roundUp(var3/32.0)
    return max(cal1, cal2)

def getParts49228(Product, parts_dict):
    A61 = B61 = C61 = A62 = B62 = C62 = A63 = B63 = C63 = 0
    A73 = B73 = C73 = 0
    A81 = B81 = C81 = A82 = B82 = C82 = A83 = B83 = C83 = 0
    A91 = B91 = C91 = A92 = B92 = C92 = A93 = B93 = C93 = A94 = B94 = C94 = 0
    D11 = E11 = F11 = D12 = E12 = F12 = D13 = E13 = F13 = D14 = E14 = F14 = 0
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    averageCurrent = getFloat(Product.Attr('General_Question_Average_current_DO').GetValue())
    paramList = ['A61', 'B61', 'C61', 'A62', 'B62', 'C62', 'A63', 'B63', 'C63']
    paramList.extend(['A73', 'B73', 'C73'])
    paramList.extend(['A81', 'B81', 'C81', 'A82', 'B82', 'C82', 'A83', 'B83', 'C83'])
    paramList.extend(['A91', 'B91', 'C91', 'A92', 'B92', 'C92', 'A93', 'B93', 'C93', 'A94', 'B94', 'C94'])
    paramList.extend(['D11', 'E11', 'F11', 'D12', 'E12', 'F12', 'D13', 'E13', 'F13', 'D14', 'E14', 'F14'])
    #Get attribute value quantity and assigned to local variable 
    for key in paramList:
        locals()[key] = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, key)
    paramDict['X61'] = partCalc49228(((A61 + A81 + A91)* 25),       (D11 * averageCurrent),         (A61 + A81 + A91 + D11))
    paramDict['X62'] = partCalc49228(((A62 + A82 + A92 + A94)* 25), ((D12 + D14) * averageCurrent), (A62 + A82 + A92 + A94 + D12 + D14))
    paramDict['X63'] = partCalc49228(((A63 + A73 + A83 + A93)* 25), (D13 * averageCurrent),         (A63 + A73 + A83 + A93 + D13))
    paramDict['X71'] = partCalc49228(((B61 + B81 + B91)* 25),       (E11 * averageCurrent),         (B61 + B81 + B91 + E11))
    paramDict['X72'] = partCalc49228(((B62 + B82 + B92 + B94)* 25), ((E12 + E14) * averageCurrent), (B62 + B82 + B92 + B94 + E12 + E14))
    paramDict['X73'] = partCalc49228(((B63 + B73 + B83 + B93)* 25), (E13 * averageCurrent),         (B63 + B73 + B83 + B93 + E13))
    paramDict['X81'] = partCalc49228(((C61 + C81 + C91)* 25),       (F11 * averageCurrent),         (C61 + C81 + C91 + F11))
    paramDict['X82'] = partCalc49228(((C62 + C82 + C92 + C94)* 25), ((F12 + F14) * averageCurrent),  (C62 + C82 + C92 + C94 + F12 + F14))
    paramDict['X83'] = partCalc49228(((C63 + C73 + C83 + C93)* 25), (F13 * averageCurrent),         (C63 + C73 + C83 + C93 + F13))
    setIOCount(Product, AttrName, paramDict)
    parts_dict['CC-PUIO31'] = (2 * (paramDict['X61'] + paramDict['X62'] + paramDict['X63']) + (paramDict['X71'] + paramDict['X72'] + paramDict['X73'] + paramDict['X81'] + paramDict['X82'] + paramDict['X83']))
    parts_dict['CC-TUIO41'] = (paramDict['X61'] + paramDict['X62'] + paramDict['X63'])  +  ( paramDict['X71'] + paramDict['X72'] + paramDict['X73'])
    parts_dict['CC-TUIO31'] = paramDict['X81'] + paramDict['X82'] + paramDict['X83']
    return parts_dict