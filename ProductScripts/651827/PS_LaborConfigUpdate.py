import GS_R2QHCI_ProductLoad
#Product.Attr("Customer_Budget_TextField").Access = AttributeAccess.Hidden
Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content = Product.Attr('AR_HCI_Proposal Language').GetValue()
if Product.Attr('Sell Price Strategy').GetValue() == 'Customer Budget':
    #Product.Attr("Customer_Budget_TextField").Access = AttributeAccess.Editable
    Product.AllowAttr('Customer_Budget_TextField')
    Product.AllowAttr('Customer_Budget_USD')
    Product.Attr('Customer_Budget_USD').Access = AttributeAccess.ReadOnly
else:
    Product.DisallowAttr('Customer_Budget_TextField')
    Product.DisallowAttr('Customer_Budget_USD')
#To update the visibitity of common labor input section
scope = Product.Attr('AR_HCI_SCOPE').GetValue()
if scope == "Software":
    Trace.Write('REENDsw-')
    Product.Attr("Header_02_open").Access = AttributeAccess.Hidden
    Product.Attr("ATTCON_02_open").Access = AttributeAccess.Hidden
    Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Hidden
    Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Hidden
    Product.Attr("R2Q_Alternate_Execution_Country").Access = AttributeAccess.Hidden
    Product.Attr("Project_Execution_Year").Access = AttributeAccess.Hidden
    Product.Attr("ATTCON_02_close").Access = AttributeAccess.Hidden
    Product.Attr("Header_02_close").Access = AttributeAccess.Hidden
elif scope == "Software + Labor":
    Trace.Write('REENDsw+lab-')
    Product.Attr("Header_02_open").Access = AttributeAccess.Editable
    Product.Attr("ATTCON_02_open").Access = AttributeAccess.Editable
    Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Editable
    Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Editable
    Product.Attr("R2Q_Alternate_Execution_Country").Access = AttributeAccess.Editable
    Product.Attr("Project_Execution_Year").Access = AttributeAccess.ReadOnly
    Product.Attr("ATTCON_02_close").Access = AttributeAccess.Editable
    Product.Attr("Header_02_close").Access = AttributeAccess.Editable
#END

cont = Product.GetContainerByName('AR_HCI_SUBPRD')
if cont.Rows.Count>1 and cont.Rows[1]['Selected_Products'] == 'HCI Labor Config' and cont.Rows[0]['Selected_Products'] == 'Honeywell Enterprise Data Management' and cont.Rows[1].Product.GetContainerByName('HCI_PHD_Tech_Scope').Rows.Count>1:
    val = int(cont.Rows[1].Product.GetContainerByName('HCI_PHD_Tech_Scope').Rows[0]['Number of Collected Tags']) + int(cont.Rows[1].Product.GetContainerByName('HCI_PHD_Tech_Scope').Rows[1]['Number of Collected Tags'])
    tags_option = {'1000':'A 1,000 Tags','2500':'B 2,500 Tags','5000':'C 5,000 Tags', '7500':'D 7,500 Tags', '10000':'E 10,000 Tags', '12500':'F 12,500 Tags', '15000':'G 15,000 Tags', '20000':'H 20,000 Tags', '25000':'J 25,000 Tags', '50000':'K 50,000 Tags', '75000':'L 75,000 Tags', '100000':'M 100,000 Tags', '250000':'N 250,000 Tags', '500000':'P 500,000 Tags', '750000':'Q 750,000 Tags', '1000000':'R 1,000,000 Tags', '1500000':'S 1,500,000 Tags', '2000000':'T 2,000,000 Tags'}
    val = int(val)
    base_sys = (cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Base_System_Size').GetValue()).split(' ')[1]
    base_sys = int(base_sys.replace(",", ""))
    #Trace.Write(str(base_sys)+'--HCI_PHD_Base_System_Size--recheck--<---000->'+str(val))
    if base_sys < val:
        #Log.Info(str(base_sys)+'--HCI_PHD_Base_System_Size--recheck--<---111->'+str(val))
        tags_option_int = [int(tag) for tag in tags_option.keys()]
        nearest_highest = [tag for tag in tags_option_int if tag >= val] if tags_option_int else ''
        nearest_highest_tag = min(nearest_highest) if nearest_highest else ''
        Final_collected_tag = tags_option.get(str(nearest_highest_tag),'A 1,000 Tags')
        cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Base_System_Size').SelectDisplayValues(Final_collected_tag)
        #Trace.Write(str(Final_collected_tag)+'--HCI_PHD_Base_System_Size---recheck---222->'+str(cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Base_System_Size').GetValue())+'---->'+str())
        #Log.Info('-HCI_PHD_Base_System_Size--final--'+str(Final_collected_tag))
        cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Base_System_Size').SelectDisplayValue(Final_collected_tag)
        cont.Rows[0].Product.ParseString('<* ExecuteScript(Quote Quantity) *>')
        cont.Rows[0].ApplyProductChanges()
        cont.Rows[0].Calculate()

if cont.Rows.Count>1:
    row=cont.Rows[1]
    row.Product.Attributes.GetByName('HCI_PHD_GES_Location').SelectValue(Product.Attributes.GetByName('AR_HCI_GES Location').GetValue())
    #row.Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectValue(Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').GetValue())
    if Product.Attr("R2Q_Alternate_Execution_Country").GetValue() != Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content:
        Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue("None")
    else:
        Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content)
        row.Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectValue(Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content)
    #Log.Info(str(row.Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').GetValue())+"---alternate---111---"+str(Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').GetValue()))
    #Trace.Write(str(cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Product').GetValue())+'--rows00--'+str(row.Product.Attributes.GetByName('HCI_PHD_Product').GetValue()))
    if (row.Product.Attributes.GetByName('HCI_PHD_Product').GetValue() == '' or row.Product.Attributes.GetByName('HCI_PHD_Product').GetValue()!= cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Product').GetValue()):
        #Trace.Write(str(cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Product').GetValue())+'--Inside reload HCI Labor '+str(row.Product.Attributes.GetByName('HCI_PHD_Product').GetValue()))
        row.Product.Attributes.GetByName('HCI_PHD_Product').SelectDisplayValue(cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Product').GetValue())
        #Trace.Write('HCI_PHD_Base_System_Size--Inside reload HCI Labor GETVALUE '+str(Product.Attributes.GetByName('AR_HCI_GES Location').GetValue()))
        SoftwareConfigured = []
        softwareAliasDict = {'AFM':'AFM_Labor','Insight':'Uniformance_Insight_Labor','PHD':'PHD_Labor','Process History Database (PHD)':'PHD_Labor','Advanced Formula Manager (AFM)':'AFM_Labor'}
        getProductScope = cont.Rows[0].Product.Attributes.GetByName('HCI_PHD_Product').GetValue()
        if '&' in getProductScope:
            selectList = getProductScope.split(' & ')
            for prd in selectList:
                SoftwareConfigured.append(softwareAliasDict[prd])
        else:
            SoftwareConfigured.append(softwareAliasDict.get(getProductScope))
        ges_participation = Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue()
        prdDict={'PHD Labor':'PHD_Labor_cpq','Uniformance Insight Labor':'Uniformance_Insight_Labor_cpq','AFM Labor':'AFM_Labor_cpq'}
        #Trace.Write('SoftwareConfigured--'+str(SoftwareConfigured))
        row.Product.Attr('HCI_Product_Choices').SelectValues(*SoftwareConfigured)
        selectPrds= row.Product.Attributes.GetByName('HCI_Product_Choices').GetValue()
        if 'PHD_Labor' in SoftwareConfigured:
            row.Product.Attributes.GetByName('AR_HCI_PHDSectionVisible').AssignValue('Yes')
            row.Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').AssignValue('0')
            GS_R2QHCI_ProductLoad.laborconfigRolldown(row,TagParserProduct)

        else:
            row.Product.Attributes.GetByName('AR_HCI_PHDSectionVisible').AssignValue('No')
        roles = ["Project Management", "Project Management - GES", "Project Administration", "Project Controls","Lead Engineering"]
        ges_loc = row.Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue()
        country_codes = {'GES China':'CN','GES India':'IN','GES Uzbekistan':'UZ'}
        cuntry_code = country_codes.get(ges_loc)
        rolesDefaultValue={}
        rolesDefaultValue['Project Management']={'Per':'10','Activity':'Sr Project Manager','country':'United States '}
        rolesDefaultValue['Project Management - GES']={'Per':'10','Activity':'ADV GES PM-'+str(cuntry_code)+'','country':'United States'} if int(ges_participation)!= 0 else {'Per':'0','Activity':'ADV GES PM-'+str(cuntry_code)+'','country':'United States'}
        rolesDefaultValue['Project Administration']={'Per':'0','Activity':'Project Admin','country':'United States'}
        rolesDefaultValue['Project Controls']={'Per':'3','Activity':'SYS PCA-Specialist','country':'United States'}
        rolesDefaultValue['Lead Engineering']={'Per':'10','Activity':'PHD Prin Eng','country':'United States'}
        Trace.Write('rolesDefaultValue---'+str(rolesDefaultValue))
        row.Product.GetContainerByName('HCI_Labor_prj_mng_lbr_input').Rows.Clear()
        for role in roles:
            prj_manage_lbr = row.Product.GetContainerByName('HCI_Labor_prj_mng_lbr_input').AddNewRow(False)
            prj_manage_lbr.GetColumnByName('Role').ReferencingAttribute.SelectDisplayValue(role)
            prj_manage_lbr['Percentage']=rolesDefaultValue[role]['Per']
            prj_manage_lbr.GetColumnByName('Activity_Type').ReferencingAttribute.SelectDisplayValue(rolesDefaultValue[role]['Activity'])
            prj_manage_lbr.GetColumnByName('Execution Country').ReferencingAttribute.SelectDisplayValue(rolesDefaultValue[role]['country'])
            prj_manage_lbr.ApplyProductChanges()
            prj_manage_lbr.Calculate()
        row.Product.GetContainerByName('HCI_Labor_common_prj_input1').Rows.Clear()
        input1Cont = row.Product.GetContainerByName('HCI_Labor_common_prj_input1').AddNewRow(False)
        input1Cont.GetColumnByName('User Requirements').SetAttributeValue('Yes')
        input1Cont.GetColumnByName('Project Set Up').SetAttributeValue('Yes')
        input1Cont.GetColumnByName('KOM type').SetAttributeValue('Face 2 Face')
        row.Product.GetContainerByName('HCI_Labor_common_prj_input2').Rows.Clear()
        input2Cont = row.Product.GetContainerByName('HCI_Labor_common_prj_input2').AddNewRow(False)
        input2Cont.GetColumnByName('Site specific documentation').SetAttributeValue(str(input2Cont['Site Acceptance Testing (SAT)']))
        fo_eng = row.Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows[0]
        fo_eng.SetColumnValue('Activity Type','PHD Sr Eng')
        participation = 100 - int(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue() or 0)
        fo_eng.SetColumnValue('Participation',str(participation))
        '''if int(participation)!= 100:
            row.Product.Attributes.GetByName('AR_HCI_ParticipationFlag').AssignValue('False')
        else:
            row.Product.Attributes.GetByName('AR_HCI_ParticipationFlag').AssignValue('True')'''
        fo_eng.SetColumnValue('Number of trips per engineer','1')
        fo_eng.SetColumnValue('Hours per trip','8')
        fo_eng_ges = row.Product.GetContainerByName('HCI_PHD_GES_Eng').Rows[0]
        fo_eng_ges.GetColumnByName('Activity Type').ReferencingAttribute.SelectDisplayValue('ADV GES Prin Eng-'+str(cuntry_code)+'')
        fo_eng_ges.SetColumnValue('Number of trips per engineer','0')
        fo_eng_ges.SetColumnValue('Hours per trip','8')
        fo_eng_ges.SetColumnValue('Participation',str(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue() or 0))
        fo_eng_ges.ApplyProductChanges()
        fo_eng_ges.Calculate()
        row.Product.Attributes.GetByName('AR_HCI_ParticipationFlag').AssignValue('True')

        if selectPrds:
            selectPrds=selectPrds.replace(", ", ",")
            selectPrds=selectPrds.split(',')
            row.Product.GetContainerByName('HCI_PHD_Selected_Products').Rows.Clear()
            for prd in selectPrds:
                laborConfigRow= row.Product.GetContainerByName('HCI_PHD_Selected_Products').AddNewRow(prdDict[prd],True)
                if prd=='PHD Labor':
                    phdContDefaultDict={}
                    phdContDefaultDict['HCI_PHD_NewDisplaysforInsight']=['Number of medium displays','New Displays for Insight']
                    phdContDefaultDict['HCI_PHD_MigratedDisplaysforInsight']=['Number of typical displays migrated from Experion','Migrated Displays for Insight']
                    phdContDefaultDict['HCI_PHD_ExcelReports']=['Number of medium reports','Reports']
                    phdContDefaultDict['HCI_PHD_CrystalReports']=['Number of medium reports','Crystal Reports'] 
                    phdContDefaultDict['HCI_PHD_SSRS_Reports']=['Number of medium reports','SQL Server Reporting Services (SSRS) Reports']
                    phdContDefaultDict['HCI_PHD_Hardware']=['Total number of servers','Hardware']
                    phdContDefaultDict['HCI_PHD_VirtualCalculations']=['Number of medium virtual calculations','Virtual Calculations']
                    phdContDefaultDict['HCI_PHD_USMConfiguration']=['Number of Historised Monitor Items','USM Configuration']
                    laborConfigRow.Product.Attributes.GetByName('HCI_PHD_IsRequired').SelectDisplayValue('1')
                    laborConfigRow.Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').AssignValue('0')
                    phdConts=['AR_HCI_PHD_ProjectInputs1','AR_HCI_PHD_ProjectInputs2','HCI_PHD_NewDisplaysforInsight','HCI_PHD_MigratedDisplaysforInsight','HCI_PHD_ExcelReports','HCI_PHD_CrystalReports','HCI_PHD_SSRS_Reports','HCI_PHD_Hardware','HCI_PHD_VirtualCalculations','HCI_PHD_USMConfiguration']
                    for conts in phdConts:
                        prdCont=laborConfigRow.Product.GetContainerByName(conts)
                        if prdCont.Rows.Count==0:
                            newRow=prdCont.AddNewRow(False)
                            if conts in phdContDefaultDict.keys():
                                for col in phdContDefaultDict[conts]:
                                    newRow[col]='1'
                    NoSysInterfared=laborConfigRow.Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').GetValue()
                    if not NoSysInterfared:
                        setNoSysInterfared = '4' # R2Q Default
                        laborConfigRow.Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').SelectDisplayValue(setNoSysInterfared)
                        cont=laborConfigRow.Product.GetContainerByName('HCI_PHD_Tech_Scope')
                        cont.Clear()
                        sysInterList = ['Type A RDI:  Experion Link (Experion or TPS DCS)','Type A RDI:  OPC RDI (Third Party or Other DCS)','LIMS Interface','ERP Interface']
                        sysInterList_connections = {'Type A RDI:  Experion Link (Experion or TPS DCS)':'3','Type A RDI:  OPC RDI (Third Party or Other DCS)':'2','LIMS Interface':'1','ERP Interface':'1'}
                        for i in range(0,int(setNoSysInterfared)):
                            sysrow=cont.AddNewRow(False)
                            sysrow.GetColumnByName('System to be interfaced to').ReferencingAttribute.SelectDisplayValue(sysInterList[i])
                            sysrow['Number of Connections']=sysInterList_connections.get(sysInterList[i],'1')
                            sysrow['Number of Collected Tags']='1000'
                            if sysInterList[i]!='Type A RDI:  OPC RDI (Third Party or Other DCS)':
                                sysrow.GetColumnByName('Interface Connectivity Complexity').SetAttributeValue('Simple')
                                sysrow.GetColumnByName('Tag configuration Complexity').SetAttributeValue('Simple')
                                sysrow['Interface Connectivity Complexity'] = 'Simple'
                                sysrow['Tag configuration Complexity'] = 'Simple'
                            else:
                                sysrow.GetColumnByName('Interface Connectivity Complexity').SetAttributeValue('Typical')
                                sysrow.GetColumnByName('Tag configuration Complexity').SetAttributeValue('Typical')
                                sysrow['Interface Connectivity Complexity'] = 'Typical'
                                sysrow['Tag configuration Complexity'] = 'Typical'
                    Trace.Write('in phd lavor cont ')
                    #GS_R2QHCI_ProductLoad.laborconfigRolldown(laborConfigRow,TagParserProduct)
                elif prd == 'AFM Labor':
                    laborConfigRow.Product.Attributes.GetByName('HCI_PHD_IsRequiredAFM').SelectDisplayValue('1')
                elif prd == 'Uniformance Insight Labor':
                    laborConfigRow.Product.Attributes.GetByName('HCI_PHD_IsRequiredUNI').SelectDisplayValue('1')
                laborConfigRow.ApplyProductChanges()
    
                # R2Q_BASESYSTEM_UPDATE moved here
    row.Product.ApplyRules()
    row.ApplyProductChanges()
    '''row=cont.Rows[0]
    edm = row.Product.Attributes.GetByName('AR_Collected_tags').GetValue()
    Trace.Write('after one -')
    lab = cont.Rows[1].Product.Attributes.GetByName('AR_Collected_tags').GetValue()
    Trace.Write('after two -')'''
else:
    if Product.Attr("R2Q_Alternate_Execution_Country").GetValue() != Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content:
        Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue("None")
    else:
        Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content)