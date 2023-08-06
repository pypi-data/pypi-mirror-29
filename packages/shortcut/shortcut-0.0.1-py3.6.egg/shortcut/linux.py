import sys
import os
import stat
from .exception import *
from .shortcutter import ShortCutter
            
class ShortCutterLinux(ShortCutter):
    
    def _get_desktop_folder(self):
        return os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        
    def _get_menu_folder(self):
        return os.path.join(os.path.join(os.path.expanduser('~')), '.local', 'share', 'applications')

    def create_shortcut_file(self, target_name, target_path, shortcut_folder):
        shortcut_file_path = os.path.join(shortcut_folder, "launch_" + target_name + ".desktop")
        with open(shortcut_file_path, "w") as shortcut:
            shortcut.write("[Desktop Entry]\n")
            shortcut.write("Name={}\n".format(target_name))
            shortcut.write("Exec={}\n".format(target_path))
            shortcut.write("Terminal=true\n")
            shortcut.write("Type=Application\n")

            # make the launch file executable
            st = os.stat(shortcut_file_path)
            os.chmod(shortcut_file_path, st.st_mode | stat.S_IEXEC)
        
        return (target_name, target_path, shortcut_file_path)
           
    def _is_file_the_target(self, target, file_name, file_path):
        match = False
        if file_name == target:
            # is the file executable
            if os.access(file_path, os.X_OK):
                match = True
            else:
                match = False
        return match
