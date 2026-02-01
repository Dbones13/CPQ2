#GS_C300_IO_Calc2
def setAtvQty(Product,AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=False
            av.Quantity = 0
            if int(qty) > 0:
                av.IsSelected=True
                av.Quantity=qty
                Trace.Write('Selected ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break


def getAtvQty(Product,AttrName,sv):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            return av.Quantity
    return 0


def setIOCount(Product, AttrName, qtyDict):
    for sv in qtyDict.keys():
        setAtvQty(Product, AttrName, sv, qtyDict[sv])


def getIOCount(Product, AttrName, params):
    resDict = dict()
    for sv in params:
        resDict[sv] = getAtvQty(Product, AttrName, sv)
    return resDict


def getFloat(val):
    if val:
        return float(val)
    return 0.00


def roundUp(n):
    res = int(n)
    return res if res == n else res+1


def percentInstalledSpareCalc(Product, AttrName, IO_Count):
    percentInstalledSpare = Product.Attr(AttrName).GetValue()
    if IO_Count > 0:
        return roundUp(getFloat(IO_Count * (1 + (getFloat(percentInstalledSpare) * 0.01))))
    else:
        return 0


def divideByX(Product, AttrName, paramList, X):
    res = 0
    if X == 0:
        return res
    resDict = getIOCount(Product, AttrName, paramList)
    for key in resDict.keys():
        if resDict[key] > 0:
            res += roundUp(getFloat(resDict[key]/X))
    return res

#CXCPQ-44488
def calcIOModule44488(Product, IO_Type, changedColumn, newValue):
    G41 = H41 = I41 = G42 = H42 = I42 = G43 = H43 = I43 = G44 = H44 = I44 = 0
    G51 = H51 = I51 = G52 = H52 = I52 = G53 = H53 = I53 = G54 = H54 = I54 = 0
    G64 = H64 = I64 = 0
    G74 = H74 = I74 = 0
    S81=T82=U83=S91=T92=U93=0
    colMapping = dict()
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name == "Series-C Control Group" else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'SCM: DO (32) 24VDC Bus External Power Supply (0-5000)':
        colMapping = {'Red_IS': 'G41', 'Future_Red_IS': 'H41', 'Non_Red_IS': 'I41', 'Red_NIS': 'G42', 'Future_Red_NIS': 'H42', 'Non_Red_NIS': 'I42', 'Red_ISLTR': 'G43', 'Future_Red_ISLTR': 'H43',  'Non_Red_ISLTR': 'I43', 'Red_RLY': 'G44', 'Future_Red_RLY': 'H44', 'Non_Red_RLY': 'I44', 'Red_HV_Rly':'S81', 'Future_HV_Rly':'T82', 'Non_Red_HV_Rly':'U83'}
    elif IO_Type == 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)':
        colMapping = {'Red_IS': 'G51', 'Future_Red_IS': 'H51', 'Non_Red_IS': 'I51', 'Red_NIS': 'G52', 'Future_Red_NIS': 'H52', 'Non_Red_NIS': 'I52', 'Red_ISLTR': 'G53', 'Future_Red_ISLTR': 'H53',  'Non_Red_ISLTR': 'I53', 'Red_RLY': 'G54', 'Future_Red_RLY': 'H54', 'Non_Red_RLY': 'I54', 'Red_HV_Rly':'S91', 'Future_HV_Rly':'T92', 'Non_Red_HV_Rly':'U93'}
    elif IO_Type == 'SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)':
        colMapping = {'Red_RLY': 'G64', 'Future_Red_RLY': 'H64', 'Non_Red_RLY': 'I64'}
    elif IO_Type == 'SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)':
        colMapping = {'Red_RLY': 'G74', 'Future_Red_RLY': 'H74', 'Non_Red_RLY': 'I74'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


def getParts44488(Product, parts_dict):
    valueDict = {'Z41':['G41','G42','G43','G44', 'S81'], 'Z42':['H41','H42','H43','H44', 'T82'], 'Z43':['I41','I42','I43','I44', 'U83'], 'Z51':['G51','G52','G53','G54', 'S91'],
                'Z52':['H51','H52','H53','H54', 'T92'], 'Z53':['I51','I52','I53','I54', 'U93'], 'Z61':['G64'], 'Z62':['H64'], 'Z63':['I64'], 'Z71':['G74'], 'Z72':['H74'], 'Z73':['I74']}
    paramDict = dict()
    for key,val in valueDict.items():
        paramDict[key]=divideByX(Product, 'SerC_IO_Params', val, 32.0)
        
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PDOB01']= 2*(paramDict['Z41'] + paramDict['Z51'] + paramDict['Z61'] + paramDict['Z71']) +  (paramDict['Z42'] + paramDict['Z43'] + paramDict['Z52'] + paramDict['Z53'] + paramDict['Z62'] + paramDict['Z63'] + paramDict['Z72'] + paramDict['Z73'])
    """##Old calculation
    parts_dict['DC-TDOB11']= paramDict['Z41'] + paramDict['Z42'] + paramDict['Z51'] + paramDict['Z52'] + paramDict['Z61'] + paramDict['Z62'] + paramDict['Z71'] + paramDict['Z72']
    parts_dict['DC-TDOB01']= paramDict['Z43'] + paramDict['Z53'] + paramDict['Z63'] + paramDict['Z73']"""
    #New calculation as per the user story CXCPQ-52466
    parts_dict['DC-TDOB11'] = paramDict['Z41'] + paramDict['Z42'] + paramDict['Z51'] + paramDict['Z52']
    parts_dict['DC-TDOB01'] = paramDict['Z43'] + paramDict['Z53']
    parts_dict['DC-TDOR11'] = paramDict['Z61'] + paramDict['Z62'] + paramDict['Z71'] + paramDict['Z72']
    parts_dict['DC-TDOR01'] = paramDict['Z63'] + paramDict['Z73']
    #CXCPQ-44489
    parts_dict = getParts44489(Product, parts_dict)
    return parts_dict

#CXCPQ-44489, CXCPQ-55754
def getParts44489(Product, parts_dict):
    paramDict = getIOCount(Product, 'SerC_IO_Params', ['Z61', 'Z62', 'Z63', 'Z71', 'Z72', 'Z73'])
    part_mapping = {'0.5M':'CC-KREBR5','1M':'CC-KREB01','2M':'CC-KREB02','5M':'CC-KREB05','10M':'CC-KREB10'}
    part_mapping['20M'] = 'CC-KREB20'
    part_mapping['30M'] = 'CC-KREB30'
    part_mapping['40M'] = 'CC-KREB40'
    part_mapping['50M'] = 'CC-KREB50'
    qty = 0
    #set default qty as 0 for all KREB parts
    for kre_part in ['CC-KREBR5', 'CC-KREB01', 'CC-KREB02', 'CC-KREB05', 'CC-KREB10', 'CC-KREB20', 'CC-KREB30', 'CC-KREB40', 'CC-KREB50']:
        parts_dict[kre_part]= qty

    ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    if ioFamilyType == 'Series-C Mark II':
        for key in paramDict.keys():
            qty += paramDict[key]
    parts_dict['CC-SDOR01']= qty

    AttrName = 'SerC_CG_DO_Relay_Extension_Cable_Length' if Product.Name == "Series-C Control Group" else 'SerC_RG_DO_Relay_Extension_Cable_Length'
    Do_Relay = Product.Attr(AttrName).GetValue()
    if Do_Relay in part_mapping.keys():
        part = part_mapping[Do_Relay]
        parts_dict[part]= qty
    return parts_dict

#CXCPQ-44490
def calcIOModule44490(Product, IO_Type, changedColumn, newValue):
    G81 = H81 = G82 = H82 = G83 = H83 = 0
    G91 = H91 = G92 = H92 = G93 = H93 = 0
    J11 = K11 = J12 = K12 = J13 = K13 = 0
    colMapping = dict()
    AttrName = 'SerC_CG_Percent_Installed_Spare' if Product.Name == "Series-C Control Group" else 'SerC_RG_Percent_Installed_Spare(0-100%)'
    if IO_Type == 'SCM: Pulse Input (8) Single Channel (0-5000)':
        colMapping = {'Red_IS': 'G81', 'Future_Red_IS': 'H81', 'Red_NIS': 'G82', 'Future_Red_NIS': 'H82', 'Red_ISLTR': 'G83', 'Future_Red_ISLTR': 'H83'}
    elif IO_Type == 'SCM: Pulse Input (4) Dual Channel (0-5000)':
        colMapping = {'Red_IS': 'G91', 'Future_Red_IS': 'H91', 'Red_NIS': 'G92', 'Future_Red_NIS': 'H92', 'Red_ISLTR': 'G93', 'Future_Red_ISLTR': 'H93'}
    elif IO_Type == 'SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)':
        colMapping = {'Red_IS': 'J11', 'Future_Red_IS': 'K11', 'Red_NIS': 'J12', 'Future_Red_NIS': 'K12', 'Red_ISLTR': 'J13', 'Future_Red_ISLTR': 'K13'}
    if changedColumn in colMapping.keys():
        locals()[colMapping[changedColumn]] = percentInstalledSpareCalc(Product, AttrName, newValue)
        setAtvQty(Product, 'SerC_IO_Params', colMapping[changedColumn], locals()[colMapping[changedColumn]])


#Intermedidate Calculation
def partCalc44490(x, y, z):
    var1 = roundUp((x + (y * 2) + z)/8.0)
    var2 = roundUp(z/2.0)
    return max(var1, var2)

#CXCPQ-44490
def getParts44490(Product, parts_dict):
    paramDict = getIOCount(Product, 'SerC_IO_Params', ['G81', 'H81', 'G82', 'H82', 'G83', 'H83', 'G91', 'H91', 'G92', 'H92', 'G93', 'H93', 'J11', 'K11', 'J12', 'K12', 'J13', 'K13'])
    paramDict['Z81'] = partCalc44490(paramDict['G81'], paramDict['G91'], paramDict['J11'])
    paramDict['Z82'] = partCalc44490(paramDict['G82'], paramDict['G92'], paramDict['J12'])
    paramDict['Z83'] = partCalc44490(paramDict['G83'], paramDict['G93'], paramDict['J13'])
    paramDict['Z84'] = partCalc44490(paramDict['H81'], paramDict['H91'], paramDict['K11'])
    paramDict['Z85'] = partCalc44490(paramDict['H82'], paramDict['H92'], paramDict['K12'])
    paramDict['Z86'] = partCalc44490(paramDict['H83'], paramDict['H93'], paramDict['K13'])
    setIOCount(Product, 'SerC_IO_Params', paramDict)
    parts_dict['CC-PPIX01'] = (2*(paramDict['Z81'] + paramDict['Z82'] + paramDict['Z83'])) + (paramDict['Z84'] + paramDict['Z85'] + paramDict['Z86'])
    parts_dict['DC-TPIX11'] = paramDict['Z81'] + paramDict['Z82'] + paramDict['Z83'] + paramDict['Z84'] + paramDict['Z85'] + paramDict['Z86']
    return parts_dict

def getParams44490(Product):
    paramDict = getIOCount(Product, 'SerC_IO_Params', ['G81', 'H81', 'G82', 'H82', 'G83', 'H83', 'G91', 'H91', 'G92', 'H92', 'G93', 'H93', 'J11', 'K11', 'J12', 'K12', 'J13', 'K13'])
    paramDict['Z81'] = partCalc44490(paramDict['G81'], paramDict['G91'], paramDict['J11'])
    paramDict['Z82'] = partCalc44490(paramDict['G82'], paramDict['G92'], paramDict['J12'])
    paramDict['Z83'] = partCalc44490(paramDict['G83'], paramDict['G93'], paramDict['J13'])
    paramDict['Z84'] = partCalc44490(paramDict['H81'], paramDict['H91'], paramDict['K11'])
    paramDict['Z85'] = partCalc44490(paramDict['H82'], paramDict['H92'], paramDict['K12'])
    paramDict['Z86'] = partCalc44490(paramDict['H83'], paramDict['H93'], paramDict['K13'])
    CC_PPIX01 = (1.02*(paramDict['Z81'] + paramDict['Z82'] + paramDict['Z83'])) + (0.68*(paramDict['Z84'] + paramDict['Z85'] + paramDict['Z86']))
    return CC_PPIX01