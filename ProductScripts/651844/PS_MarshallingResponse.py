import GS_R2Q_FunctionalUtil
WriteinProdCont = Product.GetContainerByName('WriteInProduct')

IoContainerlist = ['C300_RG_Universal_IO_cont_1', 'SerC_RG_Enhanced_Function_IO_Cont', 'C300_CG_Universal_IO_cont_1', 'SerC_CG_Enhanced_Function_IO_Cont', 'C300_RG_Universal_IO_cont_2','C300_CG_Universal_IO_cont_2','SerC_CG_Enhanced_Function_IO_Cont2', 'C300_CG_Universal_IO_Mark_1', 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont ', 'C300_CG_Universal_IO_Mark_2', 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1', 'SerC_RG_Enhanced_Function_IO_Cont2', 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont', 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1']

NISAIIotypelist = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)_Iosum', 'SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)_Iosum', 'Series-C: HLAI (16) with HART with differential inputs (0-5000)_Iosum', 'Series-C: LLAI (1) Mux RTD (0-5000)_Iosum', 'Series-C: LLAI (1) Mux TC (0-5000)_Iosum', 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)_Iosum', 'SCM: HLAI (16) with HART with differential inputs (0-5000)_Iosum']
NISAOIotypelist = ['Series-C: UIO (32) Analog Output (0-5000)_Iosum', 'SCM: UIO (32) Analog Output (0-5000)_Iosum', 'Series-C: AO (16) HART (0-5000)_Iosum', 'SCM: AO (16) HART (0-5000)_Iosum']
NISDIlist = ['Series-C: UIO (32) Digital Input (0-5000)_Iosum', 'SCM: UIO (32) Digital Input (0-5000)_Iosum', 'Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)_Iosum', 'Series-C: DI (32) 24VDC SOE (0-5000)_Iosum', 'Series-C: Pulse Input (8) Single Channel (0-5000)_Iosum', 'Series-C: Pulse Input (4) Dual Channel (0-5000)_Iosum', 'Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)_Iosum','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)_Iosum','SCM: Pulse Input (8) Single Channel (0-5000)_Iosum','SCM: Pulse Input (4) Dual Channel (0-5000)_Iosum','SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)_Iosum']
NISDOlist = ['Series-C: UIO (32) Digital Output (0-5000)_Iosum', 'SCM: UIO (32) Digital Output (0-5000)_Iosum', 'Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)_Iosum', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)_Iosum', 'SCM: DO (32) 24VDC Bus External Power Supply (0-5000)_Iosum', 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)_Iosum']

###red is and non red is -- Red_IS, Non_Red_IS
ISAIlist = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)_IoIsSum',' SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)_IoIsSum',' Series-C: HLAI (16) with HART with differential inputs (0-5000)_IoIsSum',' Series-C: LLAI (1) Mux RTD (0-5000)_IoIsSum',' Series-C: LLAI (1) Mux TC (0-5000)_IoIsSum',' Series-C: LLAI (1) Mux TC Remote CJR (0-5000)_IoIsSum',' SCM: HLAI (16) with HART with differential inputs (0-5000)_IoIsSum']

ISAOlist = ['Series-C: UIO (32) Analog Output (0-5000)_IoIsSum','SCM: UIO (32) Analog Output (0-5000)_IoIsSum','Series-C: AO (16) HART (0-5000)_IoIsSum','SCM: AO (16) HART (0-5000)_IoIsSum']

ISDIlist = ['Series-C: UIO (32) Digital Input (0-5000)_IoIsSum',' SCM: UIO (32) Digital Input (0-5000)_IoIsSum',' Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoIsSum',' Series-C: DI (32) 24VDC SOE (0-5000)_IoIsSum',' Series-C: Pulse Input (8) Single Channel (0-5000)_IoIsSum',' Series-C: Pulse Input (4) Dual Channel (0-5000)_IoIsSum',' Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)_IoIsSum',' SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoIsSum',' SCM: Pulse Input (8) Single Channel (0-5000)_IoIsSum',' SCM: Pulse Input (4) Dual Channel (0-5000)_IoIsSum',' SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)_IoIsSum']

ISDOlist = ['Series-C: UIO (32) Digital Output (0-5000)_IoIsSum',' SCM: UIO (32) Digital Output (0-5000)_IoIsSum',' Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)_IoIsSum',' Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoIsSum',' SCM: DO (32) 24VDC Bus External Power Supply (0-5000)_IoIsSum',' SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoIsSum']

### Red_RLY, Non_Red_RLY
RelayDIlist = ['Series-C: UIO (32) Digital Input (0-5000)_IoRLYSum','SCM: UIO (32) Digital Input (0-5000)_IoRLYSum','Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoRLYSum','Series-C: DI (32) 24VDC SOE (0-5000)_IoRLYSum','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoRLYSum']

RelayDOlist = ['Series-C: UIO (32) Digital Output (0-5000)_IoRLYSum',' SCM: UIO (32) Digital Output (0-5000)_IoRLYSum',' Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)_IoRLYSum',' Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoRLYSum',' SCM: DO (32) 24VDC Bus External Power Supply (0-5000)_IoRLYSum',' SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoRLYSum']

installedSpareIO = 0
iospare = 0

SMIOContainerList = ['SM_IO_Count_Analog_Input_Cont', 'SM_IO_Count_Analog_Output_Cont', 'SM_IO_Count_Digital_Input_Cont', 'SM_IO_Count_Digital_Output_Cont', 'SM_CG_Cabinet_Details_Cont_Right', 'SM_CG_Cabinet_Details_Cont_Left', 'SM_RG_Cabinet_Details_Cont_Left', 'SM_RG_Cabinet_Details_Cont','SM_RG_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Output_Cont', 'SM_RG_IO_Count_Digital_Input_Cont', 'SM_RG_IO_Count_Digital_Output_Cont']

SmNISAIDOList= ['SM_IO_Count_Analog_Output_Cont' , 'SM_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Output_Cont']
SmNISAOList= ['SM_IO_Count_Analog_Output_Cont', 'SM_RG_IO_Count_Analog_Output_Cont']
SmNISDIList = ['SM_IO_Count_Digital_Input_Cont', 'SM_RG_IO_Count_Digital_Input_Cont']
SmNISDOList = ['SM_IO_Count_Digital_Output_Cont', 'SM_RG_IO_Count_Digital_Output_Cont']

def extractProductContainer(attrName, product):
    containerList = []
    containerProductList = []
    containerRows = product.GetContainerByName(attrName).Rows
    if containerRows.Count > 0:
        sumofcount = {'Iosum': 0, 'IoIsSum': 0, 'IoRLYSum': 0}
        keydict = {
            'Red_NIS': 'Iosum',
            'Non_Red_NIS': 'Iosum',
            'Red_ISLTR': 'Iosum',
            'Non_Red_ISLTR': 'Iosum',
            'Red_IS': 'IoIsSum',
            'Non_Red_IS': 'IoIsSum',
            'Red_RLY': 'IoRLYSum',
            'Non_Red_RLY': 'IoRLYSum',
        }
        key_Dict = {
            'Red (NIS)': 'Asum',
            'Non Red (NIS)': 'Asum',
            'Red_NIS': 'Asum',
            'Non_Red_NIS': 'Asum',
            'Non Red (IS)': 'BSum',
            'Red (IS)': 'BSum',
            'Red_IS': 'BSum',
            'Non_Red_IS': 'BSum',
            'Red (RLY)': 'CSum',
            'Non Red (RLY)': 'CSum',
            'Red_RLY': 'CSum',
            'Non_Red_RLY': 'CSum',
        }
        Iotype_ = ""
        DItype = ''
        installedSpare = ''
        RMinstalledSpare = ''
        relaytypeforesd = ''
        RMrelaytypeforesd = ''

        for contanierRow in containerRows:
            contanierRowDict = {}
            if attrName in IoContainerlist:
                for col in contanierRow.Columns:
                    if contanierRow[col.Name] != '':
                        if col.Name in keydict:
                            sumofcount[keydict[col.Name]] = sumofcount[keydict[col.Name]] +  int(contanierRow[col.Name])
                        if col.Name == 'IO_Type':
                            Iotype_ = contanierRow[col.Name]

                if Iotype_:
                    contanierRowDict[Iotype_ + '_Iosum'] = sumofcount.get('Iosum') or 0
                    contanierRowDict[Iotype_ + '_IoIsSum'] = sumofcount['IoIsSum'] or 0
                    contanierRowDict[Iotype_ + '_IoRLYSum'] = sumofcount['IoRLYSum'] or 0
                containerList.append(contanierRowDict)

    
            #safetymanger
            if attrName in SMIOContainerList:
                sum_of_count = {'Asum': 0, 'BSum': 0, 'CSum': 0}
                relaytypeforesd = ''
                for col in contanierRow.Columns:
                    if col.Name == 'SM_CG_RelayTypeForESD':
                        relaytypeforesd = contanierRow.Product.Attr('SM_General_RelayTypeForESD').GetValue()
                    if contanierRow[col.Name] != '':
                        if col.Name in key_Dict:
                            sum_of_count[key_Dict[col.Name]] = sum_of_count[key_Dict[col.Name]] +  int(contanierRow[col.Name])

                        if col.Name == 'Digital Input Type' or col.Name == 'Analog Input Type' or col.Name == 'Analog Output Type' or col.Name == 'Digital Output Type' or col.Name == 'Analog_Output_Type' or col.Name == 'Analog_Input_Type' or col.Name == 'Digital_Input_Type' or col.Name == 'Digital_Output_Type':
                            DItype = contanierRow[col.Name]

                        elif col.Name == 'Percent_Installed_Spare_IOs' or col.Name == 'SM_CG_Percentage_SSM_Cabinet(0-100%)':
                            installedSpare = contanierRow[col.Name]

                        #elif col.Name == 'SM_CG_RelayTypeForESD':
                            #relaytypeforesd = contanierRow[col.Name]

                        elif col.Name in ['SM_RG_Percentage_SSM_Cabinet(0-100%)', 'SM_Percent_Installed_Spare_IO']:
                            RMinstalledSpare = contanierRow[col.Name]

                        #elif col.Name == 'SM_RG_RelayTypeForESD':
                            #RMrelaytypeforesd = contanierRow[col.Name]

                if DItype:
                    contanierRowDict[DItype + '_Asum'] = sum_of_count['Asum'] or 0
                    contanierRowDict[DItype + '_BSum'] = sum_of_count['BSum'] or 0
                    contanierRowDict[DItype + '_CSum'] = sum_of_count['CSum'] or 0

                if installedSpare:
                    contanierRowDict['Percent_Installed_Spare_IOs'] = installedSpare
                    contanierRowDict['SM_CG_Percentage_SSM_Cabinet(0-100%)'] = installedSpare
                    contanierRowDict['SM_CG_RelayTypeForESD'] = relaytypeforesd
                if RMinstalledSpare:
                    contanierRowDict['SM_Percent_Installed_Spare_IO'] = RMinstalledSpare
                    #contanierRowDict['Marshalling_Option'] = RMinstalledSpare
                    contanierRowDict['SM_RG_Percentage_SSM_Cabinet(0-100%)'] = RMinstalledSpare
                    contanierRowDict['SM_RG_RelayTypeForESD'] = RMrelaytypeforesd

                containerList.append(contanierRowDict)

            if contanierRow.Product:
                selectAttributedict_level = {}
                extractProductAttributes(selectAttributedict_level, contanierRow.Product)
                containerProductList.append(selectAttributedict_level)

    return [containerList , containerProductList]

def extractProductAttributes(attributedict, product):
    for attr in product.Attributes:
        if attr.DisplayType == 'Container' and attr.Name not in attributedict:
            attributedict[attr.Name] = extractProductContainer(attr.Name, product)
        else:
            if product.Attr(attr.Name).GetValue() != '' and attr.Name not in attributedict:
                attributedict[attr.Name] = product.Attr(attr.Name).GetValue()

productNameList = []

def WirteinItemsCreation(row, remotegroupcont, installedSpareIO, iospare, NISAI, NISAO, NISDI, NISDO, ISAI, ISAO, ISDI, ISDO, RelayDI, RelayDO, relayesd= ''):
    APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
    APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
    tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
    responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
    Req_Token = "{} {}".format(responseToken["token_type"] , responseToken["access_token"])
    excel_Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/excel-data"
    header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
    if 'Series_C_CG_Name' in row:
        controlgroup = row['Series_C_CG_Name']
        productLine = 'DCS'
        cabinetType = 'C300'
    else:
        childProdcutname = ''
        controlgroup = row['SM_CG_Name']
        prodCont = Product.GetContainerByName('R2Q CE_System_Cont').Rows
        if prodCont.Count > 0:
            for product in prodCont:
                if product.Product.Name in ['R2Q Safety Manager FGS', 'R2Q Safety Manager ESD']:
                    if product.Product.Name not in productNameList:
                        childProdcutname = 'FGS' if product.Product.Name == 'R2Q Safety Manager FGS' else 'ESD'
                        productNameList.append(product.Product.Name)
                        break
        productLine = childProdcutname
        cabinetType = 'Safety Manager'

    if remotegroupcont != '':
        if 'Series_C_RG_Name' in remotegroupcont:
            remotegroup = remotegroupcont['Series_C_RG_Name']
        else:
            remotegroup = remotegroupcont['SM_RemoteGroup_Cont'][1][0]['SM_RG_Name']
        final_request_body=("{{'quoteNumber' : '{0}', 'parentConfig' : '{1}', 'config' : '{2}', 'module' : 'Marshalling', 'executionCountry' : 'India', 'cabinetType' : '{17}', 'productLine' : '{15}', 'installedSpareIO' : '{3}', 'IOSpare' : '{4}', "
        "'RelayTypeForESD' : '{16}', 'NISAI' : '{5}', 'NISAO' : '{6}', 'NISDI' : '{7}', 'NISDO' : '{8}', 'ISAI' : '{9}', "
        "'ISAO' : '{10}', 'ISDI' : '{11}', 'ISDO' : '{12}', 'RelayDI' : '{13}', 'RelayDO' : '{14}'}}").format(Quote.CompositeNumber, controlgroup.decode("utf-8", errors="ignore"), remotegroup.decode('utf-8',  errors="ignore"), installedSpareIO, iospare, NISAI, NISAO, NISDI, NISDO, ISAI, ISAO, ISDI, ISDO, RelayDI, RelayDO, productLine, relayesd, cabinetType)
    else:
        final_request_body=("{{'quoteNumber' : '{0}', 'parentConfig' : '', 'config' : '{1}', 'module' : 'Marshalling', 'executionCountry': 'India', 'cabinetType' : '{17}', 'productLine' : '{15}', 'installedSpareIO' : '{3}', 'IOSpare' : '{4}', 'RelayTypeForESD' : '{16}', 'NISAI' : '{5}', 'NISAO' : '{6}', 'NISDI' : '{7}', 'NISDO' : '{8}', 'ISAI' : '{9}', 'ISAO' : '{10}', 'ISDI' : '{11}', 'ISDO' : '{12}', 'RelayDI' : '{13}', 'RelayDO' : '{14}'}}").format(Quote.CompositeNumber, controlgroup.decode("utf-8", errors="ignore"), '', installedSpareIO, iospare, NISAI, NISAO, NISDI, NISDO, ISAI, ISAO, ISDI, ISDO, RelayDI, RelayDO, productLine, relayesd, cabinetType)
    Log.Write("request body--->" +str(final_request_body))
    res = RestClient.Post(excel_Url, RestClient.SerializeToJson(final_request_body),header)
    res2=JsonHelper.Deserialize(res)
    Log.Write('Response for Marshalling from Apigee == '+ str(res2))
    if res2 and len(res2) > 0 and 'Failure' not in res2:
        marshalling_cabinet_counts = {
            'DCS Marshalling': "",
            'ESD Marshalling': "",
            'FGS Marshalling': ""
        }
        for itemdet in res2:
            containerRow = WriteinProdCont.AddNewRow(False)
            containerRow.GetColumnByName('Category').SetAttributeValue('Common')
            containerRow["Selected_WriteIn"] = str(itemdet['Part/Model #'])
            containerRow["WriteInProducts"] = str(itemdet['Part/Model #'])
            containerRow["Price"] = str(itemdet['Unit List Price'])
            containerRow["Cost"] = str(itemdet['Unit Regional Cost'])
            containerRow["ItemQuantity"] = str(itemdet['Quantity'])
            containerRow['Area'] = str(itemdet['Area'])
            containerRow["ExtendedDescription"]= itemdet['Extended Description']
            if itemdet['Extended Description'].startswith('TS8 Cabinet Base'):
                area = str(itemdet['Area'])
                if area in marshalling_cabinet_counts:
                    marshalling_cabinet_counts[area] = str(itemdet['Quantity'])
        if any(marshalling_cabinet_counts.values()):
            for systemCont in Product.GetContainerByName('R2Q CE_System_Cont').Rows:
                if systemCont['Selected_Products'] == "R2Q C300 System" and marshalling_cabinet_counts['DCS Marshalling']:
                    systemCont.Product.Attr('C300_Marshalling_cabinet_count (0-500)').AssignValue(marshalling_cabinet_counts['DCS Marshalling'])
                if systemCont['Selected_Products'] in ("R2Q Safety Manager ESD", "R2Q Safety Manager FGS"):
                    for laborCont in systemCont.Product.GetContainerByName('SM_Labor_Cont').Rows:
                        if marshalling_cabinet_counts['ESD Marshalling']:
                            laborCont['Marshalling_cabinet_count'] = marshalling_cabinet_counts['ESD Marshalling']
                        if marshalling_cabinet_counts['FGS Marshalling']:
                            laborCont['Marshalling_cabinet_count'] = marshalling_cabinet_counts['FGS Marshalling']
try:
    saveAction = Quote.GetCustomField("R2Q_Save").Content
    isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
    if isR2Qquote and saveAction != 'Save':
        res2 = []
        selectAttributedict = {}
        extractProductAttributes(selectAttributedict,Product)
        containerValues = str(selectAttributedict)
        remotegroupcheck = False
        SmIoInsatlledSpare = ''
        SmCabinetspare = ''
        rmcabinet = ''
        rminstalledspare = ''
        relayesd = ''
        SmMarshallingvalue = ''
        SMremotegroupcheck = False
        RmMarshalling = ''
        
        for data in selectAttributedict['R2Q CE_System_Cont'][1]:
            #C300
            if 'Series_C_Control_Groups_Cont' in data:
                CGinstalledSpareIO = 0
                CGIoSpare =0
                for key, val in data.items():
                    if key == 'Series_C_Control_Groups_Cont':
                        for row in data[key][1]:
                            Trace.Write('rows = '+str(row))
                            sums = {
                            'NISAI': 0, 'NISAO': 0, 'NISDI':0, 'NISDO':0,
                                'ISAI': 0, 'ISAO': 0, 'ISDI': 0, 'ISDO': 0,
                                'RelayDI': 0, 'RelayDO': 0, 'NISDORG': 0,
                                'NISAIRG': 0, 'NISAORG': 0
                            }
                            marshalling = '3rd Party Marshalling' if row.get('SerC_CG_Marshalling_Cabinet_Type') == '3rd Party Marshalling' else ''
                            CGinstalledSpareIO = int(row.get('SerC_CG_Percent_Installed_Spare') or 0)
                            CGIoSpare = int(row.get('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet') or 0)
                            if marshalling:
                                for ciotype, cioval in row.items():

                                    if ciotype in IoContainerlist and all(row[ciotype]):
                                        for k, v in row[ciotype][0][0].items():
                                            if k in NISAIIotypelist :
                                                sums['NISAI'] += row[ciotype][0][0][k]
                                            if k in NISAOIotypelist:
                                                sums['NISAO'] += row[ciotype][0][0][k]
                                            if k in NISDIlist:
                                                sums['NISDI'] += row[ciotype][0][0][k]
                                            if k in NISDOlist:
                                                sums['NISDO'] += row[ciotype][0][0][k]
                                            if k in ISAIlist:
                                                sums['ISAI'] += row[ciotype][0][0][k]
                                            if k in ISAOlist:
                                                sums['ISAO'] += row[ciotype][0][0][k]
                                            if k in ISDIlist:
                                                sums['ISDI'] += row[ciotype][0][0][k]
                                            if k in ISDOlist:
                                                sums['ISDO'] += row[ciotype][0][0][k]
                                            if k in RelayDIlist:
                                                sums['RelayDI'] += row[ciotype][0][0][k]
                                            if k in RelayDOlist:
                                                sums['RelayDO'] += row[ciotype][0][0][k]

                                if 'Series_C_Remote_Groups_Cont' in row and len(row['Series_C_Remote_Groups_Cont'][1]) > 0:
                                    remotegroupcheck = True
                                    for remotegroupcont in row['Series_C_Remote_Groups_Cont'][1]:
                                        installedSpareIO += int(int(row['SerC_CG_R2Q_Percent_Installed_Spare']) + int((remotegroupcont['SerC_RG_Percent_Installed_Spare(0-100%)'])))
                                        iospare += int(int(row['SerC_CG_Percent_SpareSpace_Marshalling_Cabinet']) + int((remotegroupcont['SerC_RG_Percentage_SSM_Cabinet (0-100%)'])))

                                        for riotype, rioval in remotegroupcont.items():
                                            if riotype in IoContainerlist and all(remotegroupcont[riotype]):
                                                for k, v in remotegroupcont[riotype][0][0].items():
                                                    if k in NISAIIotypelist:
                                                        sums['NISAI'] += remotegroupcont[riotype][0][0][k]
                                                    if k in NISAOIotypelist:
                                                        sums['NISAO'] += remotegroupcont[riotype][0][0][k]
                                                    if k in NISDIlist:
                                                        sums['NISDI'] += remotegroupcont[riotype][0][0][k]
                                                    if k in NISDOlist:
                                                        sums['NISDO'] += remotegroupcont[riotype][0][0][k]
                                                    if k in ISAIlist:
                                                        sums['ISAI'] += remotegroupcont[riotype][0][0][k]
                                                    if k in ISAOlist:
                                                        sums['ISAO'] += remotegroupcont[riotype][0][0][k]
                                                    if k in ISDIlist:
                                                        sums['ISDI'] += remotegroupcont[riotype][0][0][k]
                                                    if k in ISDOlist:
                                                        sums['ISDO'] += remotegroupcont[riotype][0][0][k]
                                                    if k in RelayDIlist:
                                                        sums['RelayDI'] += remotegroupcont[riotype][0][0][k]
                                                    if k in RelayDOlist:
                                                        sums['RelayDO'] += remotegroupcont[riotype][0][0][k]


                                        WirteinItemsCreation(row, remotegroupcont, installedSpareIO, iospare, sums['NISAI'], sums['NISAO'], sums['NISDI'], sums['NISDO'], sums['ISAI'], sums['ISAO'], sums['ISDI'], sums['ISDO'], sums['RelayDI'], sums['RelayDO'])
                                if not remotegroupcheck:
                                    WirteinItemsCreation(row, "", CGinstalledSpareIO, CGIoSpare, sums['NISAI'], sums['NISAO'], sums['NISDI'], sums['NISDO'], sums['ISAI'], sums['ISAO'], sums['ISDI'], sums['ISDO'], sums['RelayDI'], sums['RelayDO'])
            #safety manager
            if 'SM_ControlGroup_Cont' in data:
                relayesd = ''
                for key, values in data.items():
                    if key == 'SM_ControlGroup_Cont':
                        SM_sums = {
                            'SMNISAI': 0, 'SMNISAO': 0, 'SMNISDI': 0, 'SMNISDO': 0,
                            'SMNISAIB': 0, 'SMNISAOB': 0, 'SMNISDIB': 0, 'SMNISDOB': 0,
                            'SMRelayDI': 0, 'SMRelayDO': 0
                        }

                        for SMcontDetails in data[key][1]:
                            if 'Universal Marshalling Cabinet' in SMcontDetails:
                                SmMarshallingvalue = 'Hardware Marshalling with Other' if SMcontDetails['Universal Marshalling Cabinet'] == 'Hardware Marshalling with Other' else ''

                            if SmMarshallingvalue:
                                for cont, contVal in SMcontDetails.items():
                                    if cont in SMIOContainerList:
                                        if 'SM_CG_Cabinet_Details_Cont_Right' == cont and 'Percent_Installed_Spare_IOs' in contVal[0][0]:
                                            SmIoInsatlledSpare = contVal[0][0]['Percent_Installed_Spare_IOs']
                                        elif 'SM_CG_Cabinet_Details_Cont_Left' == cont:
                                            if  'SM_CG_RelayTypeForESD' in contVal[0][0]:
                                                relayesd = contVal[0][0]['SM_CG_RelayTypeForESD']
                                            if 'SM_CG_Percentage_SSM_Cabinet(0-100%)' in contVal[0][0]:
                                                SmCabinetspare = contVal[0][0]['SM_CG_Percentage_SSM_Cabinet(0-100%)']
                                        if len(contVal[0]) > 0 and all(contVal[0]):
                                            for count in range(len(contVal[0])):
                                                for smk, smv in contVal[0][count].items():
                                                    if '_Asum' in smk:
                                                        if cont in SmNISAIDOList:
                                                            SM_sums['SMNISAI'] += contVal[0][count][smk]
                                                        if cont in SmNISAOList:
                                                            SM_sums['SMNISAO'] += contVal[0][count][smk]
                                                        if cont in SmNISDIList:
                                                            SM_sums['SMNISDI'] += contVal[0][count][smk]
                                                        if cont in SmNISDOList:
                                                            SM_sums['SMNISDO'] += contVal[0][count][smk]
                                                    elif '_BSum' in smk:
                                                        if cont in SmNISAIDOList:
                                                            SM_sums['SMNISAIB'] += contVal[0][count][smk]
                                                        if cont in SmNISAOList:
                                                            SM_sums['SMNISAOB'] += contVal[0][count][smk]
                                                        if cont in SmNISDIList:
                                                            SM_sums['SMNISDIB'] += contVal[0][count][smk]
                                                        if cont in SmNISDOList:
                                                            SM_sums['SMNISDOB'] += contVal[0][count][smk]
                                                    elif '_CSum' in smk:
                                                        if cont in SmNISDIList:
                                                            SM_sums['SMRelayDI'] += contVal[0][count][smk]
                                                        if cont in SmNISDIList:
                                                            SM_sums['SMRelayDO'] += contVal[0][count][smk]

                        if 'SM_RemoteGroup_Cont' in SMcontDetails and len(SMcontDetails['SM_RemoteGroup_Cont'][1]) > 0:
                            SMremotegroupcheck = True
                            RMrelayesdVal = ''
                            installedspare = 0
                            cabinet = 0
                            for cont, contVal in SMcontDetails.items():
                                if cont == 'SM_RemoteGroup_Cont':
                                    for rmkey, rmvalue in contVal[1][0].items():
                                        if  rmkey == 'trigger_DigitalIO':
                                            RmMarshalling = 'Hardware_Marshalling_with_Other' if contVal[1][0]['trigger_DigitalIO'] == 'Hardware_Marshalling_with_Other' else ''
                                        if rmkey in SMIOContainerList:
                                            if rmkey == 'SM_RG_Cabinet_Details_Cont_Left' and 'SM_RG_Percentage_SSM_Cabinet' in rmvalue[0][0]:
                                                rmcabinet = int(rmvalue[0][0]['SM_RG_Percentage_SSM_Cabinet(0-100%)']) + int(SmCabinetspare)
                                            if rmkey == 'SM_RG_Cabinet_Details_Cont':
                                                if 'SM_Percent_Installed_Spare_IO' in rmvalue[0][0]:
                                                    rminstalledspare = int(rmvalue[0][0]['SM_Percent_Installed_Spare_IO']) + int(SmIoInsatlledSpare)
                                            if rmkey == 'SM_RG_RelayTypeForESD':
                                                if 'SM_RG_RelayTypeForESD' in rmvalue[0][0]:
                                                    RMrelayesdVal = rmvalue[0][0]['SM_RG_RelayTypeForESD']
                                            if len(rmvalue[0]) > 0 and all(rmvalue[0]):
                                                for smrmcontainer in rmvalue[0]:
                                                    for smrmkey, smrmval in smrmcontainer.items():
                                                        if '_Asum' in smrmkey:
                                                            if rmkey in SmNISAIDOList:
                                                                SM_sums['SMNISAI'] += int(smrmval)
                                                            if rmkey in SmNISAOList:
                                                                SM_sums['SMNISAO'] += int(smrmval)
                                                            if rmkey in SmNISDIList:
                                                                SM_sums['SMNISDI'] += int(smrmval)
                                                            if rmkey in SmNISDOList:
                                                                SM_sums['SMNISDO'] += int(smrmval)
                                                        elif '_BSum' in smrmkey:
                                                            if rmkey in SmNISAIDOList:
                                                                SM_sums['SMNISAIB'] += int(smrmval)
                                                            if rmkey in SmNISAOList:
                                                                SM_sums['SMNISAOB'] += int(smrmval)
                                                            if rmkey in SmNISDIList:
                                                                SM_sums['SMNISDIB'] += int(smrmval)
                                                            if rmkey in SmNISDOList:
                                                                SM_sums['SMNISDOB'] += int(smrmval)
                                                        elif '_CSum' in smrmkey:
                                                            if rmkey in SmNISDIList:
                                                                SM_sums['SMRelayDI'] += int(smrmval)
                                                            if rmkey in SmNISDIList:
                                                                SM_sums['SMRelayDO'] += int(smrmval)
                                    if RmMarshalling:
                                        WirteinItemsCreation(SMcontDetails, SMcontDetails, rminstalledspare, rmcabinet, SM_sums['SMNISAI'], SM_sums['SMNISAO'], SM_sums['SMNISDI'], SM_sums['SMNISDO'], SM_sums['SMNISAIB'], SM_sums['SMNISAOB'], SM_sums['SMNISDIB'], SM_sums['SMNISDOB'], SM_sums['SMRelayDI'], SM_sums['SMRelayDO'], relayesd)

                        if SmMarshallingvalue and RmMarshalling == '':
                            WirteinItemsCreation(SMcontDetails, '', SmIoInsatlledSpare, SmCabinetspare, SM_sums['SMNISAI'], SM_sums['SMNISAO'], SM_sums['SMNISDI'], SM_sums['SMNISDO'], SM_sums['SMNISAIB'], SM_sums['SMNISAOB'], SM_sums['SMNISDIB'], SM_sums['SMNISDOB'], SM_sums['SMRelayDI'], SM_sums['SMRelayDO'], relayesd)
except Exception as ex:
    Log.Write("Exception occured as follows:
{0}".format(ex))
    msg = 'Error Occured, {"ErrorCode": "PartsLaborConfig", "ErrorDescription": "Failed at: Marshalling"}'
    GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
    raise