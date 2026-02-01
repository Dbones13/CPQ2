def validateModel(cont, productType):
    list_error = []
    if productType == 'New':
        error_msg1 = 'Asset, Model and description is mandatory for all added models.'
        error_msg2 = 'Quantity and unit price and unit cost is mandatory for all added models.'
        error_msg3 = 'List price and Cost Price is mandatory for all added models.'
    else:
        error_msg1 = 'Asset, Model and description is mandatory for all added models.'
        error_msg2 = 'Renewal quantity and unit price and unit cost is mandatory for all added models.'
        error_msg4 = 'Previous Year Quantity is mandatory for all added models.'
        error_msg5 = 'Previous Year List Price is mandatory for all added models.'
        error_msg6 = 'Previous Year Cost Price is mandatory for all added models.'
        error_msg3 = 'Honeywell List price and Current Year Cost Price is mandatory for all added models.'

    error_msg = ''
    if cont.Rows.Count:
        for row in cont.Rows:
            preYearQty= listPrice=unitCost= 0
            Preqty = PreCost = PrelistPrice= qty=preYearQty=0
            if productType == 'New':
                qty = row['Quantity'] if row['Quantity'] else 0
                listPrice = row['Unit List Price'] if row['Unit List Price'] else 0
                unitCost = row['Unit Cost'] if row['Unit Cost'] else 0
                description = row["Description"]
                model = row["3rd Party Model"]
                asset = row["Asset"]
            else:
                preYearQty = row['SC_Quantity_HR_RWL'] if row['SC_Quantity_HR_RWL'] else 0
                qty = row['SC_RenewalQuantity_HR_RWL'] if row['SC_RenewalQuantity_HR_RWL'] else 0
                listPrice = row['SC_HoneywellListPrice_HR_RWL'] if row['SC_HoneywellListPrice_HR_RWL'] else 0
                unitCost = row['SC_CurrentYearUnitCostPrice_HR_RWL'] if row['SC_CurrentYearUnitCostPrice_HR_RWL'] else 0
                Preqty = row['SC_Quantity_HR_RWL'] if row['SC_Quantity_HR_RWL'] else 0
                PrelistPrice = row['SC_PreviousYearListPrice_HR_RWL'] if row['SC_PreviousYearListPrice_HR_RWL'] else 0
                PreCost = row['SC_PreviousYearCostPrice_HR_RWL'] if row['SC_PreviousYearCostPrice_HR_RWL'] else 0
                description = row["SC_Description_HR_RWL"]
                model = row["SC_Model_HR_RWL"]
                asset = row["SC_Asset_HR_RWL"]
            if Preqty =='' and productType == 'Renewal':
                error_msg += error_msg4 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            if PrelistPrice =='' and productType == 'Renewal':
                error_msg += error_msg5 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            if PreCost=='' and productType == 'Renewal':
                error_msg += error_msg6 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            if asset == '' or model == "" or description == "":
                """if error_msg1 not in list_error:
                    list_error.append(error_msg1 + "(row:"+ str(row.RowIndex+1) + ")")"""
                error_msg += error_msg1 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            if (float(qty) == 0 and float(preYearQty) == 0):
                """if error_msg2 not in list_error:
                    list_error.append(error_msg2 + "(row:"+ str(row.RowIndex+1) + ")")"""
                error_msg += error_msg2 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            elif float(listPrice) == 0 or float(unitCost) == 0:
                """if error_msg3 not in list_error
                    list_error.append(error_msg3 + "(row:"+ str(row.RowIndex+1) + ")")"""
                error_msg += error_msg3 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            """if len(list_error) == 2:
                break"""
    else:
        #list_error.append('No model available')
        error_msg = 'No model available'

    return error_msg

def validateModellss(cont, productType):
    if productType == 'New':
        error_msg1 = 'Model is mandatory for all added models.'
        error_msg2 = 'Unit List price and Unit Cost Price is mandatory for all added models.'
        error_msg3 = 'Description is mandatory for all added models.'
    else:
        error_msg1 = 'Model -Should not be Blank.'
        error_msg2 = 'Description-Should not be Blank'
        error_msg3 = 'Previous Year Quantity -Should not be Blank & can be zero'
        error_msg4 = 'Renewal Quantity -Should not be Blank & can be zero'
        error_msg5 = 'Honeywell List Price -Should not be Blank & Cannot be zero'
        error_msg6 = 'Current Year Cost Price -Should not be Blank & Cannot be zero'

    error_msg = ''
    if cont.Rows.Count:
        for row in cont.Rows:
            if productType == 'New':
                listPrice = row['Unit List Price']if row['Unit List Price'] else 0
                unitCost = row['Unit Cost  Price'] if row['Unit Cost  Price'] else 0
                description = row["Description"]
                model = row["Model"]

                if model == "":
                    error_msg += error_msg1 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if description == "":
                    error_msg += error_msg3 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if (float(unitCost) == 0 or float(listPrice) == 0):
                    error_msg += error_msg2 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
            else:
                preYearQty = row['Previous Year Quantity'] if row['Previous Year Quantity'] else 0
                qty = row['Renewal Quantity'] if row['Renewal Quantity'] else 0
                listPrice = row['Honeywell List Price Per Unit'] if row['Honeywell List Price Per Unit'] else 0
                Trace.Write(row['Honeywell List Price Per Unit'])
                unitCost = row['Current Year Unit Cost Price'] if row['Current Year Unit Cost Price'] else 0
                description = row["Description"]
                model = row["Model"]
                if model == "":
                    error_msg += error_msg1 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if description == "":
                    error_msg += error_msg2 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if preYearQty == "":
                    error_msg += error_msg3 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if qty == "":
                    error_msg += error_msg4 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if listPrice == "" or float(listPrice) == 0:
                    error_msg += error_msg5 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
                if unitCost == "" or float(unitCost) ==0:
                    error_msg += error_msg6 + "(row:"+ str(row.RowIndex+1) + ")<br/>"
    else:
        error_msg = 'No model available'

    return error_msg

productType = Product.Attr('SC_Product_Type').GetValue()
if Product.Name in ['Hardware Warranty', 'Hardware Refresh'] and productType in ['New', 'Renewal']:
    cont = Product.GetContainerByName('SC_ValidModels_HR_RWL')
    if productType == 'New':
        cont = Product.GetContainerByName('HWOS_Model Scope_3party')

    Product.Attr("Error_Message").AssignValue('')
    error_msg = validateModel(cont, productType)
    if error_msg:
        Product.Attr("Error_Message").AssignValue(error_msg)
elif Product.Name in ['Local Support Standby'] and productType in ['New', 'Renewal']:
    cont = Product.GetContainerByName('SC_Local_Support_Standby_validModel')
    Product.Attr("Error_Message").AssignValue('')
    error_msg = validateModellss(cont, productType)
    if error_msg:
        Product.Attr("Error_Message").AssignValue(error_msg)