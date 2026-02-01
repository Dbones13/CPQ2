import GS_Labor_Report_Util

labor_sys_del = []
sys_grp_name = ''

Prod_Cont_map = GS_Labor_Report_Util.Master_Prod_Cont_map
Cont_col_map = GS_Labor_Report_Util.Master_Cont_col_map
Cont_Labor_map = GS_Labor_Report_Util.Master_Cont_Labor_map

salesOrg = ""
Sales_Org_Country = ""
salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
if salesArea:
    Sales_Org_Country = SqlHelper.GetFirst("SELECT Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesArea))
    if Sales_Org_Country:
        salesOrg = Sales_Org_Country.Execution_County
else:
    Trace.Write("Sales Area is not Defined for this Qoute")
Trace.Write("Product Name---Qoute"+str(dir(Product)))
if Product.Name == 'New / Expansion Project':
    Trace.Write("1. Found")
    #Trace.Write(Item.ProductName)
    #Trace.Write(Item.PartNumber)
    for prod in Prod_Cont_map:
        if prod == Product.Name:
            Trace.Write("2. Found")
            #Trace.Write(Item.ProductName)
            #Item.EditConfiguration()
            for attr in Prod_Cont_map[prod]:
                Trace.Write(attr)
                cont = Product.GetContainerByName(attr)
                if cont:
                    for cont_rows in cont.Rows:
                        del_list = []
                        del_list.append(Product.Name)
                        del_list.append(Product.PartNumber)
                        del_list.append(attr)
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][0]).Value)
                        if "Addi" not in attr:
                            del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][1]).Value)
                            del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][2]).Value)
                        else:
                            del_list.append(0)
                            del_list.append(0)
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value)
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue)
                        ges_eng = str(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue) if cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value)
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue)
                        fo_1 = cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value)
                        if "Addi" not in attr:
                            del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue)
                            fo_2 = cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue
                            del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value)
                        else:
                            del_list.append('')
                            fo_2 = ''
                            del_list.append(0)
                        Exe_Country = cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value)
                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][11]).Value)
                        fo_cost = cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value
                        if fo_cost == '' or fo_cost == None:
                            del_list.append(0)
                        else:
                            del_list.append(fo_cost)
                        ges_cost = cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value
                        if ges_cost == '' or ges_cost == None:
                            del_list.append(0)
                        else:
                            del_list.append(ges_cost)
                        plsg = ''
                        if fo_1 != '' or fo_1 != None:
                            plsg = GS_Labor_Report_Util.get_plsg(fo_1)
                        elif fo_2 != '' or fo_2 != None:
                            plsg = GS_Labor_Report_Util.get_plsg(fo_2)
                        del_list.append(plsg)
                        ges_plsg = ''
                        if ges_eng != '' and ges_eng != None:
                            ges_plsg = GS_Labor_Report_Util.get_plsg(ges_eng)
                        del_list.append('Project')
                        if Exe_Country == salesOrg:
                            del_list.append('Front Office Labor')
                        else:
                            del_list.append('Intercompany Labor')
                        if ges_eng[-5] == "B":
                            del_list.append('GES Back -office Labor')
                        elif ges_eng[-5] == "F":
                            del_list.append('GES On-site Labor')
                        else:
                            del_list.append('')
                        del_list.append(salesOrg)
                        lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
                        del_list.append(lob_labor)
                        ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
                        del_list.append(ges_lob_labor)
                        del_list.append(ges_plsg)
                        labor_sys_del.append(del_list)
New_Exp_Cnt = Product.GetContainerByName('CE_SystemGroup_Cont')
if New_Exp_Cnt is not None:
    for sys_grp_row in New_Exp_Cnt.Rows:
        sys_grp_prouct = sys_grp_row.Product
        sys_grp_name = sys_grp_row.GetColumnByName('Child Product Name').Value
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
                                        del_list = []
                                        del_list.append(quote_generic_prds.Name)
                                        del_list.append(sys_grp_generic_prods.GetColumnByName('Generic System Name').Value)
                                        del_list.append(generic_attr)
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][0]).Value)
                                        if "Addi" not in generic_attr:
                                            del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][1]).Value)
                                            del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][2]).Value)
                                        else:
                                            del_list.append(0)
                                            del_list.append(0)
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value)
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue)
                                        ges_eng = str(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue) if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][5]).Value)
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][6]).DisplayValue)
                                        fo_1 = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][6]).DisplayValue
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][7]).Value)
                                        if "Addi" not in generic_attr:
                                            del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][8]).DisplayValue)
                                            fo_2 = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][8]).DisplayValue
                                            del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][9]).Value)
                                        else:
                                            del_list.append('')
                                            fo_2 = ''
                                            del_list.append(0)
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][10]).Value)
                                        Exe_Country = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][10]).Value
                                        del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][11]).Value)
                                        fo_cost = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][12]).Value
                                        if fo_cost == '' or fo_cost == None:
                                            del_list.append(0)
                                        else:
                                            del_list.append(fo_cost)
                                        ges_cost = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][13]).Value
                                        if ges_cost == '' or ges_cost == None:
                                            del_list.append(0)
                                        else:
                                            del_list.append(ges_cost)
                                        plsg = ''
                                        if fo_1 != '' or fo_1 != None:
                                            plsg = GS_Labor_Report_Util.get_plsg(fo_1)
                                        elif fo_2 != '' or fo_2 != None:
                                            plsg = GS_Labor_Report_Util.get_plsg(fo_2)
                                        del_list.append(plsg)
                                        ges_plsg = ''
                                        if ges_eng != '' and ges_eng != None:
                                            ges_plsg = GS_Labor_Report_Util.get_plsg(ges_eng)
                                        del_list.append(sys_grp_name)
                                        if Exe_Country == salesOrg:
                                            del_list.append('Front Office Labor')
                                        else:
                                            del_list.append('Intercompany Labor')
                                        if ges_eng[-5] == "B":
                                            del_list.append('GES Back -office Labor')
                                        elif ges_eng[-5] == "F":
                                            del_list.append('GES On-site Labor')
                                        else:
                                            del_list.append('')
                                        del_list.append(salesOrg)
                                        lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
                                        del_list.append(lob_labor)
                                        ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
                                        del_list.append(ges_lob_labor)
                                        del_list.append(ges_plsg)
                                        labor_sys_del.append(del_list)
        sys_grp_cnt = sys_grp_prouct.GetContainerByName('CE_System_Cont')
        for sys_grp_prods in sys_grp_cnt.Rows:
            quote_prds = sys_grp_prods.Product
            for prod in Prod_Cont_map:
                if prod == quote_prds.Name:
                    #Trace.Write("2. Found")
                    #Trace.Write(quote_prds.Name)
                    for attr in Prod_Cont_map[prod]:
                        #Trace.Write(attr)
                        cont = quote_prds.GetContainerByName(attr)
                        if cont:
                            for cont_rows in cont.Rows:
                                del_list = []
                                del_list.append(quote_prds.Name)
                                del_list.append(sys_grp_prods.GetColumnByName('Product Name').Value)
                                del_list.append(attr)
                                del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][0]).Value)
                                if "Addi" not in attr:
                                    del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][1]).Value)
                                    del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][2]).Value)
                                else:
                                    del_list.append(0)
                                    del_list.append(0)
                                del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value)
                                if prod == "Measurement IQ System":
                                    del_list.append('')
                                    ges_eng = "SYS GES Eng-XO-CN"
                                    del_list.append(0)
                                    del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][6]).Value)
                                    fo_1 = cont_rows.GetColumnByName(Cont_col_map[attr][6]).Value
                                else:
                                    del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue)
                                    ges_eng = str(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue) if cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
                                    del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value)
                                    del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue)
                                    fo_1 = cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue
                                del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value)
                                if "Addi" not in attr:
                                    if prod == "Measurement IQ System":
                                        del_list.append('')
                                        fo_2 = ''
                                        del_list.append(0)
                                    else:
                                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue)
                                        fo_2 = cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue
                                        del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value)
                                else:
                                    del_list.append('')
                                    fo_2 = ''
                                    del_list.append(0)
                                del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value)
                                Exe_Country = cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value
                                del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][11]).Value)
                                fo_cost = cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value
                                if fo_cost == '' or fo_cost == None:
                                    del_list.append(0)
                                else:
                                    del_list.append(fo_cost)
                                if prod == "Measurement IQ System":
                                    del_list.append(0)
                                else:
                                    ges_cost = cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value
                                    if ges_cost == '' or ges_cost == None:
                                        del_list.append(0)
                                    else:
                                        del_list.append(ges_cost)
                                plsg = ''
                                if fo_1 != '' or fo_1 != None:
                                    plsg = GS_Labor_Report_Util.get_plsg(fo_1)
                                elif fo_2 != '' or fo_2 != None:
                                    plsg = GS_Labor_Report_Util.get_plsg(fo_2)
                                del_list.append(plsg)
                                ges_plsg = ''
                                if ges_eng != '' and ges_eng != None:
                                    ges_plsg = GS_Labor_Report_Util.get_plsg(ges_eng)
                                del_list.append(sys_grp_name)
                                if Exe_Country == salesOrg:
                                    del_list.append('Front Office Labor')
                                else:
                                    del_list.append('Intercompany Labor')
                                if ges_eng[-5] == "B":
                                    del_list.append('GES Back -office Labor')
                                elif ges_eng[-5] == "F":
                                    del_list.append('GES On-site Labor')
                                else:
                                    del_list.append('')
                                del_list.append(salesOrg)
                                lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
                                del_list.append(lob_labor)
                                ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
                                del_list.append(ges_lob_labor)
                                del_list.append(ges_plsg)
                                labor_sys_del.append(del_list)
    GS_Labor_Report_Util.Store_Lbr_Dtls_in_QT(Quote, Cont_Labor_map, labor_sys_del)