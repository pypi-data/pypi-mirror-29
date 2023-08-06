#!/usr/bin/env python
from signalhandler import signalhandler
import time, sys, logging, logging.handlers, os, daemon, daemon.pidfile, lockfile, signal, argparse
import __main__
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)
class linux_daemon(object):
	def __init__(self):
		#logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s')
		self.rootlogger = logging.getLogger()
		self.rootlogger.setLevel(logging.INFO)
		self.pid = os.getpid()
		self.caller = os.path.abspath(__main__.__file__)
		self.dir = os.path.dirname(self.caller)
		self.file = os.path.basename(self.caller)
		self.handle_arguments()
		# create dir if it does not exist?

		self.logfile_name = "{}/log/{}.log".format(self.dir, self.name)
		self.stdout = "{}/log/{}.stdout".format(self.dir, self.name)
		self.stderr = "{}/log/{}.stderr".format(self.dir, self.name)
		self.formatter = logging.Formatter('%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s')
		self.handler = logging.handlers.RotatingFileHandler(self.logfile_name, maxBytes = 1000000, backupCount = 5)
		self.handler.setFormatter(self.formatter)
		self.rootlogger.addHandler(self.handler)
		self.logger = logging.getLogger(self.name)
		#self.logger.setLevel(logging.NOTSET)
		self.uid = os.geteuid()
		self.gid = os.getgid()
		self.pidfile_name =  "{}/run/{}.pid".format(self.dir, self.name)
		self.pidfile = daemon.pidfile.TimeoutPIDLockFile(self.pidfile_name)
		try:
			self.pidfile.acquire(timeout = -1)
			self.pidfile.release()
			I_can_become_daemon = True
		except lockfile.AlreadyLocked:
			existing_pid = self.pidfile.read_pid()
			if existing_pid != self.pid:
				try:
					os.kill(existing_pid, 0)
					I_can_become_daemon = False
				except OSError:  #No process with locked PID
					self.logger.info("removing stale pid file")
					self.pidfile.break_lock()
					I_can_become_daemon = True
		if self.args['action'] == 'status':
			if I_can_become_daemon:
				status = "not running"
			else:
				status = "running with pid {}".format(existing_pid)
			print("{} is {}".format(self.name, status))
			sys.exit(0)
		elif self.args['action'] == 'start':
			if I_can_become_daemon:
				print("{} starting".format(self.name))
			else:
				print("{} is already running with pid {}".format(self.name, existing_pid))
				sys.exit(1)
		elif self.args['action'] == 'stop':
			if I_can_become_daemon:
				print("{} is not running".format(self.name))
				sys.exit(4)
			else:
				try:
					os.kill(existing_pid, signal.SIGTERM)
					print("{} with pid {} is stopping".format(self.name, existing_pid))
					sys.exit(0)
				except OSError as e:
					print("could not stop {}, cause {}".format(self.name, e))
					sys.exit(3)
		elif self.args['action'] == 'restart':
			if I_can_become_daemon:
				prefix = ''
			else:
				try:
					os.kill(existing_pid, signal.SIGTERM)
				except OSError as e:
					print("could not stop {}, cause {}".format(self.name, e))
					sys.exit(3)
				try:
					timeout = time.time() + 5
					while timeout >= time.time():
						# wait until process no longer exists
						os.kill(existing_pid, 0)
					print("timeout waiting for daemon with pid {} to stop".format(existing_pid))
					sys.exit(3)
				except OSError:
					prefix = 're'
			print("{} {}starting".format(self.name, prefix))
		elif self.args['action'] == 'reload':
			if I_can_become_daemon:
				print("{} is not running".format(self.name))
				sys.exit(4)
			else:
				os.kill(existing_pid, signal.SIGHUP)
				sys.exit(0)
		else:
			# this should not happen because argparse should catch this
			print("command {} is not recognised".format(self.args['action']))
			sys.exit(2)
		# catch OS signals
		self.signal_map = {
			signal.SIGHUP: self.handle_signal,
			signal.SIGTERM: self.handle_signal,
			signal.SIGUSR1: self.handle_signal,
			signal.SIGUSR2: self.handle_signal
		}
		self.signalhandler = signalhandler(self)
	def handle_arguments(self):
		default_configfile = 'conf/{}.ini'.format(self.file.split(".")[0])
		self.parser = argparse.ArgumentParser(description = "{}: {}".format(self.name, self.description), formatter_class = SmartFormatter)
		self.parser.add_argument('action', choices = ('start', 'stop', 'restart', 'reload', 'status'), help = 'R|controls the daemon; valid commands are:\nstart, stop, restart, reload, status', default = 'status', metavar = 'action')
		self.parser.add_argument('-c', metavar = 'configfile', default=default_configfile, help = "R|configuration file, defaults to \n'{}'".format(default_configfile))
		# let subclass set optional extra options
		self.add_arguments()
		args = self.parser.parse_args()
		self.args = vars(args)
		# let subclass use optional extra options
		self.use_arguments()
	def add_arguments(self):
		# to be overridden in actual daemon
		pass
	def use_arguments(self):
		# to be overridden in actual daemon
		pass
	def handle_signal(self, signal_in, frame):
		if signal_in == signal.SIGUSR1:
			self.logger.setLevel(logging.DEBUG)
			self.logger.info("setting level to DEBUG")
		elif signal_in == signal.SIGUSR2:
			self.logger.setLevel(logging.INFO)
			self.logger.info("setting level to INFO")
		elif signal_in == signal.SIGHUP:
			self.reload()
		elif signal_in == signal.SIGTERM:
			self.exit()
		else:
			# this shouldn't happen if we didn't subscribe to this signal
			self.logger.warning("unknown signal ({}) received".format(signal_in))
	def reload(self):
		# to be overridden in actual daemon
		pass
	def exit(self, exit_code = 0):
		self.logger.debug("pid {} exiting (code {})".format(self.pid, exit_code))
		sys.exit(exit_code)
	def run(self):
		#self.logger.debug("run {} with pid {}".format(self.caller, self.pid))
		with daemon.DaemonContext(stdout = open(self.stdout, 'a+'),
						stderr = open(self.stderr, 'a+'),
						working_directory = self.dir,
						pidfile = self.pidfile,
						files_preserve = [self.handler.stream],
						signal_map = self.signal_map,
						uid = self.uid,
						gid = self.gid
						):
			# get pid of new context
			newpid = os.getpid()
			self.logger.debug("spawning {} (file {}) function main() with pid {} (from pid {})".format(self.name, self.caller, newpid, self.pid))
			self.pid = newpid
			self.main()
	def main(self):
		# to be overridden in actual daemon
		self.logger.debug("start {} with pid {}".format(self.caller, self.pid))
		pass

if __name__ == '__main__':
	print("module linux_daemon is meant to be subclassed")
