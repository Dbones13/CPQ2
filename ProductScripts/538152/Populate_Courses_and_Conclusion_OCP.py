Course_Cont = Product.GetContainerByName("SC_WEP_Courses_OCP")
Course_Cont.Rows.Clear()
Course_List = ["EXP-01","EXP-02-AT","EXP-03","EXP-2001C3","EXP-05C3","EXP-23","EXP-25","EXP-16"]
#,"EXP-2001C3"
for i in Course_List:
    course_row = Course_Cont.AddNewRow(False)
    course_row["Course"] = i
Course_Cont.MakeAllRowsSelected()
Course_Cont.Calculate

Conclusion_Cont = Product.GetContainerByName("SC_WEP_Conclusion_OCP")
Conclusion_Cont.Rows.Clear()
Conclusion_List = ["Courses","Repeat Session","Reporting Management","Scope Based Subscription, 8X5 Support, System Access"]
for j in Conclusion_List:
    conclusion_row = Conclusion_Cont.AddNewRow(False)
    conclusion_row["Deliverables"] = j
Conclusion_Cont.Calculate