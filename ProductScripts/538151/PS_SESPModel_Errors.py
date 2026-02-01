sespCont = Product.GetContainerByName("SC_Models_Scope")
err_msg = ""
err_msg_2 = ""
msidsesp = {}

if sespCont.Rows.Count > 0:
    for row in sespCont.Rows:
        sespquery = SqlHelper.GetFirst("select PartNumber from SC_PRICING_SESP where PartNumber='{}'".format(row["SESP_Models"]))
        if sespquery is None:
            err_msg += "SESP Model is invalid on row:" + str(row.RowIndex+1) + "<br>"

        if row["MSIDs"] not in msidsesp.keys():
            msidsesp[row["MSIDs"]] = [row["SESP_Models"]]
        else:
            if row["SESP_Models"] in msidsesp[row["MSIDs"]] and sespquery is not None:
                err_msg_2 += "Combination of MSID and SESP Model on row: " + str(row.RowIndex+1) +  " already exist in the table" + "<br>"
            else:
                msidsesp[row["MSIDs"]].append(row["SESP_Models"])

ErrorMsg = err_msg+err_msg_2
Product.Attr("Error_Message").AssignValue(ErrorMsg)