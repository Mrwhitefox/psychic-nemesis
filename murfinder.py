# -*- coding: utf-8 -*-
import os
import os.path
import glob
from murinput import *

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_default_db_dir():
	return os.path.join( os.getenv('APPDATA') , 'skype')


def get_available_dbs():
	if os.path.exists(get_default_db_dir()) :	
		return [file for file in glob.glob( os.path.join(get_default_db_dir(), '*', 'main.db'))]
	else:
		print("Nothing found. Specify manually a database.")
		return(None)


def choose_one_db():
	return select_from_list(get_available_dbs())