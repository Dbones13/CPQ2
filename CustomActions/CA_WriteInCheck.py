Quote.GetCustomField('WriteinCheck').Content = ""
product = SqlHelper.GetFirst("select p.product_ID from Products p join product_versions pv on p.Product_ID = pv.Product_ID where System_ID = 'WriteIn_cpq' and pv.Is_Active = 1")
if product is not None:
    activePID = product.product_ID
UserId = Quote.UserId
CartId = Quote.QuoteId
query = ("select count(PRODUCT_ID) as x from CART_ITEM where PRODUCT_ID = {0} and USERID = {1} and CART_ID = {2}").format(activePID,UserId,CartId)
res = SqlHelper.GetFirst(query)
if res.x > 0:
    Quote.GetCustomField('WriteinCheck').Content = "1"
Quote.Save(False)