import GS_HCI_PHD_Module

salesOrg = Quote.GetCustomField("Sales Area").Content
currency=Quote.GetCustomField("Currency").Content if Quote.GetCustomField("Currency").Content else 'USD'
alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
def getExecutionCountry():
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    if query is not None:
        return query.Execution_County

laborquery=SqlHelper.GetList("select Labor,Service_Material from CT_HCI_PHD_LABORMATERIAL")
laborDetails={}
for lab in laborquery:
	laborDetails[lab.Labor]=lab.Service_Material
    
finalHrs=0
prd=Product.Name
contLst=['HCI_PHD_EngineeringLabour','HCI_PHD_AdditionalDeliverables']
for cont in contLst:
    contRows=Product.GetContainerByName(cont).Rows
    for row in contRows:
        if cont=='HCI_PHD_EngineeringLabour' and row['Header']=='Header':
            finalHrs+=float(row['Final Hrs'])
        elif cont=='HCI_PHD_AdditionalDeliverables' and row['Hidden_lable']!='Total':
            finalHrs+=float(row['Final Hrs'])
        if prd=='Uniformance Insight Labor' and cont=='HCI_PHD_EngineeringLabour' and row['Deliverable']!='Total':
            finalHrs+=float(row['Final Hrs'])
Trace.Write(str(finalHrs))
contLst=['HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2']
parDictStr=Product.Attributes.GetByName('HCI_PHD_ParChildAttr').GetValue()
parDict=JsonHelper.Deserialize(parDictStr)
pmLaborDict=parDict['pmLaborDict']
productPrice={}
salesCountry=getExecutionCountry()
for cont in contLst:
    contRows=Product.GetContainerByName(cont).Rows
    for row in contRows:
        if row['PM_Percentage']:
            row['Calculated Hrs']=str(round(finalHrs * (float(pmLaborDict[row['PM_Percentage']]['Percentage'])/100)))
            row['Final Hrs']= str( round(finalHrs * (float(pmLaborDict[row['PM_Percentage']]['Percentage'])/100))* float(row['Productivity']))
            labor=row['Eng']
            serviceMaterial=str(laborDetails[labor])
            if serviceMaterial not in productPrice.keys():
                Addproduct =ProductHelper.CreateProduct(laborDetails[labor])
                productPrice[serviceMaterial]=float(Addproduct.TotalPrice)
            listPrice=productPrice[serviceMaterial]
            row['Eng Unit List Price']=str(GS_HCI_PHD_Module.getCalculateListPrice(salesOrg,float(listPrice),row['Execution Year']))
            row['Eng Total List Price']=str(float(row['Eng Unit List Price'])*float(row['Final Hrs']))
            if 'GES' not in labor:
                cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],laborDetails[labor],row['Execution Year'],currency)
                if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost)==0.00:
                    row["Execution Country"] = alternate_execution_country
                    cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],laborDetails[labor],row['Execution Year'],currency)
                if salesCountry!=row['Execution Country']:
                    cost=cost*1.1 if cost else 0
                w2wCost=cost
                if salesCountry!=row['Execution Country']:
                    w2wCost=w2wCost/1.1 if w2wCost else 0
                row['Eng Unit Regional Cost']=str(cost)
                row['Eng Total Regional Cost']=str(float(cost)*float(row['Final Hrs']))
                row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
            else:
                partNumber=laborDetails[labor]
                EC_GES=row['Execution Country']
                if '_CN' in partNumber or '_UZ' in partNumber:
                    EC_GES=''
                cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
                if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost)==0.00:
                    row["Execution Country"] = alternate_execution_country
                    cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
                EACCost=GS_HCI_PHD_Module.getEACCost(partNumber,currency)
                reginoalCost=cost+EACCost
                w2wFactor=GS_HCI_PHD_Module.getW2WFactor(partNumber)
                w2wCost=reginoalCost/(1+w2wFactor)
                row['Eng Unit Regional Cost']=str(reginoalCost)
                row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
                row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
contLst=['HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2']
for cont in contLst:
    finalHrs=0
    calcHrs=0
    delHeaders=[]
    contRows=Product.GetContainerByName(cont).Rows
    for row in contRows:
        if row['Deliverable']!='Total':
            finalHrs+=float(row['Final Hrs'])
            calcHrs+=float(row['Calculated Hrs'])
        else:
            row['Final Hrs']=str(finalHrs)
            row['Calculated Hrs']=str(calcHrs)
            if calcHrs==0:
                delHeaders.append(row.RowIndex)
    delHeaders.reverse()
    for header in delHeaders:
        Product.GetContainerByName(cont).DeleteRow(header)