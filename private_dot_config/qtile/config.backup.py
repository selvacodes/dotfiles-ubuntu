from libqtile import hook, layout, bar, widget
from libqtile.config import Screen, Group, Key, Match
from libqtile import qtile

mod = "mod4"  # Sets mod to the Windows key
keys = [
    Key([mod], "Return", lazy.spawn("ghostty")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
]

groups = [Group(i) for i in "123456"]

for i in groups:
    keys.append(Key([mod], i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([mod, "shift"], i.name, lazy.window.togroup(i.name)))

layouts = [
    layout.Max(),
    layout.Tile(),
]

screens = [
    Screen(top=bar.Bar([widget.GroupBox(), widget.Prompt(), widget.WindowName(), widget.Clock(format='%Y-%m-%d %H:%M:%S')], 24)),
]

@hook.subscribe.startup_once
def autostart():
    qtile.cmd_spawn("nm-applet")

if __name__ in ["config", "__main__"]:
    from libqtile import manager
    manager.run()

