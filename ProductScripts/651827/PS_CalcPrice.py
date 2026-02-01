#Log.Write('PS_CalcPrice---session---------exec-'+str(Session["prevent_execution"]))
cont = Product.GetContainerByName('AR_HCI_SUBPRD')
if cont.Rows.Count>1:
    laborquery=SqlHelper.GetList("select Labor,Service_Material from CT_HCI_PHD_LABORMATERIAL")
    laborDetails={}
    for lab in laborquery:
        laborDetails[lab.Labor]=lab.Service_Material

    labourFinalHrsDict={}
    for mainRow in cont.Rows[1].Product.GetContainerByName('HCI_PHD_Selected_Products').Rows:
        parentProduct=mainRow.Product
        labourFinalHrsDict[parentProduct.Name]={}
        containersLst=['HCI_PHD_EngineeringLabour','HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables']
        for conts in containersLst:
            contRows=parentProduct.GetContainerByName(conts).Rows
            for row in contRows:
                if row['Eng']!='' and laborDetails[row['Eng']] not in labourFinalHrsDict[parentProduct.Name].keys():
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]={}
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['ListPrice'] = float(row['Eng Total List Price']) if row['Eng Total List Price']!='' else 0
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['RegionalCost'] = round(float(row['Eng Total Regional Cost']),2) if row['Eng Total Regional Cost']!='' else 0
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['TotalHrs'] = float(row['Final Hrs']) if row['Final Hrs']!='' else 0
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['W2WCost'] = float(row['Eng Total WTW Cost']) if row['Eng Total WTW Cost']!='' else 0
                elif row['Eng']!='' and laborDetails[row['Eng']]  in labourFinalHrsDict[parentProduct.Name].keys() :
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['ListPrice'] += float(row['Eng Total List Price']) if row['Eng Total List Price']!='' else 0
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['RegionalCost']+= round(float(row['Eng Total Regional Cost']),2) if row['Eng Total Regional Cost']!='' else 0
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['TotalHrs'] += float(row['Final Hrs']) if row['Final Hrs']!='' else 0
                    labourFinalHrsDict[parentProduct.Name][laborDetails[row['Eng']]]['W2WCost'] += float(row['Eng Total WTW Cost']) if row['Eng Total WTW Cost']!='' else 0
    #Log.Write('laborhrsdict----'+str(labourFinalHrsDict))


    parentRid="0"
    parentProductName=""
    for item in arg.QuoteItemCollection:
        if item.ProductName in ['PHD Labor','Uniformance Insight Labor','AFM Labor']:
            #Log.Write(str(item.ProductName)+'---laabor cofnig write-111---'+str([item.RolledUpQuoteItem,item.ParentRolledUpQuoteItem]))
            parentRid=item.RolledUpQuoteItem
            parentProductName=item.ProductName
        if item.ParentRolledUpQuoteItem == parentRid:
            totalHrs=labourFinalHrsDict[parentProductName][item.ProductSystemId ]['TotalHrs']
            totallistPrice=labourFinalHrsDict[parentProductName][item.ProductSystemId ]['ListPrice']
            totalCost=labourFinalHrsDict[parentProductName][item.ProductSystemId ]['RegionalCost']
            w2wCost=labourFinalHrsDict[parentProductName][item.ProductSystemId ]['W2WCost']
            if int(totalHrs)!=0:
                #Log.Write(str(item.PartNumber)+'---laabor cofnig write-'+str([totalHrs,totallistPrice,totalCost,w2wCost]))
                #item.ListPrice= totallistPrice/totalHrs 
                #Log.Write(str(item.PartNumber)+'---laabor cofnig write-item.ListPrice'+str(item.ListPrice))
                item.QI_GESRegionalCost.Value = item.Cost= totalCost/totalHrs
                item.ExtendedCost = totalCost
                item.ExtendedListPrice = totallistPrice
                item['QI_UnitWTWCost'].Value = w2wCost/totalHrs
                item['QI_ExtendedWTWCost'].Value =  w2wCost
                item['QI_LaorPartsListPrice'].Value = totallistPrice/totalHrs
    #Quote.Calculate()
'''import GS_CalculateTotals as tcUtil
tcUtil.calculateParent(Quote)
Quote.Save(False)'''