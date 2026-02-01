if Product.Name != "Service Contract Products":
    if Product.Attr('SC_Product_Type').GetValue() == "New":
        Course_Cont = Product.GetContainerByName("SC_WEP_Courses_OCP")
        Conclusion_Cont = Product.GetContainerByName("SC_WEP_Conclusion_OCP")
        Course_Cont.Calculate()

        user_count = Product.Attr("SC_WEP_No_of_Users_OCP").GetValue()
        if user_count == "":
            user_count = 0.00
        elif isinstance(eval(user_count),float):
            user_count = int(float(user_count))
            Product.Attr("SC_WEP_No_of_Users_OCP").AssignValue(str(user_count))
        else:
            user_count = Product.Attr("SC_WEP_No_of_Users_OCP").GetValue()
        effort_loading = Product.Attr("SC_WEP_Effort_Loading_OCP").GetValue()
        Trace.Write(effort_loading)
        total = 0
        if Course_Cont.Rows.Count:
            for row in Course_Cont.Rows:
                row.Calculate()
                row["Hidden_UnitPrice"] = str(float(row["Unit_Price"]))
                row["List_Price"] = str(float(row["Unit_Price"])*float(user_count))
                row["Hidden_ListPrice"] = str(float(row["Unit_Price"])*float(user_count))
                Trace.Write(row["List_Price"])
                row["Effort_Loading"] = str(float(row["List_Price"])*float(effort_loading)/100)
                row["Hidden_EffortLoading"] = str(float(row["List_Price"])*float(effort_loading)/100)
                Trace.Write(row["Effort_Loading"])
                total += float(row["Effort_Loading"])
                row.Calculate()
            Course_Cont.Calculate()

        if Conclusion_Cont.Rows.Count:
            for row in Conclusion_Cont.Rows:
                if row["Deliverables"] == "Courses":
                    row["Value"] = str(total)
                    row["Hidden_Value"] = str(total)
                if row["Deliverables"] == "Repeat Session":
                    row["Value"] = str((25*total)/100)
                    row["Hidden_Value"] = str((25*total)/100)
                if row["Deliverables"] == "Reporting Management":
                    row["Value"] = str((10*total)/100)
                    row["Hidden_Value"] = str((10*total)/100)
                if row["Deliverables"] == "Scope Based Subscription, 8X5 Support, System Access":
                    row["Value"] = str((20*total)/100)
                    row["Hidden_Value"] = str((20*total)/100)
                row.Calculate()
            Conclusion_Cont.Calculate()

    if Product.Attr('SC_Product_Type').GetValue() == "Renewal" and Product.Attr('SC_Renewal_check').GetValue() == "1":
        Trace.Write('checking conditions')
        Course_Cont = Product.GetContainerByName("SC_WEP_Courses_OCP")
        Conclusion_Cont = Product.GetContainerByName("SC_WEP_Conclusion_OCP")
        Course_Cont.Calculate()

        #Current Year
        if Product.Attr('SC_ScopeRemoval').GetValue() == "Workforce Excellence Program":
            user_count = 0.00
            Product.Attr("SC_WEP_No_of_Users_OCP").AssignValue('0')
        else:
            user_count = Product.Attr("SC_WEP_No_of_Users_OCP").GetValue()
            if user_count == "":
                user_count = 0.00
            elif isinstance(eval(user_count),float):
                user_count = int(float(user_count))
                Product.Attr("SC_WEP_No_of_Users_OCP").AssignValue(str(user_count))
                Product.Attr("SC_WEP_No_of_Users_OCP_Backup").AssignValue(str(user_count))
            else:
                user_count = Product.Attr("SC_WEP_No_of_Users_OCP").GetValue()
                Product.Attr("SC_WEP_No_of_Users_OCP_Backup").AssignValue(str(user_count))
        effort_loading = Product.Attr("SC_WEP_Effort_Loading_OCP").GetValue()

        #Previous Year
        user_count_py = Product.Attr("SC_WEP_No_of_Users_OCP_PY").GetValue()
        if user_count_py == "":
            user_count_py = 0.00
        elif isinstance(eval(user_count_py),float):
            user_count_py = int(float(user_count_py))
            Product.Attr("SC_WEP_No_of_Users_OCP_PY").AssignValue(str(user_count_py))
        else:
            user_count_py = Product.Attr("SC_WEP_No_of_Users_OCP_PY").GetValue()
        effort_loading_py = Product.Attr("SC_WEP_Effort_Loading_OCP_PY").GetValue()


        total = 0
        total_py = 0
        if Course_Cont.Rows.Count:
            for row in Course_Cont.Rows:

                #Current Year
                row.Calculate()
                row["Hidden_UnitPrice"] = str(float(row["CY_UnitPrice"]))
                row["CY_ListPrice"] = str(float(row["CY_UnitPrice"])*float(user_count))
                row["Hidden_ListPrice"] = str(float(row["CY_UnitPrice"])*float(user_count))
                row["CY_EffortLoading"] = str(float(row["CY_ListPrice"])*float(effort_loading)/100)
                row["Hidden_EffortLoading"] = str(float(row["CY_ListPrice"])*float(effort_loading)/100)
                Trace.Write(row["CY_EffortLoading"])
                total += float(row["CY_EffortLoading"])

                #Previous Year
                row["PY_ListPrice"] = str(float(row["PY_UnitPrice"])*float(user_count_py)) if row["PY_UnitPrice"] != "" else '0'
                row["PY_EffortLoading"] = str(float(row["PY_ListPrice"])*float(effort_loading_py)/100)
                total_py += float(row["PY_EffortLoading"])

                row.Calculate()
            Course_Cont.Calculate()

        if Conclusion_Cont.Rows.Count:
            for row in Conclusion_Cont.Rows:

                #Current Year
                if row["Deliverables"] == "Courses":
                    row["CY_Value"] = str(total)
                    row["Hidden_Value"] = str(total)
                if row["Deliverables"] == "Repeat Session":
                    row["CY_Value"] = str((25*total)/100)
                    row["Hidden_Value"] = str((25*total)/100)
                if row["Deliverables"] == "Reporting Management":
                    row["CY_Value"] = str((10*total)/100)
                    row["Hidden_Value"] = str((10*total)/100)
                if row["Deliverables"] == "Scope Based Subscription, 8X5 Support, System Access":
                    row["CY_Value"] = str((20*total)/100)
                    row["Hidden_Value"] = str((20*total)/100)

                #Previous Year
                if row["Deliverables"] == "Courses":
                    row["PY_Value"] = str(total_py)
                if row["Deliverables"] == "Repeat Session":
                    row["PY_Value"] = str((25*total_py)/100)
                if row["Deliverables"] == "Reporting Management":
                    row["PY_Value"] = str((10*total_py)/100)
                if row["Deliverables"] == "Scope Based Subscription, 8X5 Support, System Access":
                    row["PY_Value"] = str((20*total_py)/100)

                row.Calculate()
            Conclusion_Cont.Calculate()