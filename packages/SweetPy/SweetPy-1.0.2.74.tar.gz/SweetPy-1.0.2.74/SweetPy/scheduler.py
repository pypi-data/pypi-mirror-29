import os
import platform
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from SweetPy.func_plus import FuncHelper
from abc import abstractmethod,ABCMeta
from django.conf import settings

class Scheduler(object):
    scheduler = None
    sched = None
    tasks = None
    instances = None
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.tasks = {}
        self.instances = {}

    def register_func(self,func,year=None, month=None, day=None,
                      week=None, day_of_week=None, hour=None, minute=None,
                      second=None, start_date=None, end_date=None, timezone=None,max_instances = None):
        if start_date is None:
            pass
        if max_instances is None:
            max_instances = 1
            # start_date =   延时启动
        task = self.sched.add_job(func,'cron',max_instances=max_instances,year=year, month=month, day=day,
                      week=week, day_of_week=day_of_week, hour=hour, minute=minute,
                      second=second, start_date=start_date, end_date=end_date, timezone=timezone)
        self.tasks[func.__name__] = task

    def task_start(self):
        if self.tasks.keys():
            self.sched.start()


def register_func(func,year=None, month=None, day=None,
                      week=None, day_of_week=None, hour=None, minute=None,
                      second=None, start_date=None, end_date=None, timezone=None,max_instances = None):
    if Scheduler.scheduler is None:
        Scheduler.scheduler = Scheduler()
    scheduler = Scheduler.scheduler
    scheduler.register_func(func,year, month, day,week, day_of_week, hour, minute,
                      second, start_date, end_date, timezone,max_instances)

def scan_timed_task_dirctory():
    sysstr = platform.system()
    if sysstr.lower() == 'windows':
        dir = os.getcwd() + '\\timedtask\\'
    else:
        dir = os.getcwd() + '/timedtask/'
    if FuncHelper.check_directory_exists(dir) == False:
        return
    if hasattr(settings,'SCHEDULER_ENABLE') and (settings.SCHEDULER_ENABLE == False):
        return
    sys.path.append(dir)
    filenames = FuncHelper.get_files_name_by_path(dir)
    for _filename in filenames:
        module = __import__(_filename[:-3])
        classnames = FuncHelper.get_all_classname_by_file_path_name(dir + _filename,'ServiceBase')
        for _classname in classnames:
            instance = getattr(module, _classname)()
            instance.reg_func()
            if Scheduler.scheduler is not None:
                Scheduler.scheduler.instances[_classname] = instance
    if Scheduler.scheduler is not None:
        Scheduler.scheduler.task_start()


class ServiceBase(object, metaclass=ABCMeta):

    @abstractmethod
    def main(self):
        pass

    @abstractmethod
    def reg_func(self):
        pass
        # register_func(self.main, second='*/3')

scan_timed_task_dirctory()






