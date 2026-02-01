def sortRow(cont,rank,new_row_index):
    try:
        sort_needed = True
        if new_row_index == 0:
            return
        while sort_needed == True:
            if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
                cont.MoveRowUp(new_row_index, False)
                new_row_index -= 1
            else:
                sort_needed = False
    except Exception,e:
        Log.Info(str(e)+ ' '+ str(rank)+ ' '+ str(new_row_index))