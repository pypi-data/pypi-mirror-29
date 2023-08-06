#!/usr/bin/env python
import logging
import signal
import sys
import time
class signalhandler(object):
	def __init__(self, app):
		# handle signals from OS
		self.app = app
		signal.signal(signal.SIGINT, self.handle_sigint)
		signal.signal(signal.SIGUSR1, self.handle_sigusr1)
		signal.signal(signal.SIGUSR2, self.handle_sigusr2)
		signal.signal(signal.SIGHUP, self.handle_sighup)
	def handle_sigint(self, signal, frame):
		exit_code = 0
		try:
			self.app.logger.info("terminating on SIGINT")
			exit_code = self.app.exit()
			while not self.app.main_done:
				time.sleep(0.1)
		except (NameError, AttributeError) as e:
			self.app.logger.warning("graceful application termination unsuccessful: {}".format(e))
			exit_code = 1
		finally:
			sys.exit(exit_code)
	def handle_sigusr1(self, signal, frame):
		self.app.logger.info('Setting logging to DEBUG')
		try:
			#self.app.rootlogger.setLevel(logging.DEBUG)
			self.app.rootlogger.setLevel(0)
		except Exception as e:
			self.app.logger.error("error setting logging to debug: {}".format(e))
	def handle_sigusr2(self, signal, frame):
		self.app.logger.info('Setting logging to INFO')
		try:
			self.app.rootlogger.setLevel(logging.INFO)
		except Exception as e:
			self.app.logger.error("error setting logging to info: {}".format(e))
	def handle_sighup(self, signal, frame):
		try:
			self.app.reload()
			self.app.logger.debug('reloading application configuration')
		except (NameError, AttributeError) as e:
			self.app.logger.warning("reloading application configuration unsuccessful: {}".format(e))