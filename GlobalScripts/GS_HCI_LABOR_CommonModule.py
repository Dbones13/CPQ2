class HCIModule:
    def __init__(self, Quote, Product):
        self.quote = Quote
        self.product = Product
        self.salesorg = Quote.GetCustomField("Sales Area").Content
        self.Quotecurrency = Quote.GetCustomField("Currency").Content
        self.CurrencyDict = {'GES China':'CNY','GES India':'INR','GES Kazakhstan':'KZT'}
        query = SqlHelper.GetList("select Exchange_Rate,From_Currency,To_Currency from Currency_ExchangeRate_Mapping (NOLOCK)")
        self.ExchangeRates = {(excRate.From_Currency,excRate.To_Currency): excRate.Exchange_Rate for excRate in query}

        getEACValue = SqlHelper.GetList("SELECT EAC_Value,GES_Service_Material,Currency FROM Labor_GES_EAC_Value(NOLOCK)")
        self.EACdict = {item.GES_Service_Material: {'EACValue':item.EAC_Value,'EACCurr':item.Currency} for item in getEACValue}

        getW2WFactor = SqlHelper.GetList("SELECT WTWMarkupFactorEstimated,GES_Service_Material FROM Labor_GES_WTW_Markup_Factor(NOLOCK) ")
        self.W2WDict = {fctr.GES_Service_Material:fctr.WTWMarkupFactorEstimated for fctr in getW2WFactor}

        inflation = SqlHelper.GetFirst("SELECT * FROM YOY_Inflation_Rate(NOLOCK) WHERE LOB = 'HCI' AND SalesOrg = '"+self.salesorg+"'")
        self.InflationRate=  inflation.Inflation_Rate if inflation else 0.0
        self.InflationRate_Year2 = inflation.Inflation_Rate_Year2 if inflation else 0.0
        self.InflationRate_Year3 = inflation.Inflation_Rate_Year3 if inflation else 0.0

        salesorg_details = SqlHelper.GetFirst("SELECT Execution_County, Currency FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_Country_Sales_Org = '{}' AND  Currency = '{}'".format(self.salesorg, self.Quotecurrency))
        self.salesorg_region = salesorg_details.Execution_County if salesorg_details else ''
        self.salesorg_curr = salesorg_details.Currency if salesorg_details else ''

        cost = SqlHelper.GetList("SELECT Part_Number,Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{}' ".format(self.salesorg))
        self.LaborcostDict = {i.Part_Number:[self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year1),self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year2), self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year3), self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year4)] for i in cost}

        getPartDesc = SqlHelper.GetList("SELECT Description,Labor_Material FROM CT_PartDescriptions(NOLOCK)")
        self.materialDesc = {desc.Labor_Material: desc.Description for desc in getPartDesc}
        self.materials = {desc.Description: desc.Labor_Material for desc in getPartDesc}

        self.EC = Product.Attr('AR_HCI_Executioncountry').GetValue()

    def LaborcostDictValue(self, exec_salesorg):
        salesOrg_value = exec_salesorg
        cost = SqlHelper.GetList("SELECT Part_Number,Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{}' ".format(salesOrg_value))
        self.LaborcostDict = {i.Part_Number:[self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year1),self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year2), self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year3), self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year4)] for i in cost}
        return self.LaborcostDict

    def LaborCostDict(self,execur):
        cost = SqlHelper.GetList("SELECT Part_Number,Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{}' ".format(execur))
        Trace.Write("--- > SELECT Part_Number,Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{}' ".format(execur))
        LaborcostDict = {i.Part_Number:[i.Cost_CurrentMonth_Year1,i.Cost_CurrentMonth_Year2,i.Cost_CurrentMonth_Year3,i.Cost_CurrentMonth_Year4,i.Cost_Currency_Code] for i in cost}
        return LaborcostDict

    def adjust_cost(self,i):
        country =i['ExecutionCountry']
        Trace.Write("SELECT Execution_County, Currency,Execution_Country_Sales_Org FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_County = '{}' ".format(country))
        salesorg_details = SqlHelper.GetFirst("SELECT Execution_County, Currency,Execution_Country_Sales_Org FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_County = '{}' ".format(country))
        
        sales_org = salesorg_details.Execution_Country_Sales_Org if salesorg_details else ''
        cost = SqlHelper.GetList("SELECT Part_Number,Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{}' ".format(sales_org))
        Trace.Write('cost--1233 ---'+str(sales_org))
        if len(sales_org) >0:
            self.LaborcostDict = {i.Part_Number:[self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year1),self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year2), self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year3), self.QuoteCurrencyConversion(i.Cost_Currency_Code,self.salesorg_curr,i.Cost_CurrentMonth_Year4)] for i in cost}
            Trace.Write('cost--123>'+str(self.LaborcostDict))
        
    def getSalesOrg(self,country):
        query = SqlHelper.GetFirst("select Execution_Country_Sales_Org,Currency from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
        if query is not None:
            return query.Execution_Country_Sales_Org, query.Currency
        else:
            return self.salesorg,self.salesorg_curr
            
    def cost_increment(self,cost):
        Trace.Write('cost inc---'+str(cost))
        denom = float(cost)/10 # increase cost by 10%
        return str(float(cost)+float(denom))
    
    def addupdateTotalRow(self,cont):
        delrowList =[rows.RowIndex for rows in cont.Rows if rows['Deliverable']=='Total']
        delrowList.reverse()
        for i in delrowList:
            cont.DeleteRow(i)
        calcHrs, FinalHrs, TotalW2W, TotalReg, TotalList, TotalUnit, totalPrd = 0.0 , 0.0, 0.0 , 0.0, 0.0 , 0.0, 0.0
        for i in cont.Rows:
            calcHrs +=float((i['CalculatedHours']) or 0.0)
            FinalHrs += float((i.Product.Attr('ItemQuantity').GetValue()) or 0.0)
            TotalList += float((i['TotalListPrice']) or 0.0)
            TotalReg += float((i['TransferCost']) or 0.0)
            TotalUnit += float((i['UnitListPrice']) or 0.0)
            #totalPrd += float(i['Productivity'] or 0.0)
            TotalW2W += float(i['W2WCost'] or 0.0)
        Trace.Write('fincal hrs--'+str(FinalHrs))
        totalRow = cont.AddNewRow(False)
        totalRow['ProductLine'] = totalRow['Engr'] = 'Total'
        totalRow['Deliverable'] ='Total'
        totalRow.Product.Attr('AR_HCI_EXECUTION_DELIVERABLES').SelectDisplayValue('Total')
        totalRow['CalculatedHours'] = str(calcHrs)
        totalRow.Product.Attr('ItemQuantity').AssignValue(str(FinalHrs))
        totalRow['FinalHours'] = str(FinalHrs)
        totalRow['TotalListPrice'] = str(TotalList)
        totalRow['TransferCost'] = str(TotalReg)
        totalRow['UnitListPrice'] = str(TotalUnit)
        totalRow['W2WCost'] = str(TotalW2W)
        totalRow['Productivity'] = '' #str(totalPrd)

    
    def getFloat(self,Var):
        if Var:
            return float(Var)
        return 0.00
    
    def QuoteCurrencyConversion(self,fromCurr,ToCurr,costprice,CurrofCost = None):
        costInQuoteCurrency = costprice
        if CurrofCost is None:
            if self.Quotecurrency== 'USD':
                Exc = self.ExchangeRates.get((fromCurr, 'USD'))
                if Exc is not None:
                    costInQuoteCurrency = self.getFloat(costprice) * self.getFloat(Exc)
            else:
                Exc = self.ExchangeRates.get((fromCurr, 'USD'))
                if Exc:
                    costInUSD = self.getFloat(costprice) * self.getFloat(Exc)
                    Exc = self.ExchangeRates.get(('USD', ToCurr))
                    if Exc is not None:
                        costInQuoteCurrency = self.getFloat(costInUSD) * self.getFloat(Exc)
        else:
            if CurrofCost == 'USD':
                Exc = self.ExchangeRates.get(('USD', ToCurr))
                if Exc is not None:
                    costInQuoteCurrency = self.getFloat(costprice) * self.getFloat(Exc)
            else:
                Exc = self.ExchangeRates.get((CurrofCost, 'USD'))
                if Exc:
                    costInUSD = self.getFloat(costprice) * self.getFloat(Exc)
                    Exc = self.ExchangeRates.get(('USD', ToCurr))
                    if Exc is not None:
                        costInQuoteCurrency = self.getFloat(costInUSD) * self.getFloat(Exc)
        
        Trace.Write('-8 '+str(costInQuoteCurrency))
        return str(costInQuoteCurrency)

    
    def getlaborPrices(self,getDict,totalprice,execution_year,current_year,exec_country_curr,CurrofCost = None):
        transfercost = 0.00
        Trace.Write(str(execution_year)+'--yeras-'+str(current_year)+'--getDict--'+str(getDict))
        if str(execution_year) == '':
            execution_year = current_year
        if int(execution_year) == current_year:
            Trace.Write('inside year 1--')
            transfercost = str(self.getFloat(str(getDict[0])))
        elif int(execution_year) == current_year + 1:
            transfercost = str(self.getFloat(str(getDict[1])))
            totalprice = float(totalprice)*(1+float(self.InflationRate))
        elif int(execution_year) == current_year + 2:
            transfercost = str(self.getFloat(str(getDict[2])))
            totalprice = float(totalprice)*(1+float(self.InflationRate))*(1+float(self.InflationRate_Year2))
        elif int(execution_year) == current_year + 3:
            transfercost = str(self.getFloat(str(getDict[3])))
            totalprice = float(totalprice)*(1+float(self.InflationRate))*(1+float(self.InflationRate_Year2))*(1+float(self.InflationRate_Year3))
        Trace.Write('--yeras vallues-'+str([transfercost, totalprice]))
        transfercost = self.QuoteCurrencyConversion(exec_country_curr,self.Quotecurrency,transfercost,CurrofCost)
        return transfercost, totalprice