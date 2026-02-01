x="No"
for row in Product.GetContainerByName("Experion_Enterprise_Cont").Rows:
    y=row.Product
    x=y.Attr('EBR_Server_Check').GetValue()
    Product.Attr('EBR_Server_Check').AssignValue(str(x))
    if str(x).lower() == 'yes':
        break
r2qprd= Product.Attr("Experion_R2Q_flag").GetValue()
if r2qprd != 'R2q_product':
    thin_qty = 0
    grp = Product.GetContainerByName("Experion_Enterprise_Cont").Rows
    for row in grp:
        rps_type = row.Product.Attr("CMS Remote Peripheral Solution Type RPS").GetValue()
        DMS_type = row.Product.Attr("DMS Remote Peripheral Solution Type RPS").GetValue()
        lis = []
        if rps_type in ("Pepperl+Fuchs BTC12","Pepperl+Fuchs BTC14"):
            lis = ["CMS Flex Station Qty 0_60", "CMS Console Station Qty 0_20", "CMS Console Station Extension Qty 0_15"]
        if DMS_type in ("Pepperl+Fuchs BTC12","Pepperl+Fuchs BTC14"):
            lis.extend(["DMS Flex Station Qty 0_60", "DMS Console Station Qty 0_20", "DMS Console Station Extension Qty 0_15"])
        for data in lis:
            thin_qty += int(row.Product.Attr(data).GetValue()) if row.Product.Attr(data).GetValue() else 0
    thin_qty = str(thin_qty)
    Product.Attr("Experion_sys_No_of_Thin_clients").AssignValue(str(thin_qty))
def setzero_if_null(check_null):
    for field in check_null:
        val = Product.Attr(field).GetValue()
        if val is None or val == '':
            Product.Attr(field).AssignValue('0')
check_null = ['No of Domain Controller','No of OPC Server','No of EMDB Servers','No of Firewall, Routers, Simulators, TOR','No of Data highway','Experion_sys_No_of_Thin_clients']
setzero_if_null(check_null)