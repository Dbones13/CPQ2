#Attribute 'CE PMD GES%' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

try:
    gesLocation = Product.GetContainerByName('PMD_Labour_Details').Rows[0].GetColumnByName('PMD_Ges_Location').Value
except:
    gesLocation = "None"
deliverables = ['PMD Engineering Plan', 'PMD Procure Materials & Services', 'PMD Customer Training', 'PMD Project Close Out Report']
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('PMD Engineering Labor Container').Rows
    gesPerc = TagParserProduct.ParseString('<* Value(CE PMD GES Engineer %) *>')
    for row in laborRows:
        if row.IsSelected and row['Deliverable'] not in deliverables:
            row.GetColumnByName('GES Eng % Split').Value = gesPerc