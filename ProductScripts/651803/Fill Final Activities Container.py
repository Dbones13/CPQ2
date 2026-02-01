from GS_FinalizedActivities import PopulateFinalizedActivities
if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
    try:
        PopulateFinalizedActivities(Product)
    except:
        Trace.Write("Error in script Fill Final Activities Container.")