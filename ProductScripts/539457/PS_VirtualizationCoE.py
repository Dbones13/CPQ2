def getfloat(val):
    if val:
        try:
            return float(val)
        except:
            return 0
    return 0

if Product.Name == "Virtualization System":
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':
        laborCont = Product.GetContainerByName('Virtualization_Labor_Deliverable')
        hrs = 0
        cal_hrs = 0
        for row in laborCont.Rows:
            if row["Deliverable"] not in ["Documentation","Virtualization CoE"]:
                hrs += getfloat(row["Final Hrs"])
                cal_hrs += round(getfloat(row["Final Hrs"]))

        for row in laborCont.Rows:
            if row["Deliverable"] == "Virtualization CoE":
                row["Final Hrs"] = str(int(round(getfloat(hrs * 0.10))))
                row["Calculated Hrs"] = str(cal_hrs * 0.10)
        laborCont.Calculate()

partsummary_cont = Product.GetContainerByName('Virtualization_partsummary_cont')
Product.Attr('VitrualizationBomPartsQty1').AssignValue('0')
Product.Attr('VitrualizationBomPartsQty2').AssignValue('0')
Product.Attr('VitrualizationBomPartsQty3').AssignValue('0')
Product.Attr('VitrualizationPartsMonitorQty').AssignValue('0')
for row in partsummary_cont.Rows:
	if row['partnumber'] == 'MZ-PCWS15':
		Product.Attr('VitrualizationBomPartsQty1').AssignValue(str(row['CE_Final_Quantity']))
	elif row['partnumber'] == 'MZ-PCSR01':
		Product.Attr('VitrualizationBomPartsQty2').AssignValue(str(row['CE_Final_Quantity']))
	elif row['partnumber'] == 'MP-C1MCB1-100':
		Product.Attr('VitrualizationBomPartsQty3').AssignValue(str(row['CE_Final_Quantity']))
	elif row['partnumber'] == 'TP-FPW231':
		Product.Attr('VitrualizationPartsMonitorQty').AssignValue(str(row['CE_Final_Quantity']))