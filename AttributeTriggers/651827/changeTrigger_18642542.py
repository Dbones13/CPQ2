GES_Part = 0
if Product.Attr("AR_HCI_GES Participation %").GetValue():
    participation = float(Product.Attr("AR_HCI_GES Participation %").GetValue())
    decimal_val = participation - int(participation)
    if decimal_val<0.5:
        GES_Part = int(participation)
    else:
        GES_Part = int(participation)+1
Product.Attr("AR_HCI_GES Participation %").AssignValue(str(GES_Part))
Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.ReadOnly
if int(GES_Part) > 0:
    Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Editable
    if Product.GetContainerByName('AR_HCI_SUBPRD').Rows.Count>1:
        row = Product.GetContainerByName('AR_HCI_SUBPRD').Rows[1]
        row.Product.Attributes.GetByName('HCI_PHD_GES_Location').SelectValue(Product.Attributes.GetByName('AR_HCI_GES Location').GetValue())
        ges_loc = row.Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue()
        country_codes = {'GES China':'CN','GES India':'IN','GES Uzbekistan':'UZ'}
        cuntry_code = country_codes.get(ges_loc)
        inpt_lbr = row.Product.GetContainerByName('HCI_Labor_prj_mng_lbr_input').Rows[1]
        inpt_lbr['Percentage']= '10' if int(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue())!= 0 else '0'
        inpt_lbr.GetColumnByName('Activity_Type').ReferencingAttribute.SelectDisplayValue('ADV GES PM-'+str(cuntry_code)+'')
        inpt_lbr.ApplyProductChanges()
        inpt_lbr.Calculate()
        row.Product.Attributes.GetByName('AR_HCI_No_GES_ENG').SelectDisplayValue('1')
        fo_eng = row.Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows[0]
        participation = 100 - int(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue() or 0)
        fo_eng.SetColumnValue('Participation',str(participation))
        fo_eng_ges = row.Product.GetContainerByName('HCI_PHD_GES_Eng').Rows[0]
        fo_eng_ges.SetColumnValue('Activity Type','ADV GES Prin Eng-'+str(cuntry_code)+'')
        fo_eng_ges.SetColumnValue('Participation',str(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue() or 0))
        row.Product.Attributes.GetByName('AR_HCI_ParticipationFlag').AssignValue('True')
        row.Product.Attributes.GetByName('AR_HCI_GES Participation %').AssignValue(str(GES_Part))
        fo_eng_ges = row.Product.GetContainerByName('HCI_PHD_GES_Eng').Rows[0]
        fo_eng_ges.GetColumnByName('Activity Type').ReferencingAttribute.SelectDisplayValue('ADV GES Prin Eng-'+str(cuntry_code)+'')
        fo_eng_ges.Calculate()
        parDictStr=row.Product.Attributes.GetByName('HCI_PHD_ParChildAttr').GetValue()
        parDict=JsonHelper.Deserialize(parDictStr)
        pmLaborDict={}
        contRows=row.Product.GetContainerByName('HCI_Labor_prj_mng_lbr_input').Rows
        for rows in contRows:
            if rows['Percentage'] and  float(rows['Percentage']) != float(0):
                pmLaborDict[rows['Role']]={}
                pmLaborDict[rows['Role']]['Percentage']=rows['Percentage']
                pmLaborDict[rows['Role']]['Activity_Type']=rows['Activity_Type']
                pmLaborDict[rows['Role']]['Country']=rows['Execution Country']
        parDict['pmLaborDict'] = pmLaborDict
        teamStr={}
        contRows=row.Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows[0]
        if contRows['Participation'] and  float(contRows['Participation']) != float(0):
            teamStr[contRows['Engineer']]={}
            teamStr[contRows['Engineer']]['Activity Type']=contRows['Activity Type']
            teamStr[contRows['Engineer']]['Participation']=contRows['Participation']
            teamStr[contRows['Engineer']]['Country']=contRows['Execution Country']
            teamStr[contRows['Engineer']]['NoOfEng']=contRows['Number of trips per engineer']
            teamStr[contRows['Engineer']]['Travel Time']=contRows['Hours per trip']
        contRows=row.Product.GetContainerByName('HCI_PHD_GES_Eng').Rows[0]
        #gesEngContry=Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue()
        if contRows['Participation'] and  float(contRows['Participation']) != float(0):
            contRows['Engineer'] = contRows['Engineer'] if contRows['Engineer'] !='' else 'GES Eng 1'
            teamStr[contRows['Engineer']]={}
            teamStr[contRows['Engineer']]['Activity Type']=contRows['Activity Type']
            teamStr[contRows['Engineer']]['Participation']=contRows['Participation']
            teamStr[contRows['Engineer']]['Country']=ges_loc
            teamStr[contRows['Engineer']]['NoOfEng']=contRows['Number of trips per engineer'] if contRows['Number of trips per engineer'] !='' else '0'
            teamStr[contRows['Engineer']]['Travel Time']=contRows['Hours per trip']
        parDict['teamStr']=teamStr
        jsonStr=JsonHelper.Serialize(parDict)
        Trace.Write(str(jsonStr)+'=jsonStr----hci--'+str(pmLaborDict))
        row.Product.Attributes.GetByName('HCI_PHD_ParChildAttr').AssignValue(jsonStr)
        selectedrows = row.Product.GetContainerByName('HCI_PHD_Selected_Products').Rows
        row.Product.ApplyRules()
        for con in selectedrows:
            con.Product.Attributes.GetByName('HCI_PHD_ParChildAttr').AssignValue(jsonStr)