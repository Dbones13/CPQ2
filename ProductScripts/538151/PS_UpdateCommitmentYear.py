cont = Product.GetContainerByName("Commitment_OTU_SESP")
selectedYear = 0
for row in cont.Rows:
    if row.IsSelected:
        selectedYear = int(float(row["SESP_Commitment_OTU"].split("-")[0]))
        break

Contract = Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content
Contract_Years = "0"
if Contract is not None or Contract != "":
    Contract_Years = Contract.Split(".")[0] if Contract.Split(".")[0] else 0
year_Check = "0"
if int(Contract_Years) == 0:
        pass
elif int(Contract_Years) < 3:
    year_Check = "1"
elif int(Contract_Years) < 5:
    year_Check = "3"
else:
    year_Check = "5"

if selectedYear != int(year_Check):
    for row in cont.Rows:
        if int(row["SESP_Commitment_OTU"].split("-")[0]) == int(year_Check):
            row.IsSelected = True
        else:
            row.IsSelected = False