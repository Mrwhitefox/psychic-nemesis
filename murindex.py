# -*- coding: utf-8 -*-
import os
import glob

class Murindex:
	
	def __init__(self, muranalyzer, filepath='output'):
		self.m = muranalyzer
		self.outpath = filepath+os.sep+self.m.owner.replace(":", "-")


	#high level function to be called for html generation.
	def run(self):
		arbolist = self.generateArbolist()
		print("Generate index pages:")
		self.html_generateIndexes(arbolist, 1)

		self.html_writeRootIndex(arbolist, self.outpath)

	#Generate a recursive structure list for the path. structure: ((current folder), [(N+1 folder struct), (N+1 folder struct), ...]
	def generateArbolist(self, curPath=None):
		if curPath is None:
			curPath = self.outpath

		return(
			(
				curPath.replace(self.outpath, ""),
				[self.generateArbolist(curPath + os.sep + dirname) for dirname in get_immediate_subdirectories(curPath)]
			)
		)


	#This will generate an index.html for all folders of the arboList
	def html_generateIndexes(self, arboList, rank):
		print('  '*rank + self.outpath + arboList[0])

		html_generateIndex(self.outpath + arboList[0])
		for folder in arboList[1]:
			self.html_generateIndexes(folder, rank+1)


	#write an index html with the list of all svg files recusively. Folders with svg inside will be a link to the folder/index.htm
	def html_writeRootIndex(self, arboList, filepath):
		string = "<html><body>"
		string += self.html_getRootList(arboList)
		string += '</body></html>'

		index = open(os.path.join(filepath, 'index.htm'), 'w')
		index.write(string)
		index.close()


	#Get the html list of files (for writeRootIndex function)
	def html_getRootList(self, arboList, result=""):
		result+="<ul>"
		svgs = getFiles(self.outpath + arboList[0], 'svg')
		htms = getFiles(self.outpath + arboList[0], 'htm')
		if svgs or htms: # there are files
			result+= "<li><a href='{0}/index.htm'>{1}</a></li>".format(arboList[0][1::], os.path.basename(arboList[0]))
			result += "<ul>"

			for svg in svgs:
				result +="<li>{0}</li>\n".format(os.path.basename(svg).replace(".svg", "")) 
			for htm in htms:
				filename = os.path.basename(htm)
				if filename != 'index.htm':
					result +="<li><a href='{0}/{1}.htm'>{1}</a></li>".format(arboList[0][1::], filename.replace(".htm", ""))

			result += "</ul>"
		else: # no files here
			result+= "<li>{0}</li>".format(os.path.basename(arboList[0]))

		if arboList[1]: #subfolders
			for folder in arboList[1]:
				result = self.html_getRootList(folder, result=result)

		result+="</ul>"
		return result


### OUTPUT HTML GENERATION
def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
			if os.path.isdir(os.path.join(a_dir, name))]


#Generate an index.html with all svg and htm files contained in this folder
def html_generateIndex(folderPath):
	svgs = getFiles(folderPath, 'svg')
	if svgs:
		index = open(os.path.join(folderPath, 'index.htm'), 'w')
		index.write('<html><body bgcolor=black text="#EEE"><table>')
		for svg in svgs:
			index.write("<figure><embed type='image/svg+xml' src='{0}' /></figure><br />\n".format(os.path.basename(svg)))

		index.write('</table></body></html>')
		index.close()


#Get all svg files inside the specified folder
def getFiles(folderPath, extension):
	if os.path.exists(folderPath) : 
		return [file for file in glob.glob( os.path.join(folderPath, '*.{0}'.format(extension)))]
	else:
		return(None)