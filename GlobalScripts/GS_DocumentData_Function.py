def getMsidBOM(item):
    bomDict = dict()
    msidList = list()
    msidGuidMap = dict()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        msidGuidMap[msid.QuoteItemGuid] = msid.PartNumber
        partDict = bomDict.get(msid.QuoteItemGuid , dict())
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                if (part.Description == 'ControlEdge PLC System Migration' and  part.PartNumber == 'PLC') or (part.Description == 'ControlEdge UOC System Migration' and  part.PartNumber == 'UOC'):
                    for child in part.Children:
                        if child.PartNumber.startswith('SVC'):
                            continue
                        if child.Description == 'CE PLC Control Group' or child.Description == 'UOC Control Group':
                            def temp2(child,partDict,msid):
                                for i in child.Children:
                                    if i.PartNumber.startswith('SVC'):
                                        continue
                                    if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                        temp2(i,partDict,msid)
                                        continue
                                    partData1 = partDict.get(i.PartNumber , ["" , 0,"","",""])
                                    partData1[0] = i.Description
                                    partData1[1] += i.Quantity
                                    partData1[2] = i['QI_PLSG'].Value
                                    partData1[3] = msid.Description
                                    partData1[4] = i.ProductTypeName
                                    partDict[i.PartNumber] = partData1
                            temp2(child,partDict,msid)
                            continue
                        partData = partDict.get(child.PartNumber , ["" , 0,"","",""])
                        partData[0] = child.Description
                        partData[1] += child.Quantity
                        partData[2] = child['QI_PLSG'].Value
                        partData[3] = msid.Description
                        partData[4] = child.ProductTypeName
                        partDict[child.PartNumber] = partData
                    continue    
                # elif part.Description == 'CE PLC Control Group' or part.Description == 'UOC Control Group':
                    # def temp(part,partDict,msid):
                        # for i in part.Children:
                            # if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                # temp(i,partDict,msid)
                                # continue
                            # partData1 = partDict.get(i.PartNumber , ["" , 0,"","",""])
                            # partData1[0] = i.Description
                            # partData1[1] += i.Quantity
                            # partData1[2] = i['QI_PLSG'].Value
                            # partData1[3] = msid.Description
                            # partData1[4] = i.ProductTypeName
                            # partDict[i.PartNumber] = partData1
                    # temp(part,partDict,msid)
                    # continue
                partData = partDict.get(part.PartNumber , ["" , 0,"","",""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part['QI_PLSG'].Value
                partData[3] = msid.Description
                partData[4] = part.ProductTypeName
                partDict[part.PartNumber] = partData
        bomDict[msid.QuoteItemGuid] = partDict
    return (msidList , bomDict,msidGuidMap)

def getMigrationBomDictConsolidated(item):
    bomDict = dict()
    msidList = list()
    msidGuidMap = dict()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                if (part.Description == 'ControlEdge PLC System Migration' and  part.PartNumber == 'PLC') or (part.Description == 'ControlEdge UOC System Migration' and  part.PartNumber == 'UOC'):
                    for child in part.Children:
                        if child.PartNumber.startswith('SVC'):
                            continue
                        if child.Description == 'CE PLC Control Group' or child.Description == 'UOC Control Group':
                            def temp3(child,partDict,msid):
                                for i in child.Children:
                                    if i.PartNumber.startswith('SVC'):
                                        continue
                                    if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                        temp3(i,partDict,msid)
                                        continue
                                    partData1 = bomDict.get(i.PartNumber , ["" , 0, ""])
                                    partData1[0] = i.Description
                                    partData1[1] += i.Quantity
                                    partData1[2] = i.ProductTypeName
                                    bomDict[i.PartNumber] = partData1
                            temp3(child,partDict,msid)
                            continue
                        partData = bomDict.get(child.PartNumber , ["" , 0 , ""])
                        partData[0] = child.Description
                        partData[1] += child.Quantity
                        partData[2] = child.ProductTypeName
                        bomDict[child.PartNumber] = partData
                    continue        
                # elif part.Description == 'CE PLC Control Group' or part.Description == 'UOC Control Group':
                    # def temp4(part,bomDict):
                        # for i in part.Children:
                            # if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                # temp4(i,bomDict)
                                # continue
                            # partData1 = bomDict.get(i.PartNumber , ["" , 0, ""])
                            # partData1[0] = i.Description
                            # partData1[1] += i.Quantity
                            # partData1[2] = i.ProductTypeName
                            # bomDict[i.PartNumber] = partData1
                    # temp4(part,partDict)
                    # continue
                partData = bomDict.get(part.PartNumber , ["" , 0 , ""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part.ProductTypeName
                bomDict[part.PartNumber] = partData
                Trace.Write("bomDict:{0}".format(bomDict))
    return (msidList , bomDict,msidGuidMap)

def getMigrationBomDictByMsid(item):
    bomDict = dict()
    msidList = list()
    msidGuidMap = dict()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        msidGuidMap[msid.QuoteItemGuid] = msid.PartNumber
        partDict = bomDict.get(msid.QuoteItemGuid , dict())
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                if (part.Description == 'ControlEdge PLC System Migration' and  part.PartNumber == 'PLC') or (part.Description == 'ControlEdge UOC System Migration' and  part.PartNumber == 'UOC'):
                    for child in part.Children:
                        if child.PartNumber.startswith('SVC'):
                            continue
                        if child.Description == 'CE PLC Control Group' or child.Description == 'UOC Control Group':
                            def temp5(child,partDict,msid):
                                for i in child.Children:
                                    if i.PartNumber.startswith('SVC'):
                                        continue
                                    if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                        temp5(i,partDict,msid)
                                        continue
                                    partData1 = partDict.get(i.PartNumber , ["" , 0, ""])
                                    partData1[0] = i.Description
                                    partData1[1] += i.Quantity
                                    partData1[2] = i.ProductTypeName
                                    partDict[i.PartNumber] = partData1
                            temp5(child,partDict,msid)
                            continue
                        partData = partDict.get(child.PartNumber , ["" , 0 , ""])
                        partData[0] = child.Description
                        partData[1] += child.Quantity
                        partData[2] = child.ProductTypeName
                        partDict[child.PartNumber] = partData
                    continue
                # elif part.Description == 'CE PLC Control Group' or part.Description == 'UOC Control Group':
                    # def temp6(part,partDict):
                        # for i in part.Children:
                            # if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                # temp6(i,partDict)
                                # continue
                            # partData1 = partDict.get(i.PartNumber , ["" , 0, ""])
                            # partData1[0] = i.Description
                            # partData1[1] += i.Quantity
                            # partData1[2] = i.ProductTypeName
                            # partDict[i.PartNumber] = partData1
                    # temp6(part,partDict)
                    # continue
                partData = partDict.get(part.PartNumber , ["" , 0, ""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part.ProductTypeName
                partDict[part.PartNumber] = partData
                Trace.Write("partDict:{0}".format(partDict))
        bomDict[msid.QuoteItemGuid] = partDict
    return (msidList , bomDict,msidGuidMap)

def DeleteQuoteTableItem(quoteItemGuids,Quote):
    table = Quote.QuoteTables["Migration_Document_Data"]
    item_delete = [row.Id for row in table.Rows if row['MIgration_GUID'] and row['MIgration_GUID'] not in quoteItemGuids]
    for r in sorted(item_delete, reverse=True):
        table.DeleteRow(r)
    table.Save()

def Delete_Quote_Item(Quote):
	quoteType = Quote.GetCustomField("Quote Type").Content
	lob = Quote.GetCustomField("Booking LOB").Content

	quoteItemGuids = []
	if lob == "LSS" and quoteType not in ('Contract New','Contract Renewal'):
		if Quote.ContainsAnyProductByPartNumber('IAA -Project') or Quote.ContainsAnyProductByPartNumber('IAA -Spot') :
			quoteItemGuids = [x.QuoteItemGuid for x in Quote.MainItems if x.PartNumber in ('IAA -Project','IAA -Spot' )]
			DeleteQuoteTableItem(quoteItemGuids,Quote)