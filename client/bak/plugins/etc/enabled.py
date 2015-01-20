from service import *

a = MonitorBase()
# print a.interval

enabled_services = {
  'service': (
      ('upCheck', upCheckMonitor()),
      ('memory', memoryMonitor())
  )
}



