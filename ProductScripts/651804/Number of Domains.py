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