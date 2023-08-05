#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse,datetime,logging,os,threading,sys
import numpy as np
import random as rnd
import individual as ig
import coverage
import sequence as sg
import settings as sp
import reads as ngs
import readcounts as rc
import rerooter as rr
from select import select
from ngsphyexceptions import *

class NGSphy:
    """
    Class that structures the whole process flow of the NGSphy: a genome-wide
    simulation of next-generation sequencing data from genetrees and species tree
    distributions.
    ----------------------------------------------------------------------------
    Attributes:
	- appLogger: Logger object to store status of the process flow.
	- path: current working directory
	- startTime: timing when processing has started
	- endTime: timing when processing has finished
	- settingsFile: path of the settings file.

    """
    appLogger=None
    path=os.getcwd()
    startTime=None
    endTime=None
    settingsFile=""

    def __init__(self,args):
    	self.startTime=datetime.datetime.now()
    	self.appLogger=logging.getLogger("ngsphy")
    	self.appLogger.info("Starting")
    	self.settingsFile=""
    	if (args.settings):
    		self.settingsFile=os.path.abspath(args.settings)
    	else:
    		self.settingsFile=os.path.abspath(os.path.join(os.getcwd(),"settings.txt"))
        if not (os.path.exists(self.settingsFile)):
            self.endTime=datetime.datetime.now()
            message="\t{0}\n\t{1}\n\t{2}\n\t{3}\n".format(\
                "The settings file:",\
                self.settingsFile,\
                "Does not exist...",\
                "Please verify. Exiting."
            )
            raise NGSphyExitException(False,message,self.endTime)

    def run(self):
        """
        Execution of the process flow.
        It does not return values. Will exit any time a process is wrongly
        executed or conditions of execution are not satisfied.
        """
    	# checking existence of settings file
    	try:
            status=True
            message="NGSphy finished correctly."
            self.appLogger.info("Checking settings...")
            if (os.path.exists(self.settingsFile)):
                self.appLogger.debug("Starting process")
                self.appLogger.debug("Starting process")
                # settings file exist, go ahead and run
            	self.settings=sp.Settings(self.settingsFile)
            	settingsOk,settingsMessage=self.settings.checkArgs()
            	# Exit heere if not correnct parser of the settings
            	if not settingsOk: self.ending(settingsOk,settingsMessage)
            	# Generate BASIC folder structure - output folder
            	self.generateFolderStructure()

            	# Settings exist and are ok.
            	# reroot-tree
                if self.settings.inputmode == 3:
                    self.appLogger.info("Re-rooting")
                    self.rerooter=rr.Rerooter(self.settings)
                    status, message=self.rerooter.run()
                    if not status: self.ending(status,message)
                    status, message= self.rerooter.recheckPloidyAfterRerooting()
                    if not status: self.ending(status, message)
                # Generate sequences
                if self.settings.inputmode < 4:
                    self.appLogger.info("Running sequence generator")
                    self.seqGenerator=sg.SequenceGenerator(self.settings)
                    # only copying ancestral sequences if the mode needs it
                    if(self.settings.inputmode >1):
                        statusRefSeq,messageRefSeq=self.seqGenerator.copyAncestralSequenceToOutputFolder()
                        if not statusRefSeq: self.ending(statusRefSeq,messageRefSeq)
                    indelibleStatus,indelibleMessage=self.seqGenerator.run()
                    if not (indelibleStatus): self.ending(indelibleStatus, indelibleMessage)
                # Generate Individuals (plody independency)
                self.indGenerator=ig.IndividualAssignment(self.settings)
                matingOk,matingMessage=self.indGenerator.checkArgs()
                if not matingOk: self.ending(matingOk,matingMessage)
                indelsCheckOK, indelsMessage=self.indGenerator.checkFilesForIndels()
                if not indelsCheckOK: self.ending(indelsCheckOK, indelsMessage)
                self.settings.indels=self.indGenerator.indelsPresence
                self.indGenerator.iteratingOverReplicates()
                # now checking NGS MODE
                if self.settings.ngsmode>0:
                    # Have to calculate coverage
                	self.appLogger.debug("Checking for Coverage. ")
                	covGenerator=coverage.CoverageMatrixGenerator(self.settings)
                	status,message=covGenerator.calculate()
                	if not status: self.ending(status,message)
            	# After this I'll have generated the individuals and folder structure
            	if self.settings.ngsmode==1:
            		self.appLogger.info("NGS Illumina reads - ART mode")
            		self.ngs=ngs.ARTIllumina(self.settings)
            		status, message=self.ngs.run()
            		if not status: self.ending(status,message)
            		self.appLogger.info("NGS read simulation process finished.")
            	elif self.settings.ngsmode==2:
            		self.appLogger.info("Read counts mode")
            		# self.appLogger.info("NGS read simulation is not being made.")
            		# If i have read count folder structure must change - i need reference folder
            		# print("ngsphy.py - Read count")
            		if self.settings.indels:
            			self.ending(False,"{0}\n\t{1}\n\t{2}".format(\
            				"Read Counts does not support INDELs (for now)",\
            				"Check the output folder. Data has been generated.",\
            				"Exiting."\
            			) )
            		self.readcount=rc.ReadCounts(self.settings)
            		status, message=self.readcount.run()
            		if not status: self.ending(status,message)
            	else:
            		self.appLogger.info("NGS simulation is not being made.")
            else:
            	self.ending(False,"Settings file ({0}) does not exist. Exiting. ".format(self.settingsFile))
            self.ending(status,message)
    	except NGSphyException as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message="{1} | File: {2} - Line:{3}\n\t{0}".format(\
                ex.message,exc_type,\
                fname, exc_tb.tb_lineno\
            )
            raise NGSphyExitException(ex.expression,message, ex.time)

    def generateFolderStructure(self):
        """
        Generates basic folder structure for a NGSphy run.
        """
    	self.appLogger.info("Creating basic folder structure.")
    	try:
    		self.appLogger.info("Creating output folder: {0} ".format(self.settings.outputFolderPath))
    		os.makedirs(self.settings.outputFolderPath)
    	except:
    		self.appLogger.debug("Output folder ({0}) exists. ".format(self.settings.outputFolderPath))


    def generateSummaryLog(self, time):
    	filename=os.path.join(\
    		self.settings.outputFolderPath,\
    		"{0}.{1:%Y}{1:%m}{1:%d}-{1:%H}:{1:%M}:{1:%S}.summary.log".format(\
    			"NGSPHY",\
    			time\
    		)
    	)
    	with open(filename, 'w') as f:
            f.write(self.settings.formatSettingsMessage())

    def ending(self, good, message):
        """
        Handles the ending of the processes. Since there is some dependency
        between processes, this will also terminate the execution of the program
        and so, ending time must be given and also notified the status of the
        termination.
        ------------------------------------------------------------------------
        Parameters:
        - good: indicates whether the process terminated correctly.
        - message: Message indicating why process is terminated.
        Raises a NGSphyException
        """
    	self.endTime=datetime.datetime.now()
        if (os.path.exists(self.settings.outputFolderPath)):
            self.generateSummaryLog(self.endTime)
        eta=self.endTime-self.startTime
        if good:
            raise NGSphyExitException(good,message,eta)
        else:
            raise NGSphyException(good,message,eta)
    	# sys.exit()
