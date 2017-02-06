import datetime
import re

import menu
import functions

if __name__ == '__main__':
    menu = menu.Menu()
    while True:
        menu.main_nav(0)


# TO DO LIST:
    #DONE:
        #menu:
            # add entry
                # task name, number of minutes, notes
                # datetime added automatically
            # lookup previous entries
                # RECORDS CAN BE EDITED
                # RECORDS CAN BE DELETED
                # find by date
                    # choose (a)range or (b)list of all dates
                        # (a)enter range
                            # present list of entries in range
                        # (b)present list of dates that have entries
                # find by time spent

            # quit

#-----------------------------------------------------------------------------------
    #NOT DONE:
                # find by exact search
                    # enter string
                        # user enters string
                        # present list of entries containing string in task name OR notes
                # find by pattern
                    # enter regular expression
                        # user enters regular expression
                        # present list of entries matching pattern in task name OR notes
