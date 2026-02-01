import GS_SM_Part_Update
import GS_SM_System_PartSumary_Calcs
import GS_SM_Hardware_Safety_Parts

parts_dict = {}
cont = Product.GetContainerByName('SM_System_PartSummary_Cont')
try:
    parts_dict = GS_SM_System_PartSumary_Calcs.get_System_parts(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_System_PartSumary_Calcs: " + str(e))
try:
    parts_dict = GS_SM_Hardware_Safety_Parts.getSMSystemParts(Product,parts_dict)
except Exception,e:
    Trace.Write(str(e))

Trace.Write("debugging: " + str(parts_dict))
GS_SM_Part_Update.execute(Product, 'SM_System_PartSummary_Cont', parts_dict)
cont.Calculate()

sm_cont_rows = cont.Rows
errorFlag = False
for row in sm_cont_rows:
    finalQuantity = int(row['CE_Final_Quantity'])
    if finalQuantity < 0:
        errorFlag = True
        break
if errorFlag:
    #Product.ErrorMessages.Add("Please check part number with -ve qty in Final Quantity Column and update value in '+/- Adj Quantity' column")
    Product.Attr('PartSummaryErrorMsg').AssignValue('True')
    Trace.Write('Error Flag True: ' + str(errorFlag))
else:
    Trace.Write('Error Flag False: ' + str(errorFlag))
    Product.Attr('PartSummaryErrorMsg').AssignValue('False')
    sm_cont_rows = Product.GetContainerByName('SM_System_PartSummary_Cont').Rows
    sm_li_cont = Product.GetContainerByName('SM_System_PartSummary_LI_Cont')
    sm_li_cont.Rows.Clear()
    for row in sm_cont_rows:
        part = row['CE_Part_Number']
        quantity = row['CE_Part_Qty']
        part_description = row['CE_Part_Description']
        adjQuantity = row['CE_Adj_Quantity'] if row['CE_Adj_Quantity'] else 0
        comments = row['CE_Comments']
        finalQuantity = int(row['CE_Final_Quantity'])
        if finalQuantity > 0:
            row = sm_li_cont.AddNewRow(part, False)
            row.GetColumnByName("CE_Part_Qty").Value = quantity
            row.GetColumnByName("CE_Part_Description").Value = part_description
            row.GetColumnByName("CE_Adj_Quantity").Value = str(adjQuantity)
            row.GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(finalQuantity))
            row.GetColumnByName("CE_Comments").Value = comments
            row.Calculate()
	sm_li_cont.Calculate()
#Product.ApplyRules()