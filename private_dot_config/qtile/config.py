# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import functions
import os
import subprocess
import colors
from libqtile import bar,  hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen , ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.extension import WindowList,Dmenu
from qtile_extras import widget
from tabbed import Tabbed

mod = "mod4"
mod2 = "control"       # Sets mod key to SUPER/WINDOWS
myTerm = "ghostty"      # My terminal of choice
myBrowser = "google-chrome"       # My browser of choice
# myEmacs = "emacsclient -c -a 'emacs' " # The space at the end is IMPORTANT!

# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()
@lazy.layout.function
def increase_space(layout):
    # subprocess.run(["notify-send","-a", " SpectrumOS", layout.name])
    layout.increase_ratio().when(layout=["treetab"])

@lazy.layout.function
def decrease_space(layout):
    # subprocess.run(["notify-send","-a", " SpectrumOS", layout.name])
    layout.decrease_ratio().when(layout=["treetab"])

# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'monadtall':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'monadtall'
keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "w", lazy.spawn("rofi -show window -theme ~/.config/rofi/spotlight.rasi"), desc='Run Launcher'),
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "shift"], "q", lazy.spawn("dm-logout -r"), desc="Logout menu"),
    Key([mod], "r", functions.nightLight_widget, desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc='Run Launcher'),

    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "space", lazy.spawn("rofi-copyq"), desc="copyq"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section, desc='Prompt to add new section in treetab'),

    # Grow/shrink windows left/right.
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.run_extension(WindowList(
        all_groups = True,
        # dmenu_bottom = True,
    )), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", maximize_by_switching_layout, lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod, "shift"], "m", minimize_all, desc="Toggle hide/show all windows on current group"),
    Key([mod, "shift"], "e", functions.session_widget, desc="Toggle hide/show all windows on current group"),
    KeyChord([mod], "z", [
        Key([], "g", lazy.layout.grow()),
        Key([], "s", lazy.layout.shrink()),
        Key([], "n", lazy.layout.normalize()),
        Key([], "m", lazy.layout.maximize())],
        mode=True,
        name="Windows"
    ),
    KeyChord([mod], "y", [
        Key([], "g", increase_space),
        Key([], "m", decrease_space),
        Key([], "j", lazy.layout.section_down()),
        Key([], "k", lazy.layout.section_up()),
    ],
        mode=True,
        name="Layouts"
    )
]

groups = []
group_names = ["1", "2", "3", "4", "5"]
group_labels = ["1", "2", "3", "4", "5"]

group_layouts = ["max", "tabbed", "tabbed", "tabbed", "tabbed"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
            Key([],'F12',lazy.group["scratchpad"].dropdown_toggle("ghostty"))
        ]
    )


groups.append(ScratchPad('scratchpad',[
            DropDown('alacritty', 'alacritty', width=0.4, height=0.6, x=0.3, y=0.2, opacity=1),
        ]),
    )
groups.append(ScratchPad('scratchpad2',[
            DropDown('copyq', 'copyq', width=0.4, height=0.6, x=0.3, y=0.2, opacity=1),
        ]),
    )

# SCRATCH PAD KEYBINDINGS
scratch_keys = [
    KeyChord([mod], "p", [
        Key([], "t", lazy.group["scratchpad"].dropdown_toggle("ghostty")),
        Key([], "c", lazy.group["scratchpad2"].dropdown_toggle("copyq"))
    ]),
    KeyChord([mod], "s", [
        Key([], "1", lazy.group["scratchpad"].dropdown_toggle("copyq"))
    ])]
keys.extend(scratch_keys)

colors = colors.Nord

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[8],
                "border_normal": colors[0]
                }

layouts = [
    # layout.MonadWide(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme)
    # layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Stack(**layout_theme, num_stacks=2),
    # layout.Columns(**layout_theme),
    # layout.TreeTab(
    #     font = "Ubuntu Bold",
    #     fontsize = 8,
    #     border_width = 0,
    #     bg_color = colors[0],
    #     active_bg = colors[8],
    #     active_fg = colors[2],
    #     inactive_bg = colors[1],
    #     inactive_fg = colors[0],
    #     padding_left = 8,
    #     padding_x = 8,
    #     padding_y = 6,
    #     sections = ["ONE", "TWO", "THREE"],
    #     section_fontsize = 2,
    #     section_fg = colors[7],
    #     section_top = 15,
    #     section_bottom = 15,
    #     level_shift = 8,
    #     vspace = 3,
    #     panel_width = 50,
    #     place_right = True,
    #     ),
        Tabbed(
        border_width = 2,
        border_focus = colors[8],
        border_normal = colors[0],
        margin = 2,
        bg_color = colors[0],
        active_fg = colors[2],
        active_bg = colors[8],
        urgent_fg = colors[2],
        urgent_bg = colors[8],
        inactive_fg = colors[1],
        inactive_bg = colors[0],
        rounded_tabs = True,
        padding_y = 2,
        hspace = 2,
        font = "Ubuntu Bold",
        fontsize = 10,
        fontshadow = None,
        bar_height = 15 ,
        place_bottom = True,
        show_single_tab = False,
        ),
        layout.Max(**layout_theme),
        layout.MonadTall(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 12,
    padding = 0,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Spacer(length = 12),
        widget.Prompt(),
        widget.GroupBox(
                 fontsize = 12,
                 margin_y = 5,
                 margin_x = 8,
                 padding_y = 0,
                 padding_x = 1,
                 borderwidth = 3,
                 active = colors[8],
                 inactive = colors[9],
                 rounded = True,
                 highlight_color = colors[2],
                 highlight_method = "line",
                 this_current_screen_border = colors[7],
                 this_screen_border = colors [4],
                 other_current_screen_border = colors[7],
                 other_screen_border = colors[4],
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[9],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.CurrentLayout(
                 foreground = colors[1],
                 padding = 5
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[9],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.Spacer(length = 12),
        widget.WindowName(
                 foreground = colors[6],
                 padding = 4,
                 max_chars = 40
                 ),
        widget.Spacer(length = 8),
        # widget.TaskList(
        #          foreground = colors[7],
        #          icon_size = 0,
        #          border_width = 0,
        #          rounded = True,
        #          markup_focused = "<span foreground='white' underline='low'>{}</span>",
        #          max_title_width = 200,
        #          spacing = 20,
        #          highlight_method = None,
        #          # window_name_location = True,
        #          # stretch = True,
        #          ),
        widget.Spacer(length = 2),
        widget.CPU(
                 format ='💻 : {load_percent}%',
                 foreground = colors[4],
                 padding = 6,
                 ),
        widget.Memory(
                 foreground = colors[8],
                 padding = 6,
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                 format = '{MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}',
                 measure_mem ='G',
                 fmt = '🐏: {}',
                 ),
        widget.DF(
                 update_interval = 60,
                 foreground = colors[5],
                 padding = 6,
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e df')},
                 partition = '/',
                 format = '{r:.0f}%',
                 # format = '{uf}{m} free',
                 fmt = '🖴 : {}',
                 visible_on_warn = False,
                 ),
        widget.Volume(
                 foreground = colors[7],
                 padding = 6,
                 fmt = '🕫 : {}',
                 ),
        widget.Backlight(
                 backlight_name = "amdgpu_bl1",
                 change_command = "light -A {}",
                 foreground = colors[8],
                 padding = 6,
                 fmt = '🔆 : {}'
                 ),
        widget.Battery(padding = 3,
                       format='{char}{percent:2.0%}({hour:d}:{min:02d})',
                       low_percentage=0.3,
                       foreground = colors[4],
                       update_interval=20,
                       discharge_char='🔌',
                       charge_char='🔋',
                       notify_low=10,
                       notify_below=30),
        widget.Clock(
                 foreground = colors[8],
                 padding = 6,
                 format = "⏱  %a, %b %d - %H:%M",
                 ),
        widget.Systray(padding = 3),
        widget.QuickExit(padding = 3, default_text = ' ⏻ '),
        widget.Spacer(length = 8),
        ]
    return widgets_list
def init_widgets_bottom_list():
    widgets_list = [
        widget.Spacer(length = 12),
        widget.TaskList(
                 foreground = colors[7],
                 icon_size = 0,
                 border_width = 0,
                 rounded = True,
                 markup_focused = "<span foreground='white' underline='low'>{}</span>",
                 max_title_width = 500,
                 spacing = 20,
                 highlight_method = None,
                 # window_name_location = True,
                 stretch = True,
                 ),
        ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[15:16]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), margin=[0, 0, 0, 0], size=15),
        # bottom=bar.Bar(widgets=init_widgets_bottom_list(), margin=[0, 8, 0, 8], size=20),
          wallpaper="/home/shri/Pictures/Wallpaper/wall_1.jpg",
          wallpaper_mode="fill",
                   )]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="copyq"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "QTILE"
