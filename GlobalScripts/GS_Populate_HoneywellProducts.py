from CF_UTILS import split_after_comma

def populateQuoteTableRow(table, dataDict, row = None):
    if not row:
        row = table.AddNewRow()
    for key, value in dataDict.items():
        row[key] = value 

def populate_PHPLPtable():
    for qitem in Quote.MainItems:
        #fp_plant = None
        phplp_query = SqlHelper.GetFirst("SELECT * FROM QT__PMC_Honeywell_Honeywell_Private_Label_Products  WHERE CartItemGUID='{}'".format(qitem.QuoteItemGuid))

        #plant_country = {"Juarez":"Juarez, Mexico","Pune":"Pune, India", "Tianjin":"Tianjin, China", "Delft":"Delft, the Netherlands", "Roswell/ TruStop":"Roswell, USA", "Kassel":"Kassel, Germany"}

        #plsg_data = SqlHelper.GetFirst("SELECT PLSG FROM HPS_PRODUCTS_MASTER WHERE  PartNumber = '{}'".format(qitem.PartNumber))

        #if plsg_data is not None:
            #coi_data = SqlHelper.GetFirst("SELECT Country_of_Origin FROM QT__Country_of_Origin WHERE Product_Line_Sub_Group = '{}'".format(plsg_data.PLSG))
            #if coi_data is not None:
                #fp_plant = SqlHelper.GetFirst("SELECT Plant FROM COUNTRY_OF_ORIGIN_PLSG_MAPPING WHERE VC_Model = '{}' and Country_of_Origin = '{}'".format(qitem.PartNumber, coi_data.Country_of_Origin))

        query = ("SELECT PRODUCT_CATALOG_CODE,IsSimple FROM PRODUCTS A JOIN product_versions B ON A.PRODUCT_ID = B.PRODUCT_ID left join HPS_PRODUCTS_MASTER hps on hps.PartNumber = A.PRODUCT_CATALOG_CODE WHERE A.PRODUCT_ACTIVE = 'True' AND A.PRODUCT_CATALOG_CODE In ('{}') AND (B.version_end_date IS NULL  or B.version_end_date <= getdate()) ").format(qitem.PartNumber)
        simpProd_query = SqlHelper.GetFirst(query)
        if phplp_query is not None:
            # Update records
            Trace.Write('Update record')
            Trace.Write('SR U ItemNumber:'+str(qitem.RolledUpQuoteItem)+':'+qitem.PartNumber)
            Trace.Write('SR U ListPrice:'+ str(qitem.ListPrice))
            for j in HWProducts_table.Rows:
                if j['CartItemGUID']==qitem.QuoteItemGuid:
                    j['Product_Line']=qitem.QI_ProductLineDesc.Value
                    j['List_Price_Unit'] = float(qitem.ListPrice)
                    j['Customer_Discount']=float(qitem.QI_MPA_Discount_Percent.Value) #float(qitem.QI_Additional_Discount_Percent.Value)
                    j['Unit_Sell_Price']=float(qitem.NetPrice)
                    j['Quantity']=qitem.Quantity
                    j['Extended_List_Price']=float(qitem.ExtendedListPrice)
                    j['Total_Discount_on_List_Price']=float(qitem.QI_Additional_Discount_Amount.Value)
                    j['Extended_Sell_Price']=float(qitem.ExtendedAmount)
                    j["Cost_Price"]=float(qitem.Cost)
                    j["Unit_Cost_Price"] = j["Cost_Price"]
                    j["Extended_Cost_Price"] = qitem.Quantity * j["Unit_Cost_Price"]
                    j["Sell_Price_WithGasETOPrice"] = float(qitem.QI_NetPrice_With_ETO.Value)
                    j["Y_special_Cost_Price"] = float(qitem.QI_REGIONAL_ETO_COST.Value)
                    yspec_query = SqlHelper.GetList("SELECT Yspecial_Quote FROM QT__Yspecial_Selection  WHERE CartItemGUID='{}'".format(qitem.QuoteItemGuid))
                    eto_query = SqlHelper.GetList("SELECT ETO_Ref_No FROM QT__PMC_ETO_Selection WHERE CartItemGUID = '{}'".format(qitem.QuoteItemGuid))
                    lv_yspec_list=''
                    lv_eto_list=''
                    if yspec_query is not None:
                        for i in yspec_query:
                            lv_yspec_list += i.Yspecial_Quote+ ','
                    if eto_query is not None:
                        for i in eto_query:
                            lv_eto_list += i.ETO_Ref_No+ ','
                    j['Specials_Quote_Number_Y_specials_quote_or_ETO_Control_number_']=lv_yspec_list+lv_eto_list
                    full_plant_value = qitem.QI_Plant.Value
                    plant_code,plant_name = split_after_comma(full_plant_value)
                    j['Supplying_Plant']=plant_name
                    '''if fp_plant is not None:
                        if plant_country.get(fp_plant.Plant):
                            fp = plant_country[fp_plant.Plant]
                            j.SetColumnValue("Supplying_Plant",fp)
                        else:
                            j.SetColumnValue("Supplying_Plant","")'''
                HWProducts_table.Save()
        else:
            #New Record- Insert
            HWProducts_table_row={}
            if simpProd_query is not None:
                if qitem.PartNumber not in write_ins:
                    lv_PartNumber = qitem.PartNumber if qitem['QI_FME'].Value == '' else qitem['QI_FME'].Value
                    HWProducts_table_row["ItemNumber"]=qitem.RolledUpQuoteItem
                    HWProducts_table_row["Full_Model_Number"] = lv_PartNumber
                    HWProducts_table_row["PartNumber"] = qitem.PartNumber
                    Trace.Write('SR ListPrice:'+ str(qitem.ListPrice))
                    Trace.Write('SR QI_Additional_Discount_Percent:'+ str(qitem.QI_Additional_Discount_Percent.Value))
                    Trace.Write('SR Extended_List_Price:'+ str(qitem.ExtendedListPrice))
                    HWProducts_table_row["Product_Line"]=qitem.QI_ProductLineDesc.Value
                    HWProducts_table_row["List_Price_Unit"] = float(qitem.ListPrice)
                    HWProducts_table_row["Customer_Discount"]=float(qitem.QI_MPA_Discount_Percent.Value) #float(qitem.QI_Additional_Discount_Percent.Value)
                    HWProducts_table_row["Unit_Sell_Price"]=float(qitem.NetPrice)
                    HWProducts_table_row["Quantity"]=qitem.Quantity
                    HWProducts_table_row["Extended_List_Price"]=float(qitem.ExtendedListPrice)
                    HWProducts_table_row["Total_Discount_on_List_Price"]=float(qitem.QI_Additional_Discount_Amount.Value)
                    HWProducts_table_row["Extended_Sell_Price"]=float(qitem.ExtendedAmount)
                    HWProducts_table_row["Cost_Price"]=float(qitem.Cost)
                    HWProducts_table_row["Unit_Cost_Price"] = HWProducts_table_row["Cost_Price"]
                    HWProducts_table_row["Extended_Cost_Price"] = qitem.Quantity * HWProducts_table_row["Unit_Cost_Price"]
                    HWProducts_table_row["Sell_Price_WithGasETOPrice"] = float(qitem.QI_NetPrice_With_ETO.Value)
                    HWProducts_table_row["Y_special_Cost_Price"] = float(qitem.QI_REGIONAL_ETO_COST.Value)
                    HWProducts_table_row["CartItemGUID"]=qitem.QuoteItemGuid
                    yspec_query = SqlHelper.GetList("SELECT Yspecial_Quote FROM QT__Yspecial_Selection  WHERE CartItemGUID='{}'".format(qitem.QuoteItemGuid))
                    eto_query = SqlHelper.GetList("SELECT ETO_Ref_No FROM QT__PMC_ETO_Selection WHERE CartItemGUID = '{}'".format(qitem.QuoteItemGuid))
                    lv_yspec_list=''
                    lv_eto_list=''
                    if yspec_query is not None: 
                        for i in yspec_query:
                            lv_yspec_list += i.Yspecial_Quote+ ','
                    if eto_query is not None:
                        for i in eto_query:
                            lv_eto_list += i.ETO_Ref_No+ ','
                    HWProducts_table_row["Specials_Quote_Number_Y_specials_quote_or_ETO_Control_number_"]=lv_yspec_list+lv_eto_list
                    full_plant_value = qitem.QI_Plant.Value
                    plant_code,plant_name = split_after_comma(full_plant_value)
                    HWProducts_table_row["Supplying_Plant"] = plant_name
                    Trace.Write('SR yspec:'+ lv_yspec_list+lv_eto_list)
                    '''if fp_plant is not None:
                        if plant_country.get(fp_plant.Plant):
                            fp = plant_country[fp_plant.Plant]
                            HWProducts_table_row["Supplying_Plant"] = fp
                        else:
                            HWProducts_table_row["Supplying_Plant"] = ""'''
                    populateQuoteTableRow(HWProducts_table,HWProducts_table_row)
        HWProducts_table.Save()
def populatetpproduct():
    tp_table=Quote.QuoteTables["PMC_Third_Party_Buyouts"]
    for qitem in Quote.Items:
        phplp_query = SqlHelper.GetFirst("SELECT * FROM QT__PMC_Third_Party_Buyouts  WHERE CartItemGUID='{}'".format(qitem.QuoteItemGuid))
        if phplp_query is not None:
            # Update records
            for k in tp_table.Rows:
                if k["CartItemGUID"] == qitem.QuoteItemGuid:
                    k["Purchase_Price_Unit"]=qitem.Cost
                    k["Unit_Sell_Price"]=qitem.NetPrice
                    k["Quantity"]=qitem.Quantity
                    #tp_table_row['Extended_3_rd_party_Cost_Price'] = float(qitem.Quantity) * float(tp_table_row['Third_party_Cost_Price'])
                    k['Extended_Purchase_Price'] = qitem.Quantity * k['Purchase_Price_Unit']
                    k['Extended_Sell_Price'] = qitem.Quantity * k['Unit_Sell_Price']
            Trace.Write('Update record')
        else:
            #New Record- Insert
            tp_table_row ={}
            if qitem.PartNumber in write_ins:
                tp_table_row["ItemNumber"]=qitem.RolledUpQuoteItem
                tp_table_row["Third_party_write_in_description"]=qitem.PartNumber
                tp_table_row["Third_party_extended_description"]=qitem.Description
                tp_table_row["Purchase_Price_Unit"]=qitem.Cost
                tp_table_row["Unit_Sell_Price"]=qitem.NetPrice
                tp_table_row["Quantity"]=qitem.Quantity
                #tp_table_row["Extended_3_rd_party_Cost_Price"] = qitem.Quantity * tp_table_row['Third_party_Cost_Price']
                tp_table_row['Extended_Purchase_Price'] = qitem.Quantity * tp_table_row['Purchase_Price_Unit']
                tp_table_row['Extended_Sell_Price'] = qitem.Quantity * tp_table_row['Unit_Sell_Price']
                tp_table_row["CartItemGUID"] = qitem.QuoteItemGuid
                tp_table_row["PartNumber"] = qitem.PartNumber
                populateQuoteTableRow(tp_table,tp_table_row)
        tp_table.Save()
#ScriptExecutor.ExecuteGlobal('GS_PMC_Update_Cost') #Added to get cost from SAP 
if Quote.GetCustomField('Booking LOB') is not None and Quote.GetCustomField('Booking LOB').Content == "PMC":
    write_ins_query = SqlHelper.GetList("SELECT Product FROM WriteInProducts")
    write_ins = []
    if write_ins_query is not None:
        for prod in write_ins_query:
            write_ins.append(prod.Product)

    HWProducts_table = Quote.QuoteTables["PMC_Honeywell_Honeywell_Private_Label_Products"]

    populate_PHPLPtable()

    populatetpproduct()