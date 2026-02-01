#import sys

def add_part(cont, parts_to_add, Product):
    for part in parts_to_add:
        try:
            row = cont.AddNewRow(part, False)
            #row.GetColumnByName('CE_Part_Qty').Value = str(int(parts_to_add[part]))
            row.GetColumnByName("CE_Part_Qty").Value = str(int(parts_to_add[part]))
            #row.GetColumnByName("CE_Part_Description").Value = (str(parts_to_add[part]['Description']))
            row.GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(int(parts_to_add[part])))
            #row.GetColumnByName("CE_Final_Quantity").Value = str(int(parts_to_add[part]['Quantity']))
            row.Calculate()
        except Exception,e:
            Product.ErrorMessages.Add("Error when adding Part Number {0}. Please verify this product exists in CPQ and is added to the container. Full Message: {1}".format(part,e))

def delete_part(cont, parts_to_delete):
    parts_to_delete.sort(reverse=True) #default key is first element of tuple (index). Reverse sort is needed otherwise it will delete every other row because the row index changes.
    for part in parts_to_delete:
        cont.DeleteRow(part[0])

def update_qty(cont, parts_to_update,Product):
    for part in parts_to_update: #dictionary where key is index, and value is new qty
        #cont.Rows[part].GetColumnByName('CE_Part_Qty').Value = str(int(parts_to_update[part]))
        quantity = int(parts_to_update[part])
        adjQuantity = cont.Rows[part].GetColumnByName("CE_Adj_Quantity").Value
        cont.Rows[part].GetColumnByName("CE_Part_Qty").Value = str(int(quantity))
        adjQuantity = adjQuantity if adjQuantity else 0
        finalQuantity = quantity + int(adjQuantity)
        cont.Rows[part].GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(int(finalQuantity)))
        if finalQuantity < 0:
            Product.Attr('PartSummaryErrorMsg').AssignValue('True')
        cont.Rows[part].Calculate()
        #cont.Rows[part].GetColumnByName("CE_Part_Qty").ReferencingAttribute.AssignValue(str(int(parts_to_update[part])))
        #qty = cont.Rows[part].GetColumnByName('CE_Final_Quantity').Value
        #cont.Rows[part].GetColumnByName("CE_Part_Qty").ReferencingAttribute.AssignValue(str(int(qty)))
        #cont.Rows[part].Calculate()

def get_current_parts(cont):
    current_parts = []
    for row in cont.Rows:
        current_parts.append((row.RowIndex, row.GetColumnByName('CE_Part_Number').Value,row.GetColumnByName('CE_Part_Qty').Value)) #this is a list of tuples
    return current_parts

def compare(current_parts, parts_dict):
    #Compare
    parts_to_add = {}
    parts_to_update = {}
    for part in parts_dict:
        part_found = False
        for row in current_parts:
            if row[1] == part: #comparing part numbers
                part_found = True
                if parts_dict[part] == 0: #This leaves it in the current_parts list, which will ensure the part gets deleted
                    break
                if (row[2] != str(int(parts_dict[part]))): #comparing qtys
                    parts_to_update[row[0]] = parts_dict[part]
                current_parts.remove(row) #this is within the if condition so that if qty = 0, the part is deleted.
                break
        if part_found == False and parts_dict[part] != 0:
            #parts_to_add[part] = {}
            parts_to_add[part] = parts_dict[part]
            #parts_to_add[part]['Description'] = parts_dict[part]['Description']
    return parts_to_add, parts_to_update, current_parts

def execute(Product, container_name, parts_dict, attrs= None):
    cont = Product.GetContainerByName(container_name)

    if attrs and ((Product.Name in ['CE PLC Control Group','UOC Control Group']  and str(attrs.ctrl_rack_ctrl_type) == 'NonRedundant') or (Product.Name in ['CE PLC Remote Group','UOC Remote Group'])) and  str(attrs.ctrl_rack_pwr_status_mod_red_sply)== 'No' and attrs.ctrl_rack_pwr_sply == 'NonRedundant':
        if parts_dict.get('900RNF-0200'):
            del parts_dict['900RNF-0200']

    current_parts = get_current_parts(cont)
    parts_to_add, parts_to_update, parts_to_delete = compare(current_parts, parts_dict)

    Trace.Write("Parts to Add: {parts_to_add}, Parts to Update: {parts_to_update}, Parts to Delete: {parts_to_delete}".format(parts_to_add=parts_to_add,parts_to_update=parts_to_update, parts_to_delete=parts_to_delete))
    add_part(cont, parts_to_add, Product)
    update_qty(cont, parts_to_update, Product)
    delete_part(cont, parts_to_delete)