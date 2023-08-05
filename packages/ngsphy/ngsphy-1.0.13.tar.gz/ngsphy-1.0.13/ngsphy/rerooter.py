#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dendropy,logging,os,shutil,sys
import settings as sp

class Rerooter:
	"""
	Class used for the manipulation of gene trees, specifically, to handle
	the re-rooting and prunning of the given gene tree.
	----------------------------------------------------------------------------
	Attributes:
	- appLogger: logger to store status of the process flow
	- settings: Settings object withh all the program parameters
	- tree: final gene tree
	- outputFilename: filename where the new tree will be stored
	- outputFilePath: absolute path of the filename where the new tree will be stored
	"""
	# general
	appLoger=None
	settings=None
	# tree-related
	tree=None
	outputFilename="ngsphy.tree"
	outputFilePath=""

	def __init__(self, settings):
		self.appLogger=logging.getLogger("ngsphy")
		self.appLogger.debug('Rerooting')
		self.settings=settings
		self.outputFilePath=os.path.join(\
			self.settings.basepath,\
			"1",\
			self.outputFilename\
		)
		self.generateFolderStructure()

	def generateFolderStructure(self):
		"""
		Generation of basic folder structure for this process
		"""
		folder=os.path.join(self.settings.basepath,"1")
		try:
			os.makedirs(folder)
			self.appLogger.info("Generating alignments folder ({0})".format(folder))
		except:
			self.appLogger.debug("Project folder exists ({0})".format(folder))
		try:
			shutil.copyfile(self.settings.ancestralSequenceFilePath, os.path.join(folder, "ancestral.fasta"))
		except:
			self.appLogger.debug("File already exists in this location ({0})".format(os.path.join(folder, "ancestral.fasta")))


	def run(self):
		"""
		Process flow of the re-rooting and pruninc process
		"""
		self.appLogger.debug('Running rerooting')
		try:
			self.tree=dendropy.Tree.get(path=self.settings.geneTreeFile,\
			 	schema="newick",\
				rooting='force-rooted',\
				preserve_underscores=True)
		except Exception as ex:
			return False, ex
		newroot=self.tree.find_node_with_taxon_label(self.settings.anchorTipLabel)
		lennewroot=newroot.edge_length
		if newroot:
			self.tree.reroot_at_edge(newroot.edge,length1=lennewroot,length2=0, update_bipartitions=False)
			self.settings.geneTreeFile=self.outputFilePath
		else:
			return False, "{0}\n\t{1}\n\t{2}".format(\
			"Rerooting problem.",\
			"Something might be wrong with the reference label.",\
			"Please Verify. Exiting"\
			)
		self.writeTreeIntoFile()
		return True,""

	def writeTreeIntoFile(self):
		"""
		Writes into a file the resulting tree
		"""
		self.appLogger.debug("Writing tree")
		self.appLogger.debug("Writing tree")
		self.tree.write(\
			path=self.outputFilePath,\
			schema="newick",\
			suppress_rooting=True\
			)

	def recheckPloidyAfterRerooting(self):
		status=True;message=""
		try:
			self.appLogger.debug("Ploidy after reroot")
			leaves = [node for node in self.tree if node.taxon]
			# print(self.tree.print_plot())
			leaves = [node.taxon.label for node in leaves if not node.taxon.label==self.settings.anchorTipLabel]
			# print(self.tree.as_string(schema='newick'))
			labels=dict()
			for tip in leaves:
				tmp=tip.strip().split("_")
				geneFamily="{0}_{1}".format(tmp[0],tmp[1])
				try:
					f=labels[geneFamily]
					labels[geneFamily]+=1
				except:
					labels[geneFamily]=1
			fail=False
			for item in labels.keys():
				if not labels[item] % self.settings.ploidy == 0:
					fail=True
					break
			if fail:
				status=False
				return status, "\n\t{0}\n\t{1}\n\t{2}".format(\
					"Problems for the individual assignment.",\
					"Number of gene-tree tips per species is not valid for the given ploidy.",\
					"Please verify. Exiting."\
				)
		except Exception as ex:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			message="\n\t{0} {1} | {2} - File: {3} - Line:{4}\n\t{5}".format(\
			    "Rerooter: Something is wrong.",\
			    ex,exc_type,\
				fname, exc_tb.tb_lineno,\
			    "Please verify. Exiting."
			    )
			status=False
		return status, message
