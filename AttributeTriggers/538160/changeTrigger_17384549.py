con = Product.GetContainerByName('HWOS_Invalid_Model Scope_3party')
for i in con.Rows:
    i['Reason'] = 'Invalid data entered - some of the fields are empty.'
else:
    con.Calculate()