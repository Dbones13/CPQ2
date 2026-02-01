import operator
cont = Product.GetContainerByName("SM_ControlGroup_Cont")
countDict = {}
for row in cont.Rows:
    countDict[row["SM_CG_Percent_Installed_Spare"]] = countDict.get(row["SM_CG_Percent_Installed_Spare"], 0) + 1
maxSpare = "0"
if len(countDict) > 0:
    maxSpare = str(max(countDict.iteritems(), key=operator.itemgetter(1))[0])
if not maxSpare:
    maxSpare = "0"
Product.Attr("doc_parameter_cg_spare_percent").AssignValue(maxSpare)