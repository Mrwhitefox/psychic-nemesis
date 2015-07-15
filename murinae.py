# -*- coding: utf-8 -*-
import os
import operator
import sys

from murfinder import *
from murinput import *
from muranalysis import *
from murindex import *


print ("Hello world")


db_path = choose_one_db()
#db_path = "path_to_specific_path.db"



t = Mursqlite(dbPath=db_path)

mura = Muranalyzer(t)


mura.an_contacts()

mura.an_activity_by()
mura.an_interactions_contact()
mura.an_detail_top(20)

mura.an_rx_tx_top()

mura.an_correlations()


htmlout = Murindex(mura)
htmlout.run()



sys.exit(0)