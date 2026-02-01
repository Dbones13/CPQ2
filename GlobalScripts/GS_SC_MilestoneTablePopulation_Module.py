def row_count_frequency(Inv_Freq):
    Invoicing_Frequencies = {
        "Adhoc": 1,
        "Yearly": 1,
        "Bi-Monthly": 12/2,
        "Every 4 weeks": 52/4,
        "Every 4 months": 12/4,
        "Monthly": 12,
        "Quarterly": 12/3,
        "Semi-Annual": 12/6,
    }
    row_count = Invoicing_Frequencies.get(Inv_Freq)
    return row_count

def Func_Start_date_End_date(Inv_Freq,StartDate,EndDate):
    Inv_Freq_Months = {
        "Yearly": 12,
        "Quarterly": 3,
        "Monthly": 1,
        "Semi-Annual": 6,
        "Bi-Monthly": 2,
        "Every 4 weeks": 28,
        "Every 4 months": 4,
    }
    Frequency_Count = Inv_Freq_Months.get(Inv_Freq)
    St_DT_lst = []
    Ed_DT_lst = []
    Start_Date = StartDate
    if Inv_Freq == 'Adhoc':
        St_DT_lst.append(StartDate)
        Ed_DT_lst.append(EndDate)
    else:
        while Start_Date <= EndDate:
            St_dt= Start_Date
            if Inv_Freq == 'Every 4 weeks':
                End_date = Start_Date.AddDays(Frequency_Count)
            else:
                End_date = Start_Date.AddMonths(Frequency_Count)
            Ed_dt = End_date.AddDays(-1)
            Start_Date = Ed_dt.AddDays(1) 
            St_DT_lst.append(St_dt)
            Ed_DT_lst.append(Ed_dt)
            #Trace.Write('Frequency:{}, StartDate : {}, EndDate :{}'.format(Inv_Freq,St_dt,End_date))
    return St_DT_lst,Ed_DT_lst

def PopulateTable(table,sell_price_lst,Contract_St_Dt_lst,Contract_Ed_Dt_lst,Years,row_count,Inv_Freq,CurrAnulDeli_St_Dt,CurrAnulDeli_Ed_Dt):
    if len(sell_price_lst) > 0:
        if Inv_Freq == 'Adhoc':
            for r in range(row_count):
                row = table.AddNewRow()
                row['Milestone_Number'] = 'Milestone {}'.format(1)
                row['Value'] = float(sum(sell_price_lst))/row_count
                row['Percentage_Amount'] = int(((float(sum(sell_price_lst))/row_count)/float(sum(sell_price_lst)))*100)
                row['Start_Date'] = Contract_St_Dt_lst[0]
                row['End_Date'] = Contract_Ed_Dt_lst[0]
                row['Yearly_Price'] = float(sum(sell_price_lst))
                if row['Start_Date'] >= CurrAnulDeli_St_Dt and  row['End_Date'] <= CurrAnulDeli_Ed_Dt:
                    row['PSC'] = True
        else:
            m = 0
            for idx,p in enumerate(sell_price_lst):
                Trace.Write('JJ' + str(p))
                for r in range(row_count):
                    Trace.Write('Jagruti' + str(p) + '  ' + str(row_count))
                    if m == len(Contract_St_Dt_lst):
                        break
                    row = table.AddNewRow()
                    row['Milestone_Number'] = 'Milestone {}'.format(m+1)
                    if Inv_Freq == 'Yearly':
                    	row['Value'] = float(p)
                        row['Percentage_Amount'] = float((float(p)/float(p))*100)
                    else:
                        row['Value'] = float(p)/row_count
                    	row['Percentage_Amount'] = float(((float(p)/row_count)/float(p))*100)
                    row['Start_Date'] = Contract_St_Dt_lst[m]
                    row['End_Date'] = Contract_Ed_Dt_lst[m]
                    row['Yearly_Price'] = float(p)
                    row['Years'] = Years[idx]
                    if row['Start_Date'] >= CurrAnulDeli_St_Dt and  row['End_Date'] <= CurrAnulDeli_Ed_Dt:
                        row['PSC'] = True
                    m = m + 1
    return table

def Main_function(Quote,lv_event):
    Contract = ['Contract New','Contract Renewal']
    if Quote.GetCustomField('Quote Type').Content in Contract:
        EGAP_Contract_Start_Date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
        EGAP_Contract_End_Date = Quote.GetCustomField('EGAP_Contract_End_Date').Content
        SC_CF_CURANNDELSTDT = Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content
        SC_CF_CURANNDELENDT = Quote.GetCustomField('SC_CF_CURANNDELENDT').Content

        if SC_CF_CURANNDELSTDT!='' and SC_CF_CURANNDELENDT!='':
            CurrAnulDeli_St_Dt = UserPersonalizationHelper.CovertToDate(SC_CF_CURANNDELSTDT)
            CurrAnulDeli_Ed_Dt = UserPersonalizationHelper.CovertToDate(SC_CF_CURANNDELENDT)

            Contract_St_Dt = UserPersonalizationHelper.CovertToDate(EGAP_Contract_Start_Date) if EGAP_Contract_Start_Date else ''
            Contract_Ed_Dt = UserPersonalizationHelper.CovertToDate(EGAP_Contract_End_Date) if EGAP_Contract_End_Date else ''

            table = Quote.QuoteTables["SC_Milestone_Table"]

            Inv_Freq = Quote.GetCustomField('SC_CF_INV_FREQUENCY').Content

            CurrAnulDeli_St_Dt_lst,CurrAnulDeli_Ed_Dt_lst = Func_Start_date_End_date(Inv_Freq,CurrAnulDeli_St_Dt,CurrAnulDeli_Ed_Dt)

            if Contract_St_Dt and Contract_Ed_Dt:
                Contract_St_Dt_lst,Contract_Ed_Dt_lst = Func_Start_date_End_date(Inv_Freq,Contract_St_Dt,Contract_Ed_Dt)
                if Contract_Ed_Dt_lst[-1] != Contract_Ed_Dt:
                    Contract_Ed_Dt_lst[-1] = Contract_Ed_Dt

            if CurrAnulDeli_Ed_Dt_lst[-1] != CurrAnulDeli_Ed_Dt:
                CurrAnulDeli_Ed_Dt_lst[-1] = CurrAnulDeli_Ed_Dt

            row_count = len(CurrAnulDeli_St_Dt_lst) if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content =='True' else row_count_frequency(Inv_Freq)

            sell_price_lst = []
            Years = []
            for item in Quote.MainItems:
                if 'Year' in item.PartNumber:
                    sell_price_lst.append(round(float(item.ExtendedAmount),2))
                    Years.append(item.PartNumber)
            Trace.Write('Test' + str(sell_price_lst))
            Mismatch_Prices=[]
            if lv_event=='QTab':
                Table_Prices = []
                for row in table.Rows:
                    Table_Prices.append(row['Yearly_Price'])
                Mismatch_Prices = [SP for SP in sell_price_lst if SP not in Table_Prices]
                Header_tot_sell_price = (Quote.GetCustomField('Total Sell Price(CW)').Content)[4:].replace(",", "")

            if Inv_Freq == 'Adhoc':
                table.GetColumnByName('PSC').AccessLevel = table.AccessLevel.Editable
            else:
                table.GetColumnByName('PSC').AccessLevel = table.AccessLevel.ReadOnly

            SC_CF_ContractEndDate = Quote.GetGlobal('SC_CF_ContractEndDate')
            SC_CF_ContractEndDate = DateTime.Parse(SC_CF_ContractEndDate) if (SC_CF_ContractEndDate !='' and SC_CF_ContractEndDate!= None) else None

            if (lv_event=='QTab' and table.Rows.Count == 0 or len(Mismatch_Prices) > 0) or lv_event=='CFINVChange' :
                table.Rows.Clear()
                if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal' and ((SC_CF_ContractEndDate and SC_CF_ContractEndDate == Contract_Ed_Dt) or Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content =='True') :
                    table = PopulateTable(table,sell_price_lst,CurrAnulDeli_St_Dt_lst,CurrAnulDeli_Ed_Dt_lst,Years,row_count,Inv_Freq,CurrAnulDeli_St_Dt,CurrAnulDeli_Ed_Dt)
                else:
                    table = PopulateTable(table,sell_price_lst,Contract_St_Dt_lst,Contract_Ed_Dt_lst,Years,row_count,Inv_Freq,CurrAnulDeli_St_Dt,CurrAnulDeli_Ed_Dt)

            table.Save()

#Main_function(Quote,'CFINVChange')