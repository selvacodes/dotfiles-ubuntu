

# _______  _______  ______  _______  __        
#|       ||   _   ||   __ \|     __||  |.-----.
#|   -  _||       ||      <|__     ||  ||  _  |
#|_______||___|___||___|__||_______||__||   __|
#                                       |__|   
# SpectrumOS - Embrace the Chromatic Symphony!
# By: gibranlp <thisdoesnotwork@gibranlp.dev>
# MIT licence 
#
import os
import subprocess
import r_custom
from libqtile.lazy import lazy
# Rofi Configuration files
rofi_right = r_custom.Rofi(rofi_args=['-theme', '~/.config/rofi/right.rasi'])
rofi_network= r_custom.Rofi(rofi_args=['-theme', '~/.config/rofi/network.rasi'])
rofi_left=r_custom.Rofi(rofi_args=['-theme', '~/.config/rofi/spotlight.rasi'])

# NightLight widget
@lazy.function
def nightLight_widget(qtile):
  options = [' Night Time(3500k)', '  Neutral (6500k)', '  Cool (7500k)']
  index, key = rofi_left.select('  Night Light', options)
  if key == -1:
    rofi_left.close()
  else:
    if index == 0:
      os.system('redshift -O 3500k -r -P')
      subprocess.run(["notify-send","-a", "SpectrumOS", "Temperature Set to Night Time"])
    elif index == 1:
      os.system('redshift -x')
      subprocess.run(["notify-send","-a", "SpectrumOS", "Temperature Set to Neutral"])
    else:
      os.system('redshift -O 7500k -r -P')
      subprocess.run(["notify-send","-a", " SpectrumOS", "Temperature Set to Cool"])

# Logout widget
@lazy.function
def session_widget(qtile):
  options = ['1 Lock','2 Log Out', '3 Reboot','4 Poweroff']
  index, key = rofi_left.select('  Session', options)
  if key == -1:
    rofi_left.close()
  else:
    if index == 0:
      os.system('i3lock')
    elif index == 1:
      qtile.shutdown()
    elif index == 2:
      os.system('systemctl reboot')
    else:
      os.system('systemctl poweroff')

