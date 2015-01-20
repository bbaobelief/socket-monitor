from services import linux
class BaseTemplate:
	name = None
	groups = []
	hosts = [] 
	
	service_dic = {}


class LinuxGenericServices(BaseTemplate):
	name = 'Linux Generic services'
	groups = ['BJ', 'HK']
	hosts = ['xiaojian']

	service_dic = {
		'cpu': linux.cpu(),
	     'memory': linux.memory(),
	       'upCheck': linux.upCheck()
	}


class WindowsGenericServices(BaseTemplate):
        name = 'Windows Generic services'
        groups = [ 'HK']

        service_dic = {
                'cpu': linux.cpu(),
               'upCheck': linux.upCheck()
        }


enabled_templates = (
	LinuxGenericServices(),
	WindowsGenericServices(),
)
