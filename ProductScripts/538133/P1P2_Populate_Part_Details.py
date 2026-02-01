#Quote.CustomFields.AssignValue('Pole',"EMEA")
p1p2valid = Product.GetContainerByName("SC_P1P2_Parts_Details")
p1p2invalid = Product.GetContainerByName("SC_P1P2_Invalid_Parts")
to_be_deleted = []
to_be_added = {}
list_index = 0
serProd = {}
try:
    Pole = Quote.GetCustomField("Pole").Content
    BookingCountry = Quote.GetCustomField("Booking Country").Content
except:
    Pole = ""
    BookingCountry = ""

if Pole == "APAC":
    Pole = "JP" if BookingCountry == "japan" else "SG"

if Product.Attr('SC_Product_Type').GetValue() == "New":
    if p1p2valid.Rows.Count > 0:
        for row in p1p2valid.Rows:
            if True:
                query = SqlHelper.GetFirst("select PartNumber from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(row['Part_Number']))
                if query is not None:
                    desc = SqlHelper.GetFirst("SELECT PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}'".format(row['Part_Number']))
                    if row["Service_Product"] not in serProd.keys():
                        serProd[row["Service_Product"]] = [row["Part_Number"]]
                    else:
                        if row["Part_Number"] in serProd[row["Service_Product"]] and query is not None:
                            invalidrow = p1p2invalid.AddNewRow()
                            invalidrow['Service_Product'] = row['Service_Product']
                            invalidrow['Part_Number'] = row['Part_Number']
                            invalidrow['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            invalidrow['Reason'] = "Duplicate Entry"
                            invalidrow['Qty'] = '0'
                            invalidrow['Hidden_Quantity'] = '0'
                            to_be_deleted.append(row.RowIndex)
                            continue
                        else:
                            serProd[row["Service_Product"]].append(row["Part_Number"])
                    partstatusquery = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(row['Part_Number'],Pole))
                    if partstatusquery is not None:
                        if partstatusquery.PartStatus == "Inactive" and partstatusquery.Replacement_Status != "Direct replacement":
                            invalidrow = p1p2invalid.AddNewRow()
                            invalidrow['Service_Product'] = row['Service_Product']
                            invalidrow['Part_Number'] = row['Part_Number']
                            invalidrow['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            invalidrow['Qty'] = '0'
                            invalidrow['Hidden_Quantity'] = '0'
                            invalidrow['Reason'] = 'Model is not active'
                            to_be_deleted.append(row.RowIndex)
                        elif partstatusquery.Replacement_Status == "Direct replacement":
                            row['Part_Status'] = partstatusquery.PartStatus
                            row['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            row['Replacement_Status'] = partstatusquery.Replacement_Status
                            row['Replacement_Part'] = partstatusquery.Replacement_Part
                            row['Qty'] = '0'
                            row['Hidden_Quantity'] = '0'
                            partstatusquerynew = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(partstatusquery.Replacement_Part,Pole))
                            if partstatusquerynew is not None:
                                if partstatusquerynew.PartStatus == 'Active':
                                    newquery = SqlHelper.GetFirst("select PartNumber from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(partstatusquery.Replacement_Part))
                                    if newquery is not None:
                                        desc1 = SqlHelper.GetFirst("SELECT PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}'".format(row['Part_Number']))
                                        description1 = desc1.PRODUCT_NAME if desc1 is not None else ""
                                        list_index += 1
                                        to_be_added[list_index] = [row['Service_Product'],partstatusquery.Replacement_Part,partstatusquerynew.PartStatus,description1,row['Qty'],partstatusquerynew.Replacement_Status,partstatusquerynew.Replacement_Part]
                        else:
                            row['Part_Status'] = partstatusquery.PartStatus
                            row['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            row['Replacement_Status'] = partstatusquery.Replacement_Status
                            row['Replacement_Part'] = partstatusquery.Replacement_Part

    to_be_deleted.reverse()
    for i in to_be_deleted:
        p1p2valid.DeleteRow(i)
        p1p2valid.Calculate()

    for j in range(1,len(to_be_added)+1):
        if to_be_added[j][1] not in serProd[to_be_added[j][0]]:
            newrow = p1p2valid.AddNewRow(False)
            newrow.GetColumnByName('Service_Product').SetAttributeValue(to_be_added[j][0])
            newrow['Service_Product'] = to_be_added[j][0]
            newrow['Part_Number'] = to_be_added[j][1]
            newrow['Part_Status'] = to_be_added[j][2]
            newrow['Description'] = to_be_added[j][3]
            newrow['Qty'] = to_be_added[j][4]
            newrow['Hidden_Quantity'] = to_be_added[j][4]
            newrow['Replacement_Status'] = to_be_added[j][5]
            newrow['Replacement_Part'] = to_be_added[j][6]
            newrow.Calculate()
            import GS_GetPriceFromCPS
            priceDict = GS_GetPriceFromCPS.getPrice(Quote,{},[newrow['Part_Number']],TagParserQuote,Session)
            if len(priceDict)>0:
                newrow["Unit_Price"] = priceDict[newrow["Part_Number"]]
                if newrow["Qty"] not in ("0",""):
                    newrow["Ext_Price"] = str(eval(newrow["Qty"])*eval(newrow['Unit_Price']))
                    newrow["Hidden_ListPrice"] = str(eval(newrow["Qty"])*eval(newrow['Unit_Price']))
            else:
                newrow["Unit_Price"] = "0"
                newrow["Ext_Price"] = "0"
                newrow["Hidden_ListPrice"] = "0"
            p1p2valid.Calculate()

if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    if p1p2valid.Rows.Count > 0:
        for row in p1p2valid.Rows:
            if True:
                query = SqlHelper.GetFirst("select PartNumber from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(row['Part_Number']))
                if query is not None:
                    desc = SqlHelper.GetFirst("SELECT PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}'".format(row['Part_Number']))
                    if row["Service_Product"] not in serProd.keys():
                        serProd[row["Service_Product"]] = [row["Part_Number"]]
                    else:
                        if row["Part_Number"] in serProd[row["Service_Product"]] and query is not None:
                            invalidrow = p1p2invalid.AddNewRow()
                            invalidrow['Service_Product'] = row['Service_Product']
                            invalidrow['Part_Number'] = row['Part_Number']
                            invalidrow['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            invalidrow['Reason'] = "Duplicate Entry"
                            invalidrow['CY_Quantity'] = '0'
                            invalidrow['Hidden_Quantity'] = '0'
                            to_be_deleted.append(row.RowIndex)
                            continue
                        else:
                            serProd[row["Service_Product"]].append(row["Part_Number"])
                    partstatusquery = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(row['Part_Number'],Pole))
                    if partstatusquery is not None:
                        if partstatusquery.PartStatus == "Inactive" and partstatusquery.Replacement_Status != "Direct replacement" and row["Product_type"] != "Renewal":
                            invalidrow = p1p2invalid.AddNewRow()
                            invalidrow['Service_Product'] = row['Service_Product']
                            invalidrow['Part_Number'] = row['Part_Number']
                            invalidrow['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            invalidrow['CY_Quantity'] = '0'
                            invalidrow['Hidden_Quantity'] = '0'
                            invalidrow['Reason'] = 'Model is not active'
                            to_be_deleted.append(row.RowIndex)
                        elif partstatusquery.Replacement_Status == "Direct replacement" and row['Service_Product'] == "Parts Holding P2":
                            row['Part_Status'] = partstatusquery.PartStatus
                            row['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            row['Replacement_Status'] = partstatusquery.Replacement_Status
                            row['Replacement_Part'] = partstatusquery.Replacement_Part
                            row['CY_Quantity'] = '0'
                            row['BackupRenewalQuantity'] = '0'
                            row['Hidden_Quantity'] = '0'
                            partstatusquerynew = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(partstatusquery.Replacement_Part,Pole))
                            if partstatusquerynew is not None:
                                if partstatusquerynew.PartStatus == 'Active':
                                    newquery = SqlHelper.GetFirst("select PartNumber from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(partstatusquery.Replacement_Part))
                                    if newquery is not None:
                                        desc1 = SqlHelper.GetFirst("SELECT PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}'".format(row['Part_Number']))
                                        description1 = desc1.PRODUCT_NAME if desc1 is not None else ""
                                        list_index += 1
                                        to_be_added[list_index] = [row['Service_Product'],partstatusquery.Replacement_Part,partstatusquerynew.PartStatus,description1,row['CY_Quantity'],partstatusquerynew.Replacement_Status,partstatusquerynew.Replacement_Part]
                        else:
                            row['Part_Status'] = partstatusquery.PartStatus
                            row['Description'] = desc.PRODUCT_NAME if desc is not None else ""
                            row['Replacement_Status'] = partstatusquery.Replacement_Status
                            row['Replacement_Part'] = partstatusquery.Replacement_Part

    to_be_deleted.reverse()
    for i in to_be_deleted:
        p1p2valid.DeleteRow(i)
        p1p2valid.Calculate()

    for j in range(1,len(to_be_added)+1):
        if to_be_added[j][1] not in serProd[to_be_added[j][0]]:
            newrow = p1p2valid.AddNewRow(False)
            newrow.GetColumnByName('Service_Product').SetAttributeValue(to_be_added[j][0])
            newrow['Service_Product'] = to_be_added[j][0]
            newrow['Part_Number'] = to_be_added[j][1]
            newrow['Part_Status'] = to_be_added[j][2]
            newrow['Description'] = to_be_added[j][3]
            newrow['CY_Quantity'] = to_be_added[j][4]
            newrow['BackupRenewalQuantity'] = to_be_added[j][4]
            newrow['Hidden_Quantity'] = to_be_added[j][4]
            newrow['Replacement_Status'] = to_be_added[j][5]
            newrow['Replacement_Part'] = to_be_added[j][6]
            newrow['Comments'] = "Scope Addition"
            newrow.Calculate()
            import GS_GetPriceFromCPS
            priceDict = GS_GetPriceFromCPS.getPrice(Quote,{},[newrow['Part_Number']],TagParserQuote,Session)
            if len(priceDict)>0:
                newrow["Unit_Price"] = priceDict[newrow["Part_Number"]]
                if newrow["CY_Quantity"] not in ("0",""):
                    newrow["CY_ExtPrice"] = str(eval(newrow["CY_Quantity"])*eval(newrow['Unit_Price']))
                    newrow["Hidden_ListPrice"] = str(eval(newrow["CY_Quantity"])*eval(newrow['Unit_Price']))
            else:
                newrow["Unit_Price"] = "0"
                newrow["CY_ExtPrice"] = "0"
                newrow["Hidden_ListPrice"] = "0"
            p1p2valid.Calculate()