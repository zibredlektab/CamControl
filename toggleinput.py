import subprocess
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

enable = 'xinput enable 8'
disable = 'xinput disable 8'
findcmd = ['xinput', 'list-props', '8']
findstr = ''

input_active = True

findstr = subprocess.check_output(findcmd)
findstr = findstr.decode("utf-8")
index = findstr.find("Enabled")
index = findstr.find(":", index)
if (findstr[index+2] == "0"):
        input_active = False
else:
        input_active = True

print('input active? ', input_active)


if (input_active):
        subprocess.call(disable, shell=True)
        subprocess.call('python ' + dir_path + "/lockoverlay.py")
else:
        subprocess.call(enable, shell=True)
exit()