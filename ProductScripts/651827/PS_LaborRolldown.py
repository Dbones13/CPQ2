#pn = SqlHelper.GetFirst("Select PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK) where PLANT_CODE = '6649' ORDER BY CpqTableEntryId DESC")
## CXCPQ-111107 # R2Q HCI Bundle set default plant
#if pn:
#    Quote.GetCustomField("CF_Plant").Content = str(pn.PLANT_NAME)
Session['R2Q_CompositeNumber'] = Quote.CompositeNumber
if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
    try:
        Quote.GetCustomField("SellPricestrategy").Content = Product.Attr('Sell Price Strategy').SelectedValue.Display
    except:
        Trace.Write("error")
    Quote.GetCustomField("CustomerBudget").Content = Product.Attr('Customer_Budget_TextField').GetValue()
#Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content = Product.Attr("R2Q_Alternate_Execution_Country").GetValue()
#if Product.Attr('AR_HCI_SCOPE').GetValue() != 'Software' and Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Quote.GetCustomField('R2Q_Save').Content != 'Submit' and Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container"):
#    Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container").Rows.Clear()
if (Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Quote.GetCustomField('R2Q_Save').Content == 'Submit') or Quote.GetCustomField('R2QFlag').Content == 'Yes' or (Quote.GetCustomField('R2QFlag').Content != 'Yes' and Quote.GetCustomField('IsR2QRequest').Content!= 'Yes'):
    if Product.GetContainerByName('AR_HCI_SUBPRD').Rows.Count>1:
        cont=Product.GetContainerByName('AR_HCI_SUBPRD').Rows[1]
        parentlabor = cont.Product.Attributes.GetByName('HCI_PHD_ParChildAttr').GetValue()
        parDict1=JsonHelper.Deserialize(parentlabor)
        Trace.Write('labor row product before cart parDict -'+str(parDict1))
        laborDetails=SqlHelper.GetList("select Labor , Service_Material from CT_HCI_PHD_LABORMATERIAL ")
        ServicelaborDict={}
        for lab in laborDetails:
            ServicelaborDict[lab.Service_Material]=lab.Labor
        for mainRow in cont.Product.GetContainerByName('HCI_PHD_Selected_Products').Rows:
            parentProduct=mainRow.Product
            Trace.Write('labor row product before cart -'+str(parentProduct.Name))
            if (Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Quote.GetCustomField('R2Q_Save').Content == 'Submit') or Quote.GetCustomField('R2QFlag').Content != 'Yes' or (Quote.GetCustomField('R2QFlag').Content != 'Yes' and Quote.GetCustomField('IsR2QRequest').Content!= 'Yes' and parentProduct.Attributes.GetByName('apply_changes').GetValue() !='True'):
                parentProduct.Attributes.GetByName('Trigger_r2q_rules').AssignValue('True')
                parDictStr=parentProduct.Attributes.GetByName('HCI_PHD_ParChildAttr').GetValue()
                parDict=JsonHelper.Deserialize(parDictStr)
                Trace.Write('labor row product before cart parDict -'+str(parDict))
                #parentProduct.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectValue(Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').GetValue())
                parentProduct.ApplyRules()
                parentProduct.Attributes.GetByName('Trigger_r2q_rules').AssignValue('')
                mainRow.ApplyProductChanges()
                labourFinalHrsDict={}
                containersLst=['HCI_PHD_EngineeringLabour','HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables']
                #productPrice={}
                for conts in containersLst:
                    contRows=parentProduct.GetContainerByName(conts).Rows
                    for row in contRows:
                        if row['Final Hrs']:
                            if row['Eng'] not in labourFinalHrsDict.keys():
                                labourFinalHrsDict[row['Eng']] = float(row['Final Hrs'])
                            else:
                                labourFinalHrsDict[row['Eng']] += float(row['Final Hrs'])
                contRows=parentProduct.GetContainerByName('HCI_PHD_LabourProducts')
                Trace.Write('Test11 '+str(labourFinalHrsDict))
                delRows=[]
                if len(labourFinalHrsDict)==0:
                    contRows.Clear()
                for labor in labourFinalHrsDict:
                    laborDetails=SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(labor))
                    if laborDetails:
                        flg=0
                        for row in contRows.Rows:
                            if row.Product.PartNumber==laborDetails.Service_Material:
                                flg=1
                                row.Product.Attr('ItemQuantity').AssignValue(str(labourFinalHrsDict[labor]))
                            if ServicelaborDict[row.Product.PartNumber] not in labourFinalHrsDict.keys():
                                #Trace.Write('Here2222')
                                delRows.append(row.RowIndex)
                        if flg==0:
                            Trace.Write('67---in flg-')
                            row=contRows.AddNewRow(laborDetails.Service_Material,False)
                            row.Product.Attr('ItemQuantity').AssignValue(str(labourFinalHrsDict[labor]))
                contRows.Calculate()
                delRows.reverse()
                for rowindx in delRows:
                    contRows.DeleteRow(rowindx)
                contRows=parentProduct.GetContainerByName('HCI_PHD_LabourProducts').Rows
                mainRow.ApplyProductChanges()
                cont.ApplyProductChanges()