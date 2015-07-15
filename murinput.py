# -*- coding: utf-8 -*-
import os
from murfinder import *


### USER INPUT
def select_from_list(choices):
	if len(choices) == 0:
		return None

	for i, choice in enumerate(choices):
		print(i, choice)

	nb = 0-1
	while not (0 <= nb < len(choices)):
		nb = input("Please choose: ")
		nb = int(nb)
	return choices[nb]