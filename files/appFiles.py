import sys
import os

class AppSupport:
    def __init__(self, name):
        self.app_name = name
        self.support_folder = self.get_support_folder()
        self.create_support_folder()

    def get_support_folder(self):
        if sys.platform == 'darwin':
            from AppKit import NSSearchPathForDirectoriesInDomains, NSApplicationSupportDirectory, NSUserDomainMask
            # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
            appdata = os.path.join(NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, True)[0], self.app_name)
        elif sys.platform == 'win32':
            appdata = os.path.join(os.environ['APPDATA'], self.app_name)
        else:
            appdata = os.path.expanduser(os.path.join("~", "." + self.app_name))

        return appdata

    def create_support_folder(self):
        support_folder = self.get_support_folder()
        if os.path.isdir(support_folder):
            return

        os.makedirs(support_folder)

    def write_data(self, fileName, data):
        with open(os.path.join(self.support_folder, fileName), "w") as f:
            f.write(data)

    def read_data(self, fileName):
        with open(os.path.join(self.support_folder, fileName)) as f:
            return f.read()

    def file_exists(self, fileName):
        return os.path.exists(os.path.join(self.support_folder, fileName))