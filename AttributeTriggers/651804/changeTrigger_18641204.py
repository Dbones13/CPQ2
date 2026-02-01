from GS_PCN_Populate_Write_Ins import updateWriteIn
attr_value = Product.Attr('Number of Domains').GetValue()
if '.' in attr_value:
    result = attr_value.split('.')[0]
    Product.Attr('Number of Domains').AssignValue(str(result))

def pcn_domain_hide_show(Product):
	number_of_domains = Product.Attr('Number of Domains').GetValue()
	if number_of_domains != '':
		domain_container = Product.GetContainerByName('Domain')
		columns = ['Domain_1', 'Domain_2', 'Domain_3']
		for i, column in enumerate(columns, start=1):
			permission = 'Editable' if i <= int(number_of_domains) else 'Hidden'
			Product.ParseString('<*CTX( Container(Domain).Column({}).SetPermission({}) )*>'.format(column,permission))
			if permission == 'Hidden':
				for row in domain_container.Rows:
					col=row.Columns
					if row.RowIndex == 0:
						col[column].Value = column.split('_')[0]+' '+column.split('_')[1]
					else:
						col[column].Value = '0'


pcn_domain_hide_show(Product)

def process_input(value):
    if isinstance(value, str):
        if value.isdigit():
            return int(value)

        if value.replace('.', '', 1).isdigit():
            float_value = float(value)
            if float_value >= 0:
                return round(float_value)

    if isinstance(value, int):
        if value >= 0:
            return value

    if isinstance(value, float):
        if value >= 0:
            return round(value)

    return 0

for rows in Product.GetContainerByName('Domain').Rows:
    if rows.RowIndex != 0:
        value_1 = process_input(rows['Domain_1'])
        value_2 = process_input(rows['Domain_2'])
        value_3 = process_input(rows['Domain_3'])
        Product.GetContainerByName('Domain').Rows[rows.RowIndex]['Domain_1'] = str(int(value_1))
        Product.GetContainerByName('Domain').Rows[rows.RowIndex]['Domain_2'] = str(int(value_2))
        Product.GetContainerByName('Domain').Rows[rows.RowIndex]['Domain_3'] = str(int(value_3))


domain_container = Product.GetContainerByName('Domain')
for rows in domain_container.Rows:
	if rows['rows_name'] != 'Domain Name':
		d1 = int(rows['Domain_1']) if rows['Domain_1'] !='' else 0
		d2 = int(rows['Domain_2']) if rows['Domain_2'] !='' else 0
		d3 = int(rows['Domain_3']) if rows['Domain_3'] !='' else 0
		rows['Sum'] = str(d1+d2+d3)
domain_container.Calculate()
#updateWriteIn(Product)