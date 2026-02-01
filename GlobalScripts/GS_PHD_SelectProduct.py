from System import DateTime
contRow=Product.GetContainerByName('HCI_PHD_Selected_Products').Rows
prdLst=[]
for row in contRow:
    prdLst.append(row['Product'])
phdContDefaultDict={}
phdContDefaultDict['HCI_PHD_NewDisplaysforInsight']=['Number of medium displays','New Displays for Insight']
phdContDefaultDict['HCI_PHD_MigratedDisplaysforInsight']=['Number of typical displays migrated from Experion','Migrated Displays for Insight']
phdContDefaultDict['HCI_PHD_ExcelReports']=['Number of medium reports','Reports']
phdContDefaultDict['HCI_PHD_CrystalReports']=['Number of medium reports','Crystal Reports'] 
phdContDefaultDict['HCI_PHD_SSRS_Reports']=['Number of medium reports','SQL Server Reporting Services (SSRS) Reports']
phdContDefaultDict['HCI_PHD_Hardware']=['Total number of servers','Hardware']
phdContDefaultDict['HCI_PHD_VirtualCalculations']=['Number of medium virtual calculations','Virtual Calculations']
phdContDefaultDict['HCI_PHD_USMConfiguration']=['Number of Historised Monitor Items','USM Configuration']
prdDict={'PHD Labor':'PHD_Labor_cpq','Uniformance Insight Labor':'Uniformance_Insight_Labor_cpq','AFM Labor':'AFM_Labor_cpq'}
selectPrds=Product.Attributes.GetByName('HCI_Product_Choices').GetValue()
if selectPrds:
    selectPrds=selectPrds.replace(", ", ",")
    selectPrds=selectPrds.split(',')
    for prd in selectPrds:
        if prd not in prdLst:
            row=Product.GetContainerByName('HCI_PHD_Selected_Products').AddNewRow(prdDict[prd],False)
            row.Product.Attributes.GetByName('AR_HCI_PRODUCTIVITY').AssignValue('1')
            #row.Product.Attributes.GetByName('Execution Year').AssignValue('2024')
            row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').SelectDisplayValue(str(DateTime.Now.Year))
            row.Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').SelectDisplayValue('United States')
            row.Product.Attributes.GetByName('HCI_PHD_GES_Location').SelectDisplayValue('GES India')
            addrow=row.Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').AddNewRow(False)
            addrow.GetColumnByName('Execution Year').ReferencingAttribute.SelectDisplayValue(str(DateTime.Now.Year))
            addrow.GetColumnByName('Deliverable').ReferencingAttribute.SelectDisplayValue('Total')
            addrow['Hidden_lable']='Total'
            addrow['Final Hrs']=str(0)
            addrow.ApplyProductChanges()
            addrow.Calculate()
            if prd=='PHD Labor':
                row.Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').AssignValue('0')
                phdConts=['AR_HCI_PHD_ProjectInputs1','AR_HCI_PHD_ProjectInputs2','HCI_PHD_NewDisplaysforInsight','HCI_PHD_MigratedDisplaysforInsight','HCI_PHD_ExcelReports','HCI_PHD_CrystalReports','HCI_PHD_SSRS_Reports','HCI_PHD_Hardware','HCI_PHD_VirtualCalculations','HCI_PHD_USMConfiguration']
                for conts in phdConts:
                    prdCont=row.Product.GetContainerByName(conts)
                    if prdCont.Rows.Count==0:
                        newRow=prdCont.AddNewRow(False)
                        if conts in phdContDefaultDict.keys():
                            for col in phdContDefaultDict[conts]:
                                newRow[col]='1'
                NoSysInterfared=row.Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').GetValue()
                if not NoSysInterfared:
                    row.Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').SelectDisplayValue('1')
                    cont=row.Product.GetContainerByName('HCI_PHD_Tech_Scope')
                    cont.Clear()
                    row=cont.AddNewRow(False)
                    row.GetColumnByName('System to be interfaced to').ReferencingAttribute.SelectDisplayValue('Type A RDI:  Experion Link (Experion or TPS DCS)')
                    row['Number of Connections']='1'
                    row['Number of Collected Tags']='1000'