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

Product.Attr('apply_changes').AssignValue('True')
prd=Product.Name
productivity=Product.Attributes.GetByName('AR_HCI_PRODUCTIVITY').GetValue()
year=Product.Attributes.GetByName('HCI_PHD_Execution_Year').GetValue()
country=Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').GetValue()
gesLoc=Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue()
engRole=Product.Attributes.GetByName('HCI_PHD_FO_GES_Eng_Roles').GetValue()
gesLocdict={'GES China':'CN','GES India':'IN','GES Uzbekistan':'UZ'}
gesCode=""
if gesLoc:
    gesCode=gesLocdict[gesLoc]


salesCountry=getExecutionCountry()
contLst=['HCI_PHD_EngineeringLabour','HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables']
headerTotal={}
calcHrsTotal={}
productPrice={}
costTotalDict={}
ListPriceTotalDict={}
WTWCostTotalDict={}
for cont in contLst:
    contRows=Product.GetContainerByName(cont).Rows
    for row in contRows:
        if not row['Productivity'] and row['Deliverable']!='Total':
            row['Productivity']="1"
        if row['Final Hrs'] and row['Calculated Hrs'] and cont!='HCI_PHD_AdditionalDeliverables' and row['Deliverable']!='Total':
            row['Productivity']=str((float(row['Final Hrs'])/float(row['Calculated Hrs']))) if float(row['Calculated Hrs'])!=0 else '1'
        if row.IsSelected and cont!='HCI_PHD_AdditionalDeliverables':
            if productivity and row['Calculated Hrs'] and float(row['Calculated Hrs'])!=0:
                row['Productivity']=str(productivity)
            if year:
                row['Execution Year']=str(year)
            if country:
                row['Execution Country']=country
            Trace.Write(str(['-->check',cont,row['Calculated Hrs'],row['Productivity']]))
            row['Final Hrs']=str(round(float(row['Calculated Hrs'])*float(row['Productivity'])))
            if gesLoc and 'GES' in row['Eng']:
                gesEng=row['Eng'].split('-')
                row['Eng']=gesEng[0]+'-'+gesCode
            if cont=='HCI_PHD_EngineeringLabour' and engRole:
                row['Eng']=engRole
        elif row.IsSelected and cont=='HCI_PHD_AdditionalDeliverables':
            if year:
                row['Execution Year']=str(year)
                row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').AssignValue(year)
                row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').SelectValue(year)
                row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').SelectDisplayValue(year)
            if country:
                row['Execution Country']=country
                row.Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').AssignValue(country)
                row.Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').SelectDisplayValue(country)
        if row['Eng'] and row['Eng']!='None':
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
                if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
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
                if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
                    row["Execution Country"] = alternate_execution_country
                    cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
                '''if salesCountry!=row['Execution Country']:
                    cost=cost*1.1 if cost else 0'''
                EACCost=GS_HCI_PHD_Module.getEACCost(partNumber,currency)
                reginoalCost=cost+EACCost
                w2wFactor=GS_HCI_PHD_Module.getW2WFactor(partNumber)
                w2wCost=reginoalCost/(1+w2wFactor)
                row['Eng Unit Regional Cost']=str(reginoalCost)
                row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
                row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
        if prd=='PHD Labor' and cont=='HCI_PHD_EngineeringLabour' and row['Header']!='Header':
            if row['Header'] not in headerTotal.keys():
                headerTotal[row['Header']]=float(row['Final Hrs'])
            else:
                headerTotal[row['Header']]+=float(row['Final Hrs'])
            if row['Header'] not in calcHrsTotal.keys():
                calcHrsTotal[row['Header']]=float(row['Calculated Hrs'])
            else:
                calcHrsTotal[row['Header']]+=float(row['Calculated Hrs'])
            if row['Header'] not in costTotalDict.keys():
                costTotalDict[row['Header']]=float(row['Eng Total Regional Cost'])
            else:
                costTotalDict[row['Header']]+=float(row['Eng Total Regional Cost'])
            if row['Header'] not in ListPriceTotalDict.keys():
                ListPriceTotalDict[row['Header']]=float(row['Eng Total List Price'])
            else:
                ListPriceTotalDict[row['Header']]+=float(row['Eng Total List Price'])
            if row['Header'] not in WTWCostTotalDict.keys():
                WTWCostTotalDict[row['Header']]=float(row['Eng Total WTW Cost'])
            else:
                WTWCostTotalDict[row['Header']]+=float(row['Eng Total WTW Cost'])
if prd=='PHD Labor':
    cont=Product.GetContainerByName('HCI_PHD_EngineeringLabour')
    contRows=cont.Rows
    finalHrs=0
    calcHrs=0
    totalCost=0
    totalListPrice=0
    totalWTWCost=0
    delHeaders=[]
    for row in contRows:
        if row['Header']=='Header' and row['Deliverable'] not in headerTotal.keys() :
            delHeaders.append(row.RowIndex)
        if row['Header']=='Header' and row['Deliverable'] in headerTotal.keys() :
            row['Final Hrs']=str(headerTotal[row['Deliverable']])
            finalHrs+=float(row['Final Hrs'])
            if row['Final Hrs'] and row['Calculated Hrs']:
                row['Productivity']=str((float(row['Final Hrs'])/float(row['Calculated Hrs']))) if float(row['Calculated Hrs'])!=0 else '1'
        if row['Header']=='Header' and row['Deliverable'] in calcHrsTotal.keys() :
            row['Calculated Hrs']=str(calcHrsTotal[row['Deliverable']])
            calcHrs+=float(row['Calculated Hrs'])
        if row['Header']=='Header' and row['Deliverable'] in costTotalDict.keys() :
            row['Eng Total Regional Cost']=str(costTotalDict[row['Deliverable']])
            totalCost+=float(row['Eng Total Regional Cost'])
        if row['Header']=='Header' and row['Deliverable'] in ListPriceTotalDict.keys() :
            row['Eng Total List Price']=str(ListPriceTotalDict[row['Deliverable']])
            totalListPrice+=float(row['Eng Total List Price'])
        if row['Header']=='Header' and row['Deliverable'] in WTWCostTotalDict.keys() :
            row['Eng Total WTW Cost']=str(WTWCostTotalDict[row['Deliverable']])
            totalWTWCost+=float(row['Eng Total WTW Cost'])
        '''if row['Deliverable']=='Travel Time':
            finalHrs+=float(row['Final Hrs'])
            calcHrs+=float(row['Calculated Hrs'])'''
        if row['Deliverable']=='Total':
            row['Final Hrs']=str(finalHrs)
            row['Calculated Hrs']=str(calcHrs)
            row['Eng Total Regional Cost']=str(totalCost)
            row['Eng Total List Price']=str(totalListPrice)
            row['Eng Total WTW Cost']=str(totalWTWCost)
            if calcHrs==0:
                delHeaders.append(row.RowIndex)
    delHeaders.reverse()
    for header in delHeaders:
        cont.DeleteRow(header)
        
if prd=='Uniformance Insight Labor':
    finalHrs=0
    calcHrs=0
    totalCost=0
    totalListPrice=0
    totalWTWCost=0
    delHeaders=[]
    cont=Product.GetContainerByName('HCI_PHD_EngineeringLabour')
    contRows=cont.Rows
    for row in contRows:
        if row['Deliverable']!='Total':
            finalHrs+=float(row['Final Hrs'])
            calcHrs+=float(row['Calculated Hrs'])
            totalCost+=float(row['Eng Total Regional Cost'])
            totalListPrice+=float(row['Eng Total List Price'])
            totalWTWCost+=float(row['Eng Total WTW Cost'])
            
        else:
            row['Final Hrs']=str(finalHrs)
            row['Calculated Hrs']=str(calcHrs)
            row['Eng Total Regional Cost']=str(totalCost)
            row['Eng Total List Price']=str(totalListPrice)
            row['Eng Total WTW Cost']=str(totalWTWCost)
            if calcHrs==0:
                delHeaders.append(row.RowIndex)
    delHeaders.reverse()
    for header in delHeaders:
        cont.DeleteRow(header)
contLst=['HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2']
for cont in contLst:
    finalHrs=0
    calcHrs=0
    totalCost=0
    totalListPrice=0
    totalWTWCost=0
    delHeaders=[]
    contRows=Product.GetContainerByName(cont).Rows
    for row in contRows:
        if row['Deliverable']!='Total':
            finalHrs+=float(row['Final Hrs'])
            calcHrs+=float(row['Calculated Hrs'])
            totalCost+=float(row['Eng Total Regional Cost'])
            totalListPrice+=float(row['Eng Total List Price'])
            totalWTWCost+=float(row['Eng Total WTW Cost'])
        else:
            row['Final Hrs']=str(finalHrs)
            row['Calculated Hrs']=str(calcHrs)
            row['Eng Total Regional Cost']=str(totalCost)
            row['Eng Total List Price']=str(totalListPrice)
            row['Eng Total WTW Cost']=str(totalWTWCost)
            if calcHrs==0:
                delHeaders.append(row.RowIndex)
    delHeaders.reverse()
    for header in delHeaders:
        Product.GetContainerByName(cont).DeleteRow(header)

finalHrs=0
totalCost=0
totalListPrice=0
totalWTWCost=0
contRows=Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').Rows
for row in contRows:
    if row['Hidden_lable']!='Total':
        if row.IsSelected:
            if country:
                row['Execution Country'] = country
                row.Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').AssignValue(country)
                row.Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').SelectDisplayValue(country)
            if year:
                row['Execution Year'] = year
                row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').AssignValue(year)
                row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').SelectValue(year)
                row.Product.Attributes.GetByName('HCI_PHD_Execution_Year').SelectDisplayValue(year)
            if engRole:
                row['Eng'] = engRole
                row.Product.Attributes.GetByName('HCI_PHD_PM_Labour2').AssignValue(engRole)
                row.Product.Attributes.GetByName('HCI_PHD_PM_Labour2').SelectValue(engRole)
                row.Product.Attributes.GetByName('HCI_PHD_PM_Labour2').SelectDisplayValue(engRole)
        finalHrs+=float(row['Final Hrs']) if row['Final Hrs']!='' else 0
        totalCost+=float(row['Eng Total Regional Cost']) if row['Eng Total Regional Cost']!='' else 0
        totalListPrice+=float(row['Eng Total List Price']) if row['Eng Total List Price']!='' else 0
        totalWTWCost+=float(row['Eng Total WTW Cost']) if row['Eng Total WTW Cost']!='' else 0
    else:
        row['Final Hrs']=str(finalHrs)
        row['Eng Total Regional Cost']=str(totalCost)
        row['Eng Total List Price']=str(totalListPrice)
        row['Eng Total WTW Cost']=str(totalWTWCost)
    row.Calculate()

Product.ResetAttr('AR_HCI_PRODUCTIVITY')
Product.ResetAttr('HCI_PHD_Execution_Year')
Product.ResetAttr('AR_HCI_FO_ENG_Executioncountry')
Product.ResetAttr('HCI_PHD_GES_Location')
Product.ResetAttr('HCI_PHD_FO_GES_Eng_Roles')