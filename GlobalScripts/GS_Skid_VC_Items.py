def Skid_items(sender):
    for attr in sender.SelectedAttributes:
        for value in attr.Values:
            if  attr.Name=="Pskid FME":
                Trace.Write(str(sender.QI_FME.Value)+"-----QI_FME-----recheck---111---"+str(value.Display))
                sender.QI_FME.Value= value.Display
