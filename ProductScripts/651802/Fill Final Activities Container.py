if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
    from GS_FinalizedActivities import PopulateFinalizedActivities
    PopulateFinalizedActivities(Product)
    Trace.Write("bhc163------>Assessments")
    Product.Attr('CyberChildFlag').AssignValue('True')