import datetime
modifieddate =datetime.datetime.now()
def check_existing(favId='', folderId=''):
	qrystr = "SELECT CpqTableEntryId from R2Q_FAVORITES(NOLOCK) where"
	if favId:
		favdata = SqlHelper.GetFirst("{} FAV_ID = '{}'".format(qrystr,favId))
		return favdata.CpqTableEntryId if favdata else None
	elif folderId:
		favdata = SqlHelper.GetList("{} FOLDER_ID = {}".format(qrystr,folderId))
		return [entry.CpqTableEntryId for entry in favdata] if favdata else None
	else:
		return None

def savefav(productName,favid):
	condition = "(SELECT MAX(Id) FROM FavoritesDefinition (nolock) WHERE CreatedByUserId = {userid} ) ".format(userid = userid) if favid == 0 or favid =='' else favid
	USER_ID = User.UserName
	Trace.Write("Save condition: "+str(condition))
	import_table_attr_grp = SqlHelper.GetTable("R2Q_FAVORITES")
	get_Fav = SqlHelper.GetFirst("""SELECT fd.Name, fd.PartNumber, fd.ProductId, fd.Description, fd.Id AS maximumId,sys_FavoriteFolder.FolderName,sys_FavoriteFolder.Id as folderId
	FROM
		FavoritesDefinition (nolock) fd
	LEFT JOIN
		sys_FavoritesInFolders (nolock)
	ON
		fd.Id = sys_FavoritesInFolders.FavoriteId
	LEFT JOIN
		sys_FavoriteFolder (nolock)
	ON
		sys_FavoritesInFolders.FavoriteFolderId = sys_FavoriteFolder.Id
	WHERE
		fd.CreatedByUserId = {userid}
	AND
		fd.Id = {condition} """.format(userid = userid,condition=condition))

	if get_Fav:
		max_id = get_Fav.maximumId
		fav_name = get_Fav.Name
		Trace.Write("fav_name: "+str(fav_name))
		row_data = {
			'PRODUCT_ID': str(get_Fav.ProductId),
			'PRODUCT_NAME': str(productName),
			'FAV_ID': str(max_id),
			'FAV_NAME': str(fav_name),
			'FAV_DESCRIPTION': str(get_Fav.Description),
			'USER_ID': str(USER_ID),
			'PART_NUMBER': str(get_Fav.PartNumber),
			'FOLDER_ID': str(get_Fav.folderId),
			'FOLDER_NAME': str(get_Fav.FolderName),
			'CpqTableEntryModifiedBy':userid,
			'CpqTableEntryDateModified':modifieddate
			}
		entryid = check_existing(favId=max_id)
		if entryid:
			row_data.update({'CpqTableEntryId': entryid})
		import_table_attr_grp.AddRow(row_data)
		SqlHelper.Upsert(import_table_attr_grp)
		Trace.Write("Fav table updated..")
	return True

def updatefolder(folderId,folderName):
	folderdata = check_existing(folderId=folderId)
	import_table_attr_grp = SqlHelper.GetTable("R2Q_FAVORITES")
	if folderdata:
		for entryid in folderdata:
			import_table_attr_grp.AddRow({
					'CpqTableEntryId': entryid,
					'FOLDER_NAME': str(folderName),
					'CpqTableEntryModifiedBy':userid,
					'CpqTableEntryDateModified':modifieddate
					})
		SqlHelper.Upsert(import_table_attr_grp)

def get_folderlist(folderid):
	folder_list = []
	while folderid:
		result = SqlHelper.GetFirst("""SELECT id,foldername FROM sys_FavoriteFolder(NOLOCK) WHERE ParentId = {}""".format(folderid))
		folder_list.append(str(folderid))
		if result:
			parent = result.id
			folderid = parent
		else:
			break
	return "(" + ",".join(folder_list) + ")"

def deletefav(favid,folderid):
	condition=''
	if favid:
		condition = "FAV_ID = '{}'".format(favid)
	elif folderid:
		folderlist = get_folderlist(folderid)
		condition = "FOLDER_ID in {}".format(folderlist)
	Trace.Write("Del condition: "+str(condition))
	if condition:
		favData = SqlHelper.GetList("select * from R2Q_FAVORITES (NOLOCK) where {}".format(condition))
		tableInfo = SqlHelper.GetTable("R2Q_FAVORITES")
		for row in favData:
			tableInfo.AddRow(row)
		SqlHelper.Delete(tableInfo)
	return True

def breadcrumb(folderid):
	breadcrumb_list = []
	breadcrumb_str = '''<li class="breadcrumb-items">
							<a href="#" onclick="ViewR2QFavorites()" class="breadcrumb-heading-tab">Favorites</a>
						</li>'''
	while folderid:
		result = SqlHelper.GetFirst("""SELECT ParentId,foldername FROM sys_FavoriteFolder WHERE id = {}""".format(folderid))
		if result:
			parent = result.ParentId
			breadcrumb_list.append('''<li class="breadcrumb-items">
							<a href="#" onclick="view_favfolder(this)" class="breadcrumb-heading-tab" id="catList'''+str(folderid)+'''">'''+str(result.foldername)+'''</a>
						</li>''')
			folderid = parent
		else:
			break
	rev_breadcrum = reversed(breadcrumb_list)
	breadcrumb_str += ''.join(rev_breadcrum)
	return breadcrumb_str

def generate_folder_table(folderid):
	folderlist = []
	condition = "sf.ParentId = {}".format(folderid) if folderid else "(sf.ParentId IS NULL OR sf.ParentId = '')"
	folderdata = SqlHelper.GetList("SELECT distinct sf.Id, sf.FolderName FROM sys_FavoriteFolder (NOLOCK) sf INNER JOIN R2Q_FAVORITES (NOLOCK) fav ON fav.FOLDER_NAME = sf.FolderName WHERE {} and fav.PART_NUMBER= '{}' and ownerid= {}".format(condition,Product.PartNumber,User.Id))
	for row in folderdata:
		folderbody = '''<div class="favorite-folders-list-container">
							<a href="#" onclick="view_favfolder(this)" id="catList'''+str(row.Id)+'''" class="folder-name focus-helper"><span class="sap-icon">&#xe1c9;</span>'''+str(row.FolderName)+'''</a>
							<span class="favorites-icon">
								<a href="#" onclick="r2q_editFolder(this)" data-target="#updateFavfolder" data-toggle="modal" id="edit-folder" class="fiori3-icon-button edit-favorites-icon" aria-label="Edit Folder" title="Edit Folder">
									<span class="sap-icon">&#xe038;</span>
								</a>
								<a href="#" onclick="r2q_removeFolder(this)" data-target="#deleteFavfolder" data-toggle="modal" class="fiori3-icon-button" id="delete-folder" aria-label="Delete Folder"  title="Delete Folder">&#xe03d;</a>
							</span>
						</div>'''
		folderdict = {"folder_name":str(folderbody)}
		folderlist.append(folderdict)
	return folderlist

def generate_fav_table(folderid):
	favdata = SqlHelper.GetList("select * from R2Q_FAVORITES (nolock) JOIN FavoritesDefinition (nolock) fd on fd.Id = FAV_ID where USER_ID = '{}' and PRODUCT_ID='{}' and FOLDER_ID = '{}'".format(username,prodId,folderid))
	get_prdtype = SqlHelper.GetFirst("select ptd.PRODUCTTYPE_NAME  from products (nolock) PRD inner join product_types_defn (nolock) ptd on ptd.PRODUCTTYPE_CD = PRD.PRODUCTTYPE_CD where PRODUCT_ID = '{}'".format(prodId))
	prdType = get_prdtype.PRODUCTTYPE_NAME if get_prdtype else ''
	table_header = '''<table data-search="true" data-pagination="true" class="fiori3-table fiori3-products-list-table" id="r2q_favorites">
		<thead>
			<tr>
				<th data-sortable="true" data-field="fav_name">Product Name</th>
				<th data-sortable="true" data-field="category">Category</th>
				<th data-sortable="true" data-field="prd_type">Type</th>
				<th data-sortable="true" data-field="prd_name">Based On Product</th>
				<th data-sortable="true" data-field="actioncol">Actions</th>
			</tr>
		</thead>
		<tbody></tbody></table>'''

	folder_header = '''<table class="fiori3-table fiori3-products-list-table" aria-label="Categories List View" id="r2q_favfolder">
		<thead>
			<tr>
				<th scope="col" data-field="folder_name">Name</th>
			</tr>
		</thead>
		<tbody></tbody></table>'''

	data_list = []
	for row in favdata:
		name_str = '''<div class="image-on-hover">
					<div>
						<a class="product-title focus-helper">'''+str(row.FAV_NAME)+'''</a>
						<span class="part-number tooltip-if-long ellipsis example" title="'''+str(row.PART_NUMBER)+'''">(<span>'''+str(row.PART_NUMBER)+'''</span>)</span>
					</div>
					<span  class="favorites-icon">
						<a href="#" onclick="r2q_editfav(this)" class="product-title edit-favorites-icon" id="editIcon'''+str(row.FAV_ID)+'''" tabindex="0" aria-label=" Msg.EditFavorite" title="Edit Favorite">
							<span class="sap-icon">&#xe038;</span>
						</a>
						<a href="#" onclick="r2q_removeFav(this)" class="product-title in-favorites" data-toggle="modal" data-target="#deleteFavpopup" id="favoriteIcon'''+str(row.FAV_ID)+'''" tabindex="0" aria-label="Delete Favorite" title="Delete Favorite">
						<span class="sap-icon">&#xe065;</span>
						</a>
					</span>
					<img class="img-thumbnail" src="" alt="">
				</div>
				<p class="description visible-lg visible-md">'''+str(row.FAV_DESCRIPTION)+'''</p>'''
		cat_str = '''<a class="category-name-cell" id="favoriteCategory'''+str(row.FAV_ID)+'''">Projects</a>'''
		type_str = '''<span>'''+str(prdType)+'''</span>'''
		prd_str = '''<span>'''+str(row.PRODUCT_NAME)+'''</span>'''
		action_str = '''<div style="display: none;">
					<div class="alert alert-warning small" style="display: none;">This product is no longer available and has been discontinued.</div>
					<div class="alert alert-warning small" style="display: none;">
						This product is no longer available and has been discontinued but here is the replacement product.
						<br>
						<a href="#" id="replacementLink'''+str(row.FAV_ID)+'''">Link to Product Replacement</a>
					</div>
				</div>
				<div>
					<div class="fiori3-input-group flex-wrap flex-end">
						<div class="config-button">
							<a href="/Configurator.aspx?favId='''+str(row.FAV_ID)+'''" onclick="r2q_configFav()" class="btn btn-secondary fiori3-btn-secondary">Configure</a>
						</div>
					</div>
				</div>'''
		data_dict = dict(zip(['fav_name','category','prd_type','prd_name','actioncol'],[str(name_str), cat_str,type_str,prd_str,str(action_str)]))
		data_list.append(data_dict)
	folderlistdata = generate_folder_table(folderid)
	breadcrumb_data = breadcrumb(folderid)

	return table_header,data_list,folder_header,folderlistdata,breadcrumb_data

userid = User.Id
username = User.UserName
prodId = Product.Id
action = Param.Action if hasattr(Param, "Action") else ""
if action == 'Save':
	favid = Param.editfavoriteId if hasattr(Param,"editfavoriteId") else ''
	productName = Param.productName if hasattr(Param,"productName") else ''
	ApiResponse = ApiResponseFactory.JsonResponse(savefav(productName,favid))
elif action == 'Delete':
	favid = Param.favId if hasattr(Param,"favId") else ''
	folderid = Param.favoritefoldId if hasattr(Param,"favoritefoldId") else ''
	ApiResponse = ApiResponseFactory.JsonResponse(deletefav(favid,folderid))
elif action == 'View':
	folderid = Param.folderid if hasattr(Param,"folderid") else ''
	ApiResponse = ApiResponseFactory.JsonResponse(generate_fav_table(folderid))
elif action == 'Update':
	folderid = Param.favoritefoldId if hasattr(Param,"favoritefoldId") else ''
	foldername = Param.favFolderName if hasattr(Param,"favFolderName") else ''
	ApiResponse = ApiResponseFactory.JsonResponse(updatefolder(folderid,foldername))