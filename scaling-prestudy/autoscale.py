#!/usr/bin/env python3

JOBS = 10
EMULATION = True
ALLCORES = False

import queue
import threading
import time
import os

jobsqueue = {}
jobsscheduled = {}
jobstmp = {}

def threadhandler(stage, verbose):
	project = "vim-8.0.0197"

	job = jobsscheduled[stage].get()
	jobstmp[stage].put(job)
	if verbose:
		print("handle job", job, "at stage", stage)
	jobproject = "{}.{}".format(project, job)
	if stage == "configure":
		if EMULATION:
			os.system("cd test && rm -rf {} && cp -r {} {} && cd {} && ./configure".format(jobproject, project, jobproject, jobproject))
		else:
			time.sleep(8)
	elif stage == "make":
		if EMULATION:
			if ALLCORES:
				os.system("cd test/{} && make -j5".format(jobproject))
			else:
				os.system("cd test/{} && make".format(jobproject))
		else:
			time.sleep(30)
	if verbose:
		print("finish job", job)
	throwaway = jobstmp[stage].get()
	newstage = None
	if stage == "configure":
		newstage = "make"
	if newstage:
		jobsqueue[newstage].put(job)

def handle(stage, verbose):
	t = threading.Thread(target=threadhandler, args=(stage, verbose))
	t.setDaemon(True)
	t.start()

def allempty(queues):
	for queue in queues:
		if queue.qsize() > 0:
			return False
	return True

def runpipeline(numjobs, maxconf, maxmake, verbose):
	stages = ("configure", "make")
	jobsqueue.clear()
	jobsscheduled.clear()
	jobstmp.clear()
	for stage in stages:
		jobsqueue[stage] = queue.Queue()
		jobsscheduled[stage] = queue.Queue()
		jobstmp[stage] = queue.Queue()

	maxselected = {}
	maxselected["configure"] = maxconf
	maxselected["make"] = maxmake

	for i in range(numjobs):
		jobsqueue["configure"].put(i)

	if verbose:
		print("starting with queue size", jobsqueue["configure"].qsize())

	while not allempty(list(jobsqueue.values()) + list(jobsscheduled.values()) + list(jobstmp.values())):
		for stage in stages:
			if (jobsscheduled[stage].qsize() + jobstmp[stage].qsize()) < maxselected[stage] and jobsqueue[stage].qsize() > 0:
				job = jobsqueue[stage].get()
				jobsscheduled[stage].put(job)
				if verbose:
					print("pick", job, "for stage", stage)
				handle(stage, verbose)
		time.sleep(0.1)

	if verbose:
		print("finish")

f = open("autoscale.emulation={}.allcores={}.csv".format(EMULATION, ALLCORES), "w")
print("#maxconf,makemake,duration,utility", file=f)
for maxconf in range(1, JOBS):
	for maxmake in range(1, JOBS):
		#if maxconf < 5 or (maxconf == 5 and maxmake < 6):
		#	continue
		s_time = time.time()
		runpipeline(JOBS, maxconf, maxmake, False)
		d_time = time.time() - s_time
		factor = 100.0
		utility = factor / ((maxconf + maxmake) * d_time)
		print("{},{},{},{}".format(maxconf, maxmake, d_time, utility), file=f)
		f.flush()
