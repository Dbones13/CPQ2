#Optional Table populate
def populateQuoteTableRow(table , dataDict , row = None):
    if not row:
        row = table.AddNewRow()
    for key , value in dataDict.items():
        row[key] = value

def populateOptional(Quote):
    optable=Quote.QuoteTables["Optional_FP_Items"]
    wstable = Quote.QuoteTables["WS_Table"]
    opw_table = Quote.QuoteTables['PMC_Optional_WriteIns']
    wstable_rows = []
    opserialnum = 1
    optable_data = {"SerialNr_Op":"","Description_Op":"","ModelNumber_Op":"","Quantity_Op":"","UnitPrice_Op":"","TotalPrice_Op":""}
    opw_table_row = {"SerialNr_Opw":"","PartNumber_Opw":"","Description_Opw":"","Quantity_Opw":"","UnitPrice_Opw":"","TotalPrice_Opw":""}
    opw_sr_index = 1
    optable.Rows.Clear()
    opw_table.Rows.Clear()

    for row in wstable.Rows:
        rowData = {}
        for cell in row.Cells:
            columnValue = row[cell.ColumnName]
            rowData[cell.ColumnName] = columnValue
        wstable_rows.append(rowData)

    for ws_row in wstable_rows:
        if ws_row["ItemType"]=="Optional":
            optable_data["SerialNr_Op"]=opserialnum
            optable_data["Description_Op"]=ws_row["ItemDescription"]
            optable_data["ModelNumber_Op"]=ws_row["ModelCode"]
            optable_data["Quantity_Op"]=ws_row["Quantity"]
            optable_data["UnitPrice_Op"]=ws_row["UnitPrice"]
            optable_data["TotalPrice_Op"]=ws_row["ListPrice"]
            populateQuoteTableRow(optable,optable_data)
            opserialnum += 1

    write_ins_query = SqlHelper.GetList("SELECT Product FROM WriteInProducts WHERE Category='PMC' OR Category='Common'")
    write_ins = []
    for prod in write_ins_query:
        write_ins.append(prod.Product)

    for qitem in Quote.Items:
        if qitem.PartNumber in write_ins:
            wrcat_flag = SqlHelper.GetFirst("SELECT 1 as FLAG FROM WriteInProducts WHERE (Product='{}' AND Description='{}' AND Category='{}') OR (Product='{}' AND Description='{}' AND Category='{}')".format(qitem.PartNumber,qitem.Description,'PMC',qitem.PartNumber,qitem.Description,'Common'))
            if wrcat_flag is not None and qitem.ItemType == 3:
                opw_table_row["SerialNr_Opw"]=opw_sr_index
                opw_table_row["PartNumber_Opw"]=qitem.PartNumber
                opw_table_row["Description_Opw"]=qitem.Description
                opw_table_row["Quantity_Opw"]=qitem.Quantity
                opw_table_row["UnitPrice_Opw"]=qitem.ListPrice
                opw_table_row["TotalPrice_Opw"]=qitem.ExtendedListPrice
                populateQuoteTableRow(opw_table,opw_table_row)
                opw_sr_index += 1