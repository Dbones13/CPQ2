quoteCurrency = Quote.SelectedMarket.CurrencyCode
EXCHANGE_RATE = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content if Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content else 1 #SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
def currency(c):
	return float(c)*float(EXCHANGE_RATE)
    
Model_Scope = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")
BGP_Models_Hid_Cont = Product.GetContainerByName('SC_BGP_Models_Cont_Hidden')
SC_Product_Type=Product.Attr('SC_Product_Type').GetValue()
BGP_Models_Hid_Cont.Clear()
SP=[]
summary=Product.GetContainerByName('SC_BGP_Models_Cont')
summary.Clear()
# Fetching all values
for row in Model_Scope.Rows:
    sp_name=row['Service_Product']
    SP.append(sp_name)
'''sp1=set(SP)

prodTable = SqlHelper.GetList("select distinct ServiceProduct, ProductCode from CT_SC_ENTITLEMENTS_DATA where Product_Type = 'BGP' and ServiceProduct in {}".format(str(tuple(sp1)).replace(',)',')')))
prodDist = {}
for row in prodTable:
    prodDist[row.ServiceProduct] = row.ProductCode'''
sp1=list(set(SP))
prodDist = {}
if sp1:
    prodTable = SqlHelper.GetList("select distinct ServiceProduct, ProductCode from CT_SC_ENTITLEMENTS_DATA where Product_Type = 'BGP' and ServiceProduct in {}".format(str(tuple(sp1)).replace(',)',')')))
    for row in prodTable:
        prodDist[row.ServiceProduct] = row.ProductCode

if SC_Product_Type=='New':
# calculation part
    for i in sp1:
        final_sum_lp=0
        final_sum_cp=0
        for row in Model_Scope.Rows:
            row['Hidden_Quantity'] = row['Quantity']
            if i==row['Service_Product']:
                qty=int(row['Quantity'])
                if row['Unit_List_Price']=="":
                    a=0
                else:
                    a=float(row['Unit_List_Price'])
                if row['Unit_Cost_Price']=="":
                    b=0
                else:
                    b=float(row['Unit_Cost_Price'])
                lp=a
                cp=b
                s=qty*lp
                c=qty*cp
                final_sum_lp+=s
                final_sum_cp+=c

        row1=summary.AddNewRow(True)
        row1['Service_Product']=i
        row1['ProductCode'] = prodDist[i]
        row1['Quantity'] = str(qty)
        L_Price = round(final_sum_lp,2)
        row1['List_Price']=str(L_Price)

        C_Price = round(final_sum_cp,2)
        row1['Cost_Price']=str(C_Price)
        Hidden_row = BGP_Models_Hid_Cont.AddNewRow(True)
        Hidden_row['Service_Product'] = row1['Service_Product']
        Hidden_row['Quantity'] = row1['Quantity']
        Hidden_row['List_Price'] = row1['List_Price']
        Hidden_row['Cost_Price'] = row1['Cost_Price']
        Hidden_row['ProductCode'] = row1['ProductCode']
else:
    for row in Model_Scope.Rows:
        row1=summary.AddNewRow(True)
        Hidden_row = BGP_Models_Hid_Cont.AddNewRow(True)
        #Hidden_row['Cost_Price']='0.00'
        row1['Service_Product']=Hidden_row['Service_Product']=row['Service_Product']
        Hidden_row['ProductCode'] = row['ProductCode']
        row1['Renewal_Quantity']=Hidden_row['Renewal_Quantity']=row['Renewal_Quantity']
        row1['PY_Quantity']=Hidden_row['PY_Quantity']=row['PY_Quantity']
        if row['Current_Year_List_Price'] != "":
        	row1['Honeywell_List_Price']=Hidden_row['Honeywell_List_Price'] = row['Current_Year_List_Price']
        row1['Previous_Year_List_Price']=Hidden_row['Previous_Year_List_Price']=Hidden_row['PY_ListPrice']=row['Previous_Year_List_Price'] if row['Previous_Year_List_Price']!='' else '0.00'
        #row1['Previous_Year_List_Price']=Hidden_row['Previous_Year_List_Price']=row['Previous_Year_List_Price']
        row1['Model_Number']=Hidden_row['Model_Number']=row['Model_Number']
        row1['Description']=Hidden_row['Description']=row['Description']
        row1['Asset_No']=Hidden_row['Asset_No']=row['Asset No']
        row1['Previous_Year_Cost_Price']=Hidden_row['Previous_Year_Cost_Price']=row['Previous_Year_Cost_Price']
        row1['Current_Year_Cost_Price']=Hidden_row['Cost_Price']=Hidden_row['Current_Year_Cost_Price']=row['Current_Year_Cost_Price']
        row1['Scope Reduction Price']=Hidden_row['Scope Reduction Price']= str(float(row['Scope Reduction Price'])) if row['Scope Reduction Price']!='' else '0.00'
        row1['Scope Addition Price']=Hidden_row['Scope Addition Price']=row['Scope Addition Price'] if row['Scope Addition Price']!='' else '0.00'
        Hidden_row['SR_Price']= str(float(row['Scope Reduction Price'])) if row['Scope Reduction Price']!='' else '0.00'
        Hidden_row['SA_Price']=row['Scope Addition Price'] if row['Scope Addition Price']!='' else '0.00'
        # SC_Pricing_Escalation Changes
        if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
            Hidden_row['List_Price'] = str(float(Hidden_row['SR_Price']) + float(Hidden_row['SA_Price']) + float(Hidden_row['Previous_Year_List_Price']))
            Hidden_row['Escalation_Price'] = str(float(Hidden_row['Previous_Year_List_Price']) - float(Hidden_row['SR_Price']))
        else:
            Hidden_row['List_Price'] = str(row['Current_Year_List_Price'])
            Hidden_row['Escalation_Price'] = '0'
        Hidden_row.Calculate()
        row1['Comments']=Hidden_row['Comments']='Scope Addition' if float(row1['Scope Reduction Price'])+float(row1['Scope Addition Price'])>0  else  'Scope Reduction' if  float(row1['Scope Reduction Price'])+float(row1['Scope Addition Price']) <0 else 'No Scope Change'
        row1['Py_SellPrice']=Hidden_row['Py_SellPrice']=row['Py_SellPrice']
        Hidden_row['LY_Discount']=row['LY_Discount']
           
    
summary.Calculate()
BGP_Models_Hid_Cont.Calculate()