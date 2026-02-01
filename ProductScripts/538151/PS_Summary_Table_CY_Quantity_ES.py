SC_ScopeRemoval = Product.Attr('SC_ScopeRemoval').GetValue()
row_cont = Product.GetContainerByName('Asset_details_ServiceProd').Rows.Count
ES_Asset_Summary = Product.GetContainerByName('ES_Asset_Summary')
Trace.Write("SC_ScopeRemoval "+str(SC_ScopeRemoval))
if SC_ScopeRemoval in [None, '']:
    if ES_Asset_Summary.Rows.Count:
        for row in ES_Asset_Summary.Rows:
            Trace.Write("row_cont "+str(row_cont))
            row["No_MSID_CY"] = str(row_cont) if row_cont!='' else 0
if ES_Asset_Summary.Rows.Count:
    for row in ES_Asset_Summary.Rows:
        if row["No_MSID_PY"] > row["No_MSID_CY"]:
            row["Escalation_Price"] = str(float(row["PY_List_Price"]) - float(row["Scope_Reduction"]))
        else:
            row["Escalation_Price"] = str(float(row["PY_List_Price"]) - float(row["Scope_Reduction"]))
        row["PY_ListPrice"] = row["PY_List_Price"]
        row["SR_Price"] = row["Scope_Reduction"]
        row["SA_Price"] = row["Scope_Addition"]
        row['Comments'] = 'Scope Addition' if float(row['Scope_Addition']) > 0 else ('Scope Reduction' if float(row['Scope_Reduction']) < 0 else 'No Scope Change')
        row['Hidden_List_Price'] = row['CY_List_Price']

#PY sell price code
Comp_summ = Product.GetContainerByName("ESComparisonSummary")
Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
Product_type = Product.Attr('SC_Product_Type').GetValue()
Quote_Number = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
ES_Asset_Summary = Product.GetContainerByName('ES_Asset_Summary')
#if Product_type == 'Renewal' and Quote_Number in [None,''] and Contract_Number not in [None, '']:
if Product_type == 'Renewal':
    discount_percent = 0
    if Comp_summ.Rows.Count:
        for row in Comp_summ.Rows:
            discount_percent = ((float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC']) if float(row['PY_List_Price_SFDC']) != '' else 0)
    if ES_Asset_Summary.Rows.Count:
        for hrow in ES_Asset_Summary.Rows:
                discount = discount_percent
                hrow['PY_SellPrice'] = str(float(hrow['PY_List_Price']) - (float(hrow['PY_List_Price']) * discount))