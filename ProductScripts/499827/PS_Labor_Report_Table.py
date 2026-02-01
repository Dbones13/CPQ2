import GS_Labor_Report_Map_Util as gslrmu
labor_sys_del = {}
Prod_Cont_map = gslrmu.get_Prod_Cont_map()
Cont_col_map = gslrmu.get_Cont_col_map()
prod_idx = 0
salesOrg = ""
Sales_Org_Country = ""
salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
if salesArea:
    Sales_Org_Country = SqlHelper.GetFirst("SELECT Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesArea))
    if Sales_Org_Country:
        salesOrg = Sales_Org_Country.Execution_County
else:
    Log.Info("Sales Area is not Defined for this Qoute")
fo_final_hrs=fo_final_cost=ic_final_hrs=ic_final_cost=fo_final_hrs1=ic_final_hrs1=fo_regional_cost=fo_ges_regional_cost=fo_regional_cost1=fo_ges_regional_cost1=ic_regional_cost=ic_ges_regional_cost=ic_regional_cost1=ic_ges_regional_cost1=GES_ENG=GES_BO_hrs=GES_BO_hrs1=GES_BO_cost_fo=GES_BO_cost_fo1=GES_BO_cost_ges=GES_BO_cost_ges1=GES_BO_cost=GES_OS_hrs=GES_OS_hrs1=GES_OS_cost_fo=GES_OS_cost_fo1=GES_OS_cost_ges=GES_OS_cost_ges1=GES_OS_cost=GES_MS_hrs=GES_MS_hrs1=GES_MS_cost_fo=GES_MS_cost_fo1=GES_MS_cost_ges=GES_MS_cost_ges1=GES_MS_cost=HMI_cost=HMI_hrs=HMI_cost_ges=HMI_cost_fo=HMI_hrs1=HMI_cost_fo1=HMI_cost_ges1=0
Fo_1_split=Fo_2_split=fo_final_hrs2=fo_final_hrs3=ic_1_split=ic_2_split=ic_final_hrs2=ic_final_hrs3=Ges_split_BO=GES_BO_hrs2=Ges_split_OS=GES_OS_hrs2=0

for attr in Prod_Cont_map['New / Expansion Project']:
	cont = Product.GetContainerByName(attr)
	if cont:
		for cont_rows in cont.Rows:
			if salesOrg == cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value:
				Fo_1_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value!='' else 0.0)
				if "Addi" not in attr:
					Fo_2_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value!='' else 0.0)
				else:
					Fo_2_split = 0
				fo_final_hrs =  float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
				fo_final_hrs1 = round(float(fo_final_hrs * Fo_1_split * 0.01))
				fo_final_hrs2 = round(float(fo_final_hrs * Fo_2_split * 0.01))
				fo_final_hrs3 += (fo_final_hrs1 + fo_final_hrs2)
				fo_regional_cost = float(cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0)
				fo_regional_cost1 += fo_regional_cost
			else:
				ic_1_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value!='' else 0.0)
				if "Addi" not in attr:
					ic_2_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value!='' else 0.0)
				else:
					ic_2_split = 0
				ic_final_hrs =  float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
				ic_final_hrs1 = round(float(ic_final_hrs*ic_1_split * 0.01))
				ic_final_hrs2 = round(float(ic_final_hrs*ic_2_split * 0.01))
				ic_final_hrs3 += (ic_final_hrs1+ic_final_hrs2)
				ic_regional_cost = float(cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0)
				ic_regional_cost1 += ic_regional_cost
			GES_ENG = str(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue) if cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
			if GES_ENG[-5] == "B":
				Ges_split_BO = float(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value!='' else 0.0)
				GES_BO_hrs = float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
				GES_BO_hrs1 = round(float(GES_BO_hrs * Ges_split_BO * 0.01))
				GES_BO_hrs2 += GES_BO_hrs1
				GES_BO_cost_ges = float(cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value!='' else 0.0)
				GES_BO_cost_ges1 += GES_BO_cost_ges
			elif GES_ENG[-5] == "F":
				Ges_split_OS = float(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value!='' else 0.0)
				GES_OS_hrs = float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
				GES_OS_hrs1 = round(float(Ges_split_OS * GES_OS_hrs * 0.01))
				GES_OS_hrs2 += GES_OS_hrs1
				GES_OS_cost_ges = float(cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value!='' else 0.0)
				GES_OS_cost_ges1 += GES_OS_cost_ges
New_Exp_Cnt = Product.GetContainerByName('CE_SystemGroup_Cont')
if New_Exp_Cnt is not None:
    for sys_grp_row in New_Exp_Cnt.Rows:
        sys_grp_prouct = sys_grp_row.Product
        
        if sys_grp_row.GetColumnByName("Include_Generic_System").Value == "Yes":
            sys_grp_generic_cnt = sys_grp_prouct.GetContainerByName('PMC_Generic_System_Cont')
            if sys_grp_generic_cnt.Rows.Count > 0:
                for sys_grp_generic_prods in sys_grp_generic_cnt.Rows:
                    quote_generic_prds = sys_grp_generic_prods.Product
                    for generic_prd in Prod_Cont_map:
                        if generic_prd == quote_generic_prds.Name:
                            for generic_attr in Prod_Cont_map[generic_prd]:
                                generic_cont = quote_generic_prds.GetContainerByName(generic_attr)
                                if generic_cont:
                                    for generic_cont_rows in generic_cont.Rows:
                                        if salesOrg == generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][10]).Value:
                                            Fo_1_split = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][7]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][7]).Value!='' else 0.0)
                                            if "Addi" not in generic_attr:
                                                Fo_2_split = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][9]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][9]).Value!='' else 0.0)
                                            else:
                                                Fo_2_split = 0
                                            fo_final_hrs =  float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value!='' else 0.0)
                                            fo_final_hrs1 = round(float(fo_final_hrs * Fo_1_split * 0.01))
                                            fo_final_hrs2 = round(float(fo_final_hrs * Fo_2_split * 0.01))
                                            fo_final_hrs3 += fo_final_hrs1 + fo_final_hrs2
                                            fo_regional_cost = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][12]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][12]).Value!='' else 0.0)
                                            fo_regional_cost1 += fo_regional_cost
                                        else:
                                            ic_1_split = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][7]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][7]).Value!='' else 0.0)
                                            if "Addi" not in generic_attr:
                                                ic_2_split = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][9]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][9]).Value!='' else 0.0)
                                            else:
                                                ic_2_split = 0
                                            ic_final_hrs =  float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value!='' else 0.0)
                                            ic_final_hrs1 = round(float(ic_final_hrs*ic_1_split * 0.01))
                                            ic_final_hrs2 = round(float(ic_final_hrs*ic_2_split * 0.01))
                                            ic_final_hrs3 += (ic_final_hrs1+ic_final_hrs2)
                                            ic_regional_cost = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][12]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][12]).Value!='' else 0.0)
                                            ic_regional_cost1 += ic_regional_cost
                                        GES_ENG = str(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue) if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
                                        if GES_ENG[-5] == "B":
                                            Ges_split_BO = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][5]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][5]).Value!='' else 0.0)
                                            GES_BO_hrs = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value!='' else 0.0)
                                            GES_BO_hrs1 = round(float(GES_BO_hrs * Ges_split_BO * 0.01))
                                            GES_BO_hrs2 += GES_BO_hrs1
                                            GES_BO_cost_ges = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][13]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][13]).Value!='' else 0.0)
                                            GES_BO_cost_ges1 += GES_BO_cost_ges
                                        elif GES_ENG[-5] == "F":
                                            Ges_split_OS = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][5]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][5]).Value!='' else 0.0)
                                            GES_OS_hrs = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value!='' else 0.0)
                                            GES_OS_hrs1 = round(float(Ges_split_OS * GES_OS_hrs * 0.01))
                                            GES_OS_hrs2 += GES_OS_hrs1
                                            GES_OS_cost_ges = float(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][13]).Value if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][13]).Value!='' else 0.0)
                                            GES_OS_cost_ges1 += GES_OS_cost_ges
                                        
        
        sys_grp_cnt = sys_grp_prouct.GetContainerByName('CE_System_Cont')
        if sys_grp_cnt is not None:
            for sys_grp_prods in sys_grp_cnt.Rows:
                quote_prds = sys_grp_prods.Product
                for prod in Prod_Cont_map:
                    if prod == quote_prds.Name:
                        Log.Info("Product -> "+prod)
                        for attr in Prod_Cont_map[prod]:
                            cont = quote_prds.GetContainerByName(attr)
                            Log.Info("Attribute -> "+attr)
                            if cont:
                                if attr == "HMI_Engineering_Labor_Container":
                                    for cont_rows in cont.Rows:
                                        HMI_hrs = cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0
                                        HMI_hrs1 += float(HMI_hrs)
                                        HMI_cost_fo1 = cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0
                                        HMI_cost_ges1 = cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value!='' else 0.0
                                        HMI_cost_fo += float(HMI_cost_fo1)
                                        HMI_cost_ges += float(HMI_cost_ges1)
                                        HMI_cost = HMI_cost_fo + HMI_cost_ges       
                                for cont_rows in cont.Rows: 
                                    if prod == "Measurement IQ System":
                                        if salesOrg == cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value:
                                            Fo_1_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value!='' else 0.0)
                                            fo_final_hrs =  float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
                                            fo_final_hrs1 = round(float(fo_final_hrs * Fo_1_split * 0.01))
                                            fo_final_hrs3 += fo_final_hrs1
                                            fo_regional_cost = float(cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0)
                                            fo_regional_cost1 += fo_regional_cost
                                        else:
                                            ic_1_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value!='' else 0.0)
                                            ic_final_hrs =  float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
                                            ic_final_hrs1 = round(float(ic_final_hrs*ic_1_split * 0.01))
                                            ic_final_hrs3 += ic_final_hrs1
                                            ic_regional_cost = float(cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0)
                                            ic_regional_cost1 += ic_regional_cost
                                    else:
                                        if salesOrg == cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value:
                                            Fo_1_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value!='' else 0.0)
                                            if "Addi" not in attr:
                                                Fo_2_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value!='' else 0.0)
                                            else:
                                                Fo_2_split = 0
                                            fo_final_hrs =  float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
                                            fo_final_hrs1 = round(float(fo_final_hrs * Fo_1_split * 0.01))
                                            fo_final_hrs2 = round(float(fo_final_hrs * Fo_2_split * 0.01))
                                            fo_final_hrs3 += fo_final_hrs1 + fo_final_hrs2
                                            fo_regional_cost = float(cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0)
                                            fo_regional_cost1 += fo_regional_cost
                                        else:
                                            ic_1_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value!='' else 0.0)
                                            if "Addi" not in attr:
                                                ic_2_split = float(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value!='' else 0.0)
                                            else:
                                                ic_2_split = 0
                                            ic_final_hrs =  float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
                                            ic_final_hrs1 = round(float(ic_final_hrs*ic_1_split * 0.01))
                                            ic_final_hrs2 = round(float(ic_final_hrs*ic_2_split * 0.01))
                                            ic_final_hrs3 += (ic_final_hrs1+ic_final_hrs2)
                                            ic_regional_cost = float(cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value!='' else 0.0)
                                            ic_regional_cost1 += ic_regional_cost
                                        GES_ENG = str(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue) if cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
                                        if GES_ENG[-5] == "B":
                                            Ges_split_BO = float(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value!='' else 0.0)
                                            GES_BO_hrs = float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
                                            GES_BO_hrs1 = round(float(GES_BO_hrs * Ges_split_BO * 0.01))
                                            GES_BO_hrs2 += GES_BO_hrs1
                                            GES_BO_cost_ges = float(cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value!='' else 0.0)
                                            GES_BO_cost_ges1 += GES_BO_cost_ges
                                        elif GES_ENG[-5] == "F":
                                            Ges_split_OS = float(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value!='' else 0.0)
                                            GES_OS_hrs = float(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value!='' else 0.0)
                                            GES_OS_hrs1 = round(float(Ges_split_OS * GES_OS_hrs * 0.01))
                                            GES_OS_hrs2 += GES_OS_hrs1
                                            GES_OS_cost_ges = float(cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value if cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value!='' else 0.0)
                                            GES_OS_cost_ges1 += GES_OS_cost_ges

    QT_Table = Quote.QuoteTables["Labor_Report_Table"]
    QT_Table.Rows.Clear()
    newRow = QT_Table.AddNewRow()
    newRow['Front_Office_Labor_Final_Hrs'] = fo_final_hrs3
    newRow['Intercompany_Labor_Final_Hrs'] = ic_final_hrs3
    newRow['Front_Office_Labor_Total_Cost'] = fo_regional_cost1
    newRow['Intercompany_Labor_Total_Cost'] = ic_regional_cost1
    newRow['GES_Back_office_Labor_Final_Hrs'] = GES_BO_hrs2
    newRow['GES_Back_office_Labor_Total_Cost'] = GES_BO_cost_ges1
    newRow['GES_On_site_Labor_Final_Hrs'] = GES_OS_hrs2
    newRow['GES_On_site_Labor_Total_Cost'] = GES_OS_cost_ges1
    newRow['Miscellaneous_Labor_Final_Hrs'] = GES_MS_hrs1
    newRow['Miscellaneous_Labor_Total_Cost'] = GES_MS_cost
    newRow['HMI_Labor_Final_Hrs'] = HMI_hrs1
    newRow['HMI_Labor_Total_Cost'] = HMI_cost
    newRow['Sales_Org_Country'] = salesOrg
    QT_Table.Save()
    Log.Info('fo_final_hrs3--'+str(fo_final_hrs3)+'--ic_final_hrs3--'+str(ic_final_hrs3)+'--fo_regional_cost1--'+str(fo_regional_cost1)+'--ic_regional_cost1--'+str(ic_regional_cost1)+'--GES_BO_hrs2--'+str(GES_BO_hrs2)+'--GES_BO_cost_ges1--'+str(GES_BO_cost_ges1)+'--GES_OS_hrs2--'+str(GES_OS_hrs2)+'--GES_OS_cost_ges1--'+str(GES_OS_cost_ges1)+'--GES_MS_hrs1--'+str(GES_MS_hrs1)+'--GES_MS_cost--'+str(GES_MS_cost)+'--HMI_hrs1--'+str(HMI_hrs1)+'--HMI_cost--'+str(HMI_cost)+'--salesOrg--'+str(salesOrg))