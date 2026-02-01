import operator
cont = Product.GetContainerByName("Series_C_Control_Groups_Cont")
countDict = {}
family =0
Foundation=0
Profibus=0
Ethernet=0
PMIO=C300=CN100=HIVE300=Virtual=Physical=0
fam=0
fam1=universal=0
for row in cont.Rows:
    if row["controler_required"]=='C300 CEE':
        C300 +=1
    if row["controler_required"]=='CN100 CEE':
        CN100 +=1
    if row["controler_required"]=='CN100 I/O HIVE - C300 CEE':
        HIVE300 +=1
    if row["controler_required"]=='Control HIVE - Virtual':
        Virtual +=1
    if row["controler_required"]=='Control HIVE - Physical':
        Physical +=1
    if row["Uni_marshling"]=='Yes':
        universal +=1
    if row["SerC_CG_IO_Family_Type"]=='Series C':
        fam +=1
    if row["SerC_CG_IO_Family_Type"]=='Series-C Mark II':
        fam1 +=1
    if row["SerC_CG_IO_Family_Type"]=='Turbomachinery':
        family +=1
    if row["SerC_CG_Foundation_Fieldbus_Interface_required"]=='Yes':
        Foundation +=1
    if row["SerC_GC_Profibus_Gateway_Interface"]=='Yes':
        Profibus +=1
    if row["SerC_CG_Ethernet_Interface"]=='Yes':
        Ethernet +=1
    if row["SerC_CG_PM_IO_Solution_required"]=='Yes':
        PMIO +=1
    countDict[row["SerC_CG_Percent_Installed_Spare"]] = countDict.get(row["SerC_CG_Percent_Installed_Spare"], 0) + 1
maxSpare = "0"
if len(countDict) > 0:
    maxSpare = str(max(countDict.iteritems(), key=operator.itemgetter(0))[0])
if not maxSpare:
    maxSpare = "0"
Product.Attr("doc_parameter_cg_spare_percent_for_c300").AssignValue(maxSpare)
Product.Attr("IO_Family_document").AssignValue(str(family))
Product.Attr("Foundation_Fieldbus_document").AssignValue(str(Foundation))
Product.Attr("Profibus_Gateway_Interface_document").AssignValue(str(Profibus))
Product.Attr("Ethernet_Interface_document").AssignValue(str(Ethernet))
Product.Attr("PM_IO_Solution_required_document").AssignValue(str(PMIO))
Product.Attr("C300_IO_FamilY1_for_proposal").AssignValue(str(fam))
Product.Attr("C300_IO_FamilY2_for_proposal").AssignValue(str(fam1))
Product.Attr("C300_controlerrequred300_for_proposal").AssignValue(str(C300))
Product.Attr("C300_controler_100_for_proposal").AssignValue(str(CN100))
Product.Attr("C300_100controlerrequred300_for_proposal").AssignValue(str(HIVE300))
Product.Attr("C300_Contro_vertual_for_proposal").AssignValue(str(Virtual))
Product.Attr("C300_contro_physical_for_proposal").AssignValue(str(Physical))
Product.Attr("C300_universal_marshling_for_proposal").AssignValue(str(universal))
Trace.Write(universal)