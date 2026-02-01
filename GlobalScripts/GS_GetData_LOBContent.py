# ---------------------------------------------------------------------------------------------------------
# 					Change History Log
# ---------------------------------------------------------------------------------------------------------
# Description:LOB Content and Populating data into Quote Table - LOB Content (QT_FinancialSummary_LOBContent).
#            Called from Quote Calculation to get "LOB Content" table populated
# ----------------------------------------------------------------------------------------------------------
# Date 			Name					Version   Comment
# 10-04-2023	Sarthak Gupta			31		  Initial Creation
#

def getLOB_Content(Quote):

    plsgquery = SqlHelper.GetList(
        "SELECT Product_Line_Sub_Group,SAP_PL_PLSG, Cost_Category, B.LOB, Sub_LOB FROM {} A JOIN SAP_PLSG_LOB_Mapping B ON A.Product_Line_Sub_Group = B.SAP_PL_PLSG WHERE A.cartid = {} AND A.ownerId ={}".format(
            "QT__Product_Line_Sub_Group_Details", Quote.QuoteId, Quote.UserId
        )
    )
    plsg_dict = {}
    for item in plsgquery:
        plsg_dict[item.SAP_PL_PLSG] = item.LOB
    lob=["PAS","LSS","AS","PMC","CYB","CCC","Other","Total"]
    TotalsellPrice=[0,0,0,0,0,0,0,0]
    # calculating total sell price for for each LOB
    for i in Quote.Items:
        if len(list(i.AsMainItem.Children))==0:
            # iLob=i.QI_PLLOB.Value.strip()
            iLob = i.QI_PLLOB.Value.strip() if Quote.GetCustomField('Quote Type').Content in('Contract New','Contract Renewal') else plsg_dict.get(i.QI_PLSG.Value, '')
            if iLob=="PAS":
                TotalsellPrice[0]+=i.ExtendedAmount
            elif iLob=="LSS":
                TotalsellPrice[1]+=i.ExtendedAmount
            elif iLob=="AS":
                TotalsellPrice[2]+=i.ExtendedAmount
            elif iLob=="PMC":
                TotalsellPrice[3]+=i.ExtendedAmount
            elif iLob=="CYB" or iLob=="Cyber":
                TotalsellPrice[4]+=i.ExtendedAmount
            elif iLob=="CCC":
                TotalsellPrice[5]+=i.ExtendedAmount
            else:
                TotalsellPrice[6]+=i.ExtendedAmount
            TotalsellPrice[7]+=i.ExtendedAmount
    # fetching exchange rate
    EXRate=Quote.GetCustomField("Exchange Rate").Content
    EXRate=1 if EXRate=="" or EXRate == None else float(EXRate)
    # populate data in QT_LOB_CONTENT_financial_summary Table along with conversion of sell price in USD
    QT_LOB_Content=Quote.QuoteTables["QT_FinancialSummary_LOBContent"]
    QT_LOB_Content.Rows.Clear()
    for j in range(0,len(lob)):
        row = QT_LOB_Content.AddNewRow()
        row["LOB"] = "HCI" if lob[j]=="AS" else lob[j]
        row["Sell_Price_QC"]=TotalsellPrice[j]
        # calucuting sell price in USD rounded upto 2 decimal places
        totalSellPrice_USD=round(TotalsellPrice[j]/EXRate,2)
        row["Sell_Price_USD"]=totalSellPrice_USD
    QT_LOB_Content.Save()