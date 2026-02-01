Product.ParseString('[IF]([EQ](<*VALUE(Server Mounting)*>,Desk)){<*SELECTVALUE(Server Node Type_desk:SVR_STD_DELL_Tower_RAID1)*>}{if_false}[ENDIF]')
Product.Attr('PERF_ExecuteScripts').AssignValue('')