# productName=Product.Name
Products ={
"TPC Product Upload":Product.GetContainerByName("Siebel_Invalid_Parts"),
"Siebel Product Upload":Product.GetContainerByName("Siebel_Invalid_Parts"),
"Winest Labor Import":Product.GetContainerByName("Winest Invalid Labor Container")
}

headers={"TPC Product Upload":["Item Id","Part Number","Message"],"Siebel Product Upload":["Item Id","Part Number","Message"],"Winest Labor Import":["Execution Deliverable","Material Number","Area","WBS Code","Year","Calculated Hrs","Execution Country","Execution Year","Message"]}
rowData=[]
def conData(Invalid_con,rowData):
    for row in Invalid_con.Rows:
        data=[row["Item Id"],row["Part Number"],row["Message"]] if Invalid_con.Name=="Siebel_Invalid_Parts" else [row["Deliverable"],row["Material Number"],row["Area"],row["WBS Code"],row["Year"],row["Calculated Hrs"],row["Execution Country"],row["Execution Year"],row["Message"]]
        rowData.append(data)
    return rowData

productName=Product.Name
rowData.append(headers[productName])
con_data=conData(Products.get(productName),rowData)
if productName == 'TPC Product Upload':
    Product.Attr("Download_Flag").AssignValue('Downloaded')
ApiResponse = ApiResponseFactory.JsonResponse(con_data)