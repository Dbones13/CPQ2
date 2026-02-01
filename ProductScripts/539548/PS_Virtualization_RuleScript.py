def hide_column(container, Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container, Column))
def show_column(container, Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container, Column))
def getfloat(val):
	if val:
		try:
			return float(val)
		except:
			return 0
	return 0
def SetCalculatedandFinal(Deliverable,data):
    virtualizationCon = Product.GetContainerByName("MSID_Labor_Virtualization_con")
    for row in virtualizationCon.Rows:
        if row["Deliverable"] == Deliverable:
            row["Calculated_Hrs"]=str(getfloat(data))
            Final_Hrs=getfloat(data)*getfloat(row["Adjustment_Productivity"])
            row["Final_Hrs"]=str(Final_Hrs)
            break

data,hwdata,doc,offdata,fatdata,onsitedata,satdata = '','','','','','',''

Parent_Container = Product.GetContainerByName('CONT_MSID_SUBPRD').Rows
for row in Parent_Container:
    if row['Selected_Products'] in ('Virtualization System Migration', 'Virtualization System'):
        data = row['Plan_review_Kick_off_Meetings']
        hwdata = row['HW_SW_order_to_factory']
        doc = row['Documentation']
        offdata = row['Off_Site_Config_activities']
        fatdata = row['FAT']
        onsitedata = row['On_Site_activities']
        satdata = row['SAT']
    	break

SelectedProduct = Product.Attr('MSID_Selected_Products').GetValue()
Scope = Product.Attr('MIgration_Scope_Choices').GetValue()

if ('Virtualization System Migration' in SelectedProduct or 'Virtualization System' in SelectedProduct) and (Scope  in ['LABOR', 'HW/SW/LABOR']):
    Product.Attr('msid_virtualization_Plan_review_Kick_off_Meeting').AssignValue(data)
    Product.Attr('msid_virtualization_HW_SW_order_to_factory').AssignValue(hwdata)
    Product.Attr('msid_virtualization_Documentation').AssignValue(doc)
    Product.Attr('msid_virtualization_Off_Site_Config_activities').AssignValue(offdata)
    if Product.Attr('msid_virtualization_FAT').GetValue() !=fatdata:
        SetCalculatedandFinal('FAT',fatdata)
    Product.Attr('msid_virtualization_FAT').AssignValue(fatdata)
    Product.Attr('msid_virtualization_On_Site_activities').AssignValue(onsitedata)
    if Product.Attr('msid_virtualization_SAT').GetValue() != satdata:
         SetCalculatedandFinal('SAT',satdata)
    Product.Attr('msid_virtualization_SAT').AssignValue(satdata)

if 'Generic System' in SelectedProduct:
    show_column('CONT_MSID_SUBPRD','Product Name')
    show_column('CONT_MSID_SUBPRD','User_Define_Name')
else:
    hide_column('CONT_MSID_SUBPRD','Product Name')
    hide_column('CONT_MSID_SUBPRD','User_Define_Name')