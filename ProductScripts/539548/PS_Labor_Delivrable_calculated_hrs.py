isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    def isFloat(val):
        if val is not None and val != '':
            try:
                float(val)
                return True
            except:
                return False
        return False

    def getfloat(val):
        if val:
            try:
                return float(val)
            except:
                return 0
        return 0
    def getContainer(Name):
        return Product.GetContainerByName(Name)

    def getFinalhr(oldCalHrs,calc,prod,oldFinalHrs,final_hr,row):
        if (getfloat(calc) == 0.0) and (getfloat(oldCalHrs) != 0.0):
            final = getfloat(oldFinalHrs)
            row["Adjustment_Productivity"] = "1"
        elif getfloat(calc) == getfloat(oldCalHrs):
            final=final_hr
        else:
            final = round(calc * prod)
        return final

    '''selectedProducts = list()
    for row in getContainer("MSID_Product_Container").Rows:
        selectedProducts.append(row["Product Name"])'''
    # msidCont = Product.GetContainerByName("CONT_MSID_SUBPRD")
    # for row in msidCont.Rows:
    # 		#if row["Selected_Products"] == "OPM":
    # 	Product = row.Product
    # 	selectedProducts = row["Selected_Products"]

    scope = Product.Attr('MIgration_Scope_Choices').GetValue()
    #scope = Product.Attr('Scope').GetValue()
    Trace.Write("scope::"+str(scope))

    def calculatedhours(Msid_Product,laborCont, modulename):
        Trace.Write("modulename::"+str(laborCont))
        Msid_Product.ExecuteRulesOnce = True
        if modulename == "3rd Party PLC to ControlEdge PLC/UOC":
            Trace.Write("test::")
            tableLabor = SqlHelper.GetList("select Deliverables,Calculate_hrs,Deliverable_Type from TABLE_3RD_PARTY_PLC_UOC_LABOR_DELIVERABLES where Calculate_hrs != ''")
        elif modulename == "Virtualization System":
            tableLabor = SqlHelper.GetList("select Deliverables,Calculate_hrs,Deliverable_Type from VIRTUALIZATION_LABOR_DELIVERABLES where Calculate_hrs != ''")
        elif modulename == "Generic System":
            tableLabor = SqlHelper.GetList("select Deliverables,Calculate_hrs,Deliverable_Type from GENERIC_LABOR_DELIVERABLES where Calculate_hrs != ''")
        elif modulename == "QCS RAE Upgrade":
            tableLabor = SqlHelper.GetList("select Deliverables,Calculate_hrs,Deliverable_Type from QCS_RAE_UPGRADE_LABOR_DELIVERABLES_MSID where Calculate_hrs != ''")
        elif modulename == "TPA/PMD Migration":
            tableLabor = SqlHelper.GetList("select Deliverables,Calculate_hrs,Deliverable_Type from TPAPMD_MIGRATION_LABOR_DELIVERABLES where Calculate_hrs != ''")
        elif modulename == "ELEPIU ControlEdge RTU Migration Engineering":
            tableLabor = SqlHelper.GetList("select Deliverables,Calculate_hrs,Deliverable_Type from ELEPIU_MIGRATION_LABOR_DELIVERABLES where Calculate_hrs != ''")
        calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
        offsite_deliverables = []
        onsite_deliverables = []
        total_onsite = 0
        total_offsite = 0
        total_final_onsite = 0
        total_final_offsite = 0
        _dict = {"Total":0, "Off-Site":0, "On-Site":0}
        for x in tableLabor:
            #calc_name_dict[x.Deliverables] = x.Calculate_hrs
            if x.Deliverable_Type == "Offsite":
                #Trace.Write(x.Deliverables)
                offsite_deliverables.append(x.Deliverables)
                Trace.Write("test1234::"+str(Msid_Product.Attr(x.Calculate_hrs).GetValue()))
                if isFloat(Msid_Product.Attr(x.Calculate_hrs).GetValue()):
                    cal_hrs = float(Msid_Product.Attr(x.Calculate_hrs).GetValue()) if Msid_Product.Attr(x.Calculate_hrs).GetValue() != '' else 0
                    Trace.Write("cal_hrs::"+str(cal_hrs))
                    total_offsite = total_offsite + cal_hrs
                    calc_name_dict[x.Deliverables] = cal_hrs
                else:
                    cal_hrs = 0
                    total_offsite = total_offsite + cal_hrs
                    calc_name_dict[x.Deliverables] = cal_hrs
            else:
                onsite_deliverables.append(x.Deliverables)
                cal_hrs = float(Msid_Product.Attr(x.Calculate_hrs).GetValue()) if Msid_Product.Attr(x.Calculate_hrs).GetValue() != '' else 0
                total_onsite = total_onsite + cal_hrs
                calc_name_dict[x.Deliverables] = cal_hrs
        Trace.Write('1111')
        for row in laborCont.Rows:
            Trace.Write('222')
            oldCalHrs = row["Calculated_Hrs"]
            Trace.Write("oldCalHrs::"+str(oldCalHrs))
            oldFinalHrs = row["Final_Hrs"]
            Trace.Write("oldFinalHrs::"+str(oldFinalHrs))
            deliverable = row.GetColumnByName("Deliverable").Value
            if deliverable in calc_name_dict.keys() : #and not isFloat(calc_name_dict[deliverable]):
                calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]  #Get the calculated value of deliverable
                Trace.Write("calc name: {0}".format(row.GetColumnByName("Deliverable").Value))
                try:
                    row.GetColumnByName("Calculated_Hrs").Value = str(round(calc_name,2))
                    if row.GetColumnByName("Calculated_Hrs").Value == '':
                        row.GetColumnByName("Calculated_Hrs").Value = str(0)
                    final_hr = getfloat(row.GetColumnByName('Final_Hrs').Value)
                    calc = getfloat(row.GetColumnByName('Calculated_Hrs').Value)
                    prod = getfloat(row.GetColumnByName('Adjustment_Productivity').Value)
                    final = getFinalhr(oldCalHrs,calc,prod,oldFinalHrs,final_hr,row)
                    #if getfloat(calc) == getfloat(oldCalHrs): final=final_hr
                    #else : final = round(calc * prod)
                    if row.GetColumnByName("Deliverable").Value in offsite_deliverables:
                        total_final_offsite = total_final_offsite + final
                    else:
                        total_final_onsite = total_final_onsite + final
                    row.GetColumnByName('Final_Hrs').Value = str(getfloat(final))
                except Exception,e:
                    msg = "Error when Calculating Hours for: {0}, Error: {1}".format(calc_name, e)
                    Product.ErrorMessages.Add(msg)
                    Trace.Write(msg)
                    Log.Error(msg)
            else:
                if deliverable not in ["On-Site", "Off-Site", "Total"]:
                    final_hr = getfloat(row.GetColumnByName('Final_Hrs').Value)
                    if row["Deliverable_Type"] in ("Offsite","Off-Site"):
                        total_final_offsite = total_final_offsite + final_hr
                    else:
                        total_final_onsite = total_final_onsite + final_hr
                _dict[row.GetColumnByName("Deliverable").Value] = row.RowIndex
        Trace.Write('2222')
        for k in _dict:
            if k == "Total":
                laborCont.Rows[_dict[k]]["Calculated_Hrs"] = str(round((total_offsite + total_onsite),2))
                laborCont.Rows[_dict[k]]["Final_Hrs"] = str(total_final_offsite + total_final_onsite)
            if k == "Off-Site":
                laborCont.Rows[_dict[k]]["Calculated_Hrs"] = str(round(total_offsite,2))
                laborCont.Rows[_dict[k]]["Final_Hrs"]  = str(total_final_offsite)
            if k == "On-Site":
                laborCont.Rows[_dict[k]]["Calculated_Hrs"] = str(round(total_onsite,2))
                laborCont.Rows[_dict[k]]["Final_Hrs"] = str(total_final_onsite)
        laborCont.Calculate()
        Product.ExecuteRulesOnce = False

    if scope == 'HW/SW/LABOR' or scope == 'LABOR': #and ('3rd Party PLC to ControlEdge PLC/UOC' in selectedProducts or 'Virtualization System' in selectedProducts):
        plcuocCon = getContainer('3rd_Party_PLC_UOC_Labor')
        VirtualizationCon = getContainer('MSID_Labor_Virtualization_con')
        QCSCon = getContainer('MSID_Labor_QCS_RAE_Upgrade_con')
        TPACon = getContainer('MSID_Labor_TPA_con')
        ELEPIUCon = getContainer('MSID_Labor_ELEPIU_con')
        gensyscount = 0
        msidCont = Product.GetContainerByName("CONT_MSID_SUBPRD")
        for genrow in msidCont.Rows:
            if 'Generic System' in genrow['Product Name']:
                gensyscount = int(str(genrow['Product Name']).split()[-1])
        for row in msidCont.Rows:
            selectedProducts = row["Selected_Products"]
            Msid_Product = row.Product
            Trace.Write("selectedProducts::"+str(selectedProducts))
            #if selectedProducts == 'Virtualization System Migration':
                #Virtualization_hidden_cont = Product.GetContainerByName("MSID_Product_Container_Virtualization_hidden")
                #if Virtualization_hidden_cont.Rows.Count == 0:
                    #newRowVir = Virtualization_hidden_cont.AddNewRow('Virtualization_System_Migration_cpq')
                    #newRowVir['Product Name'] = "Virtualization System"
                    #newRowVir.ApplyProductChanges()
            calculatedhours(Msid_Product,plcuocCon,"3rd Party PLC to ControlEdge PLC/UOC") if "3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts and plcuocCon.Rows.Count > 0 else 0
            calculatedhours(Product,VirtualizationCon,"Virtualization System") if "Virtualization System" in selectedProducts  else 0
            calculatedhours(Msid_Product,QCSCon,"QCS RAE Upgrade") if "QCS RAE Upgrade" in selectedProducts and QCSCon.Rows.Count > 0 else 0
            calculatedhours(Msid_Product,TPACon,"TPA/PMD Migration") if "TPA/PMD Migration" in selectedProducts and TPACon.Rows.Count > 0 else 0
            calculatedhours(Msid_Product,ELEPIUCon,"ELEPIU ControlEdge RTU Migration Engineering") if "ELEPIU ControlEdge RTU Migration Engineering" in selectedProducts and ELEPIUCon.Rows.Count > 0 else 0
            if 'Generic System Migration' in selectedProducts:
                for i in range(1,gensyscount+1):
                    gen_cont=getContainer('MSID_Labor_Generic_System'+str(i)+'_Cont')
                    calculatedhours(Msid_Product,gen_cont,"Generic System")