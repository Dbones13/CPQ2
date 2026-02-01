def getInt(Var):
    if Var:
        return int(Var)
    return 0

def calc640(qty3U, qty2U, qty1U, r640):
    check = 40 - 2*r640
    qty3U += (check/3)

    if check % 3 == 2:
        qty2U += 1
    elif check % 3 == 1:
         qty1U += 1

    return qty3U, qty2U, qty1U

platform = Product.Attr("Virtualization_Platform_Options").GetValue()
limit ,qty3U, qty2U, qty1U, cabinet = 0,0,0,0,0
if platform == "Essentials Platforms-Dell Servers":
    #Trace.Write("Inside if")
    hostSwitch = Product.Attr("Virtualization_for_Hosts_and_Switches").GetValue()
    if hostSwitch == "Yes":

        cabinetDepth = Product.Attr("Virtualization_Cabinet_Depth_Size").GetValue()
        r640 = getInt(Product.Attr("Virtualization_Number_of_R640XL_Management_Servers").GetValue()) + getInt(Product.Attr("Virtualization_Number_of_R640XL_Standard_Servers").GetValue())
        r740 = getInt(Product.Attr("Virtualization_Number_R740XL_Performance_A_Servers").GetValue()) + getInt(Product.Attr("Virtualization_Number_R740XL_Performance_B_Servers").GetValue())

        if cabinetDepth == "1 meter" and (r640+r740) > 0:
            if (r640 > 0):
                if(r640 % 8 != 0):
                    limit = 17 - 2*(r640 % 8)

                while(r640 > 0):
                    if r640 > 7:
                        r640 -= 8
                        qty3U, qty2U, qty1U = calc640(qty3U, qty2U, qty1U, 8)
                        cabinet += 1

                    else:
                        qty3U, qty2U, qty1U = calc640(qty3U, qty2U, qty1U, r640)
                        r640 = 0
                        cabinet += 1

            if (r740 > 0):
                if limit != 0:
                    if r740 > (limit/3):
                        r740 -= (limit/3)
                        qty3U -= (limit/3)
                        qty1U += (limit/3)
                    else:
                        qty3U -= r740
                        qty1U += r740
                        r740 = 0

                while(r740 > 0):
                    if r740 > 4:
                        r740 -= 5
                        qty3U += 8
                        qty1U += 6
                        cabinet += 1

                    else:
                        qty3U += (13 -r740)
                        qty1U += (r740 + 1)
                        r740 = 0
                        cabinet += 1

if getInt(Product.Attr('Vrtualization_3U').GetValue()) != qty3U or Product.Attr('Vrtualization_3U').GetValue() == '':
    Product.Attr('Vrtualization_3U').AssignValue(str(qty3U))
if getInt(Product.Attr('Vrtualization_2U').GetValue()) != qty2U or Product.Attr('Vrtualization_2U').GetValue() == '':
    Product.Attr('Vrtualization_2U').AssignValue(str(qty2U))
if getInt(Product.Attr('Vrtualization_1U').GetValue()) != qty1U or Product.Attr('Vrtualization_1U').GetValue() == '':
    Product.Attr('Vrtualization_1U').AssignValue(str(qty1U))
if getInt(Product.Attr('Virtualization_Cabinet').GetValue()) != cabinet or Product.Attr('Virtualization_Cabinet').GetValue() == '':
    Product.Attr('Virtualization_Cabinet').AssignValue(str(cabinet))
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
Product.ApplyRules()