# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)

#Hide the calculate button when the product is loaded
import datetime
# EXPERION_ENT_DISPLAYS_SHAPES_FACEPLATES1
if TagParserProduct.ParseString('<*value(Is HMI Engineering in Scope?)*>')=='Yes':
    #TagParserProduct.ParseString('<*AllowAttributes(Experion_Ent_Displays_Shapes_Faceplates)*>')
    def sortRow(cont,rank,new_row_index):
        sort_needed = True
        if new_row_index == 0:
            return
        while sort_needed == True:
            Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
            if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
                cont.MoveRowUp(new_row_index, False)
                new_row_index -= 1
            else:
                sort_needed = False
    Product.ExecuteRulesOnce = True
    laborCont = Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates')
    tableLabor = SqlHelper.GetList('select Displays_Shapes_Faceplates,Rank from EXPERION_ENT_DISPLAYS_SHAPES_FACEPLATES1')
    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Displays/Shapes/Faceplates').Value)
    
    for row in tableLabor:
        if row.Displays_Shapes_Faceplates not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Displays/Shapes/Faceplates"] = row.Displays_Shapes_Faceplates
            new_row["rank"] = str(row.Rank)
            #sortRow(laborCont,row.Rank,new_row.RowIndex)
        elif row.Displays_Shapes_Faceplates in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Displays_Shapes_Faceplates == cont_row.GetColumnByName('Displays/Shapes/Faceplates').Value:
                    rows_to_delete.append(cont_row.RowIndex)
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    Product.ExecuteRulesOnce = False
#Rule_to_code_changes start
EP_PKS511_ESD_Inputs_Cont = Product.GetContainerByName('EP-PKS511-ESD')
if EP_PKS511_ESD_Inputs_Cont:
	EP_PKS511_ESD = EP_PKS511_ESD_Inputs_Cont.Rows[0].GetColumnByName('EP-PKS511-ESD').Value
	if Product.Attr('Experion Software Release').GetValue() != 'R511' or Product.Attr('Experion Base Media Delivery').GetValue() != 'Electronic Download':
		Product.Attr('Exp_Ent_Sys_Part_Summary').AssignValue(EP_PKS511_ESD)
	if Product.Attr('Experion Software Release').GetValue() == 'R511' and Product.Attr('Experion Base Media Delivery').GetValue() == 'Electronic Download':
		Product.Attr('Exp_Ent_Sys_Part_Summary').AssignValue(EP_PKS511_ESD)
	#if Product.Attr('Network Assessment in scope?').GetValue() != 'Yes':
	#	Product.Attr('Network Assessment in scope?').AssignValue('No')
	#if Product.Attr('Is HART Interface in Scope?').GetValue() != 'Yes':
	#	Product.DisallowAttr('Is HART in C300 Controller?')
#Rule_to_code_changes end