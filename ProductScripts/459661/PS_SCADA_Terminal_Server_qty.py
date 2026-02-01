tsqadd=0
SoftR=0
for row in Product.GetContainerByName("CE_System_Cont").Rows:
    y=row.Product
    if y.Name=="3rd Party Devices/Systems Interface (SCADA)":
        for row2 in y.GetContainerByName("Scada_CCR_Unit_Cont").Rows:
            z=row2.Product
            zcon=z.GetContainerByName("Additional Hardware")
            for rowx in zcon.Rows:
                if rowx.GetColumnByName("Third_Party_Devices_Systems_Interface_SCADA").Value=="Terminal Server (0-50)":
                    tsq=rowx.GetColumnByName("Quantity").Value
                    if tsq=="":
                        tsq=0
                    tsqadd=tsqadd+int(tsq)
                    Trace.Write(tsqadd)
for row in Product.GetContainerByName("CE_System_Cont").Rows:
    y2=row.Product
    if y2.Name=="Experion Enterprise System":
        y2.Attributes.GetByName('EXP Terminal Server').AssignValue(str(tsqadd))
        SoftR=y2.Attributes.GetByName('Experion Software Release').SelectedValue.Display
        Trace.Write("SoftR: "+str(SoftR))
for row in Product.GetContainerByName("CE_System_Cont").Rows:
    y3=row.Product
    if y3.Name=="Safety Manager ESD" or y3.Name=="Safety Manager BMS" or y3.Name=="Safety Manager FGS" or y3.Name=="Safety Manager HIPPS":
        y3.Attributes.GetByName('Experion Software Release').AssignValue(str(SoftR))