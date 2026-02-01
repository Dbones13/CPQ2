import GS_PasC300CG_DocumnetIOGenerater,GS_PasC300RG_DocumnetIOGenerater
import GS_C300_PASDocument_data1,GS_PasC300RG_IO_Documnet_1
def populateC300DataPoP(Quote):
    hierarchy = {
        'Level0': "New / Expansion Project",
        'Level1': "System Group",
        "Level2": "C300 System",
        "Level3":"Series-C Control Group"
    }

    QT_Table = Quote.QuoteTables["PAS_Document_Data"]
    SM = ''
    C300CGIO=0
    C300PMIO=0
    C300RGIO=0
    for Item in filter(lambda item:item.ProductName.startswith(hierarchy["Level2"]), Quote.MainItems):
        SM ='Yes'
        newRow = QT_Table.AddNewRow()
        newRow["System_Name"] = Item.ProductName
        newRow["System_Item_GUID"] = Item.QuoteItemGuid
        newRow["System_Grp_GUID"] = Item.ParentItemGuid
        newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
        contr=Item.SelectedAttributes.GetContainerByName('Series_C_Control_Groups_Cont').Rows
        for row in contr:
            C300CGIO += int(row['total_family_CG_ios_doc']) if row['total_family_CG_ios_doc']!='' else 0
            C300PMIO += int(row['pmio_ios']) if row['pmio_ios']!='' else 0
            C300PMIO += int(row['ethernet_ios']) if row['ethernet_ios']!='' else 0
            C300PMIO += int(row['turbo_ios']) if row['turbo_ios']!='' else 0
            C300PMIO += int(row['Total_Sumof_FF_IOs']) if row['Total_Sumof_FF_IOs']!='' else 0
            C300PMIO += int(row['Total_Profibus_Red_NonRed_IOs']) if row['Total_Profibus_Red_NonRed_IOs']!='' else 0
            C300RGIO += int(row['Total RG Local Io Proposal']) if row['Total RG Local Io Proposal']!='' else 0
        Trace.Write("lahu------->> "+str(C300RGIO))
        expectedResult = str(C300CGIO)
        expectedResult1 = str(C300PMIO)
        expectedResult2 = str(C300RGIO)
        newRow['C300FMIO'] = expectedResult
        newRow['C300PMIO'] = expectedResult1
        newRow['C300RGIO'] = expectedResult2

    if SM != 'Yes':
        for row in QT_Table.Rows:
            if row["System_Name"].startswith('C300 System'):
                rowId = row.Id
                QT_Table.DeleteRow(int(rowId))

    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName and row["System_Item_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber

    #for level 3
    for Item in filter(lambda item:item.ProductName == hierarchy["Level3"], Quote.MainItems):
        newRow = QT_Table.AddNewRow()
        newRow["CG_Name"] = Item.PartNumber
        newRow["CG_Item_GUID"] = Item.QuoteItemGuid
        newRow["System_Item_GUID"] = Item.ParentItemGuid
        newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem

    LST_CG_GUID = 1
    CGn = {
        "C300 System" : 0
    }
    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if Item.ProductName.startswith(hierarchy["Level2"]) and row["System_Item_GUID"] == Item.QuoteItemGuid:
                row["System_Name"] = Item.ProductName
                row["System_Item_GUID"] = Item.QuoteItemGuid
                row["System_Grp_GUID"] = Item.ParentItemGuid
                if LST_CG_GUID == Item.ParentItemGuid and row["CG_Name"] != '':
                    CGn[Item.ProductName] += int(1)
                    row["CG_No"] = str(CGn[Item.ProductName])
                elif row["CG_Name"] != '':
                    CGn = {"C300 System" : 0}
                    CGn[Item.ProductName] = 1
                    row["CG_No"] = str(CGn[Item.ProductName])
                    LST_CG_GUID = Item.ParentItemGuid

    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName and row["System_Grp_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber
    n = RIO_CNT = LIO_CNT = 0
    for Item in filter(lambda item: item.ProductName.startswith("C300 System"), Quote.MainItems):
        for child in filter(lambda item: item.ProductName == "Series-C Control Group", Item.Children):
            ioSum=GS_C300_PASDocument_data1.populateC300Data1(Quote,child)
            ioSum1=GS_PasC300CG_DocumnetIOGenerater.populateC300Data2(Quote,child)
            #LIO_CNT = sum(ioSum)
            ioSum.pop(0)
            ioSum1.pop(0)#calculation started from index 1
            expectedResult = [str(d) for d in ioSum]
            expectedResult1 = [str(a) for a in ioSum1]
            Trace.Write("Expected Result CG: "+str(expectedResult))
            Trace.Write("Expected Result SubCG: "+str(expectedResult1))
            for row in QT_Table.Rows:
                if row['System_Item_GUID'] == Item.QuoteItemGuid:
                    if row['CG_Item_GUID'] == child.QuoteItemGuid:
                        row['CG'] = "|".join(expectedResult)
                        row['SUBCG'] = "|".join(expectedResult1)
                        row['Local_IO']= LIO_CNT
            n = 0
            for rg in filter(lambda item: item.ProductName == "Series-C Remote Group", child.Children):
                    n += 1
                    rgIoSum=GS_PasC300RG_DocumnetIOGenerater.populateC300Data2(Quote,rg)
                    rgIoSum1=GS_PasC300RG_IO_Documnet_1.populateC300RGData1(Quote,rg)
                    rgIoSum.pop(0) #calculation started from index 1
                    rgIoSum1.pop(0)
                    expectedResult = [str(d) for d in rgIoSum]
                    expectedResult1 = [str(a) for a in rgIoSum1]
                    Trace.Write("Expected Result RG: "+str(expectedResult))
                    for row in QT_Table.Rows:
                        if row['System_Item_GUID'] == Item.QuoteItemGuid:
                            if row['CG_Item_GUID'] == child.QuoteItemGuid:
                                row['RG'+str(n)] = "|".join(expectedResult1)
                                row['SubRG'+str(n)] = "|".join(expectedResult)
                                row['Remote_IO'] = RIO_CNT
                                row['Remote_Qty'] = str(n)
                                if n == 1:
                                    row['RGNames'] = rg.PartNumber
                                else:
                                    row['RGNames'] = row['RGNames'] + "|" + rg.PartNumber

    QT_Table.Save()
    if SM != 'Yes':
        return False
    else:
        return True
#populateC300DataPoP(Quote)