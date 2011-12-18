import time
import Growl


class MyNotifier(Growl.GrowlNotifier):
   applicationName = 'Downtify'
   notifications = ['ntf1']

def gNotify(message='', action='') :
    growl = MyNotifier()
    growl.register()
    growl.notify('ntf1', message , action)
    
def main():
    growl = MyNotifier()
    growl.register()


__all__ = ['gNotify', 'main']

if __name__ == "__main__":
    main()
