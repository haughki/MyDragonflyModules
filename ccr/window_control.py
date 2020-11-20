
#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for moving and controlling **windows**
=====================================================

This command-module offers commands for naming windows, bringing
named windows to the foreground, and positioning and resizing
windows.

Commands
--------

The following voice commands are available:

Command: **"name window <dictation>"**
    Assigns the given name to the current foreground window.

Command: **"focus <window name>"** or **"bring <window name> to the foreground"**
    Brings the named window to the foreground.

Command: **"focus title <window title>"**
    Brings a window with the given word(s) in the title to the foreground.

Command: **"place <window> <position> [on <monitor>]"**
    Relocates the target window to the given position.

Command: **"stretch <window> <position>"**
    Stretches the target window to the given position.

Usage examples
--------------

 - Say **"place window left"** to relocate the foreground window
   to the left side of the monitor it's on.
 - Say **"place Firefox top right on monitor 2"** to relocate
   the window which was previously named "Firefox" to the top right
   corner of the second display monitor.

"""

import pkg_resources
pkg_resources.require("dragonfly2 >= 0.6.5beta1.dev-r76")

import time, logging
from dragonfly import *
from supporting import utils
from ccr import rule_ccr

rule_log = logging.getLogger("rule")

#---------------------------------------------------------------------------
# Set up this module's configuration.

config = Config("Window control")
config.lang                = Section("Language section")
# Giving windows arbitrary names never seem to work properly for me. Naming a window would associate an arbitrary name
# with an in memory window object. But, in certain situations, the underlying window object for a given window could change,
# but the cached object would not 'refresh' (not automatically), so that the name for the window would have an old, outdated window object.
# config.lang.name_win       = Item("name (window | win) <name>",
#                                   doc="Command to give the foreground window a name; must contain the <name> extra.")
config.lang.focus_win      = Item("(jump | focus) <win_selector>",
                                  doc="Bring a named window to the foreground. 'focus chrome'")
config.lang.focus_title    = Item("(jump | focus) title <text>",
                                  doc="Bring a window with a given title (or title fraction) to the foreground. 'focus chrome google maps'")
#config.lang.translate_win  = Item("place <win_selector> <position> [on <mon_selector>]",
config.lang.translate_win  = Item("place <win_selector> (<position> [on <mon_selector>] | on <mon_selector>)",
                                  doc="Move a window to a monitor or to a location on a monitor. 'place chrome on 2' or 'place chrome top on 2'")
config.lang.nudge_win      = Item("nudge <win_selector> <direction> [<nudge_multiplier>]",
                                  doc="Nudge a window in a direction. 'nudge chrome right 6'")
config.lang.resize_win     = Item("place <win_selector> [from] <position> [to] <position> [on <mon_selector>]",
                                  doc="Move and resize a window. 'place chrome top right on 2'")
config.lang.stretch_win    = Item("stretch <win_selector> [to] <position>",
                                  doc="Stretch a window in a direction. 'stretch chrome left'")
config.lang.place_win_fraction = Item("place <win_selector> <position> <screen_fraction>",
                                      doc="Place a window according to a screen fraction. 'place chrome top third'")

#config.lang.win_selector   = Item("window | win | [window] <win_names> [<title_fragment>]",
config.lang.win_selector   = Item("[(this | current | window)] | <win_names> [<title_fragment>]",
                                  doc="Partial command for specifying a window; must contain the <win_names> extra.")
config.lang.mon_selector   = Item("(this | current) monitor | [monitor] <mon_names>",
                                  doc="Partial command for specifying a monitor; must contain the <mon_names> extra.")
config.lang.left           = Item("left", doc="Word for direction left or left side of monitor.")
config.lang.right          = Item("right", doc="Word for direction right or right side of monitor.")
config.lang.up             = Item("up", doc="Word for direction up.")
config.lang.down           = Item("down", doc="Word for direction down.")
config.lang.top            = Item("top", doc="Word for top side of monitor.")
config.lang.bottom         = Item("bottom", doc="Word for bottom side of monitor.")
config.lang.screen_fractions = Item({
    "half":     0.5,
    "third":    0.33,
    "quarter":  0.25,
},
    doc="Fractions of the screen")

config.settings            = Section("Settings section")
config.settings.grid       = Item(10, doc="The number of grid divisions a monitor is divided up into when placing windows.")
config.settings.defaults   = Item({
    "NatLink": {"exe_name": "natspeak", "title_hint": "messages from Natlink"},
    "idea": {"exe_name": "", "title_hint": ""},
    "studio": {"exe_name": "devenv", "title_hint": ""},
    "chrome": {"exe_name": "", "title_hint": "Google Chrome"},
}, doc="Default window names. Maps spoken-forms to {executable name, title, executable path} dict.")
#config.generate_config_file()
config.load()


#===========================================================================
# Create this module's main grammar object.

winctrl_grammar = Grammar("window control")


#---------------------------------------------------------------------------
# Dictionary list of window and monitor names.

win_names     = DictList("win_names")
win_names_ref = DictListRef("win_names", win_names)
mon_names     = DictList("mon_names")
mon_names_ref = DictListRef("mon_names", mon_names)

# Populate monitor names.
for i, m in enumerate(monitors):
    mon_names[str(i+1)] = m

#---------------------------------------------------------------------------
# Default window names handling.

default_names = config.settings.defaults

# Pre-populate the win_names mapping with the given default names.
for key in default_names.keys():
    win_names[key] = key


# Helper function to search for a default-name window.
def get_app_window(app_name, title_fragment=None):
    if title_fragment:
        title_fragment = title_fragment.lower()
    return find_window(app_name, title_fragment, **default_names[app_name])  # The last parameter here unpacks the dictionary into named parameters based on the dictionary keys.


def find_window(app_name, title_fragment, exe_name, title_hint):
    #exe_name, title_hint = default_names[app_name]
    if not exe_name:
        exe_name = app_name
    exe_name = exe_name.lower()
    if title_hint:
        title_hint = title_hint.lower()

    best_match = None
    got_title_hint_match = False

    # print "exe: " + exe_name
    # print "title frag: " + title_fragment
    # print "title hint: " + title_hint

    all_windows = Window.get_all_windows()
    # windows.sort(key=lambda x: x.executable
    for window in all_windows:
        if not utils.windowIsValid(window):
            continue

        rule_log.debug("wanted exe:{} actual exe:{}".format(exe_name.encode('utf-8'), window.executable.encode('utf-8').lower()))
        rule_log.debug("hint:{} title:{}".format(title_hint.encode('utf-8'), window.title.encode('utf-8').lower()))
        rule_log.debug("fragment:{} title:{}".format(title_fragment.encode('utf-8'), window.title.encode('utf-8').lower()))

        # there will always be an exe name because of check above
        if window.executable.lower().find(exe_name) != -1:
            if exe_name == "chrome" and window.title.lower().find("hidden tabs - workona") != -1:  # custom rule to never focus workona hidden tabs
                continue
            if not title_fragment and not title_hint:
                best_match = window
                break
            if not got_title_hint_match:
                best_match = window
            if title_fragment and window.title.lower().find(title_fragment) != -1:
                best_match = window
                break
            if title_hint and window.title.lower().find(title_hint) != -1:
                best_match = window
                got_title_hint_match = True

    if not best_match:
        raise StandardError(
            "Found no match for app_name: " + str(app_name) + " with title_fragment: " + str(title_fragment))

    # best_match.name = app_name
    return best_match


#---------------------------------------------------------------------------
# Internal window selector rule and element.

class WinSelectorRule(CompoundRule):

    spec = config.lang.win_selector
    extras = [
        win_names_ref,
        Dictation("title_fragment"),
    ]
    exported = False

    def value(self, node):
        if node.has_child_with_name("win_names"):
            app_name = node.get_child_by_name("win_names").value()
            # print "app_name: " + str(app_name)
            title_fragment = ""
            if node.has_child_with_name("title_fragment"):
                title_fragment = str(node.get_child_by_name("title_fragment").value())
                # print "title_fragment: " + title_fragment
            return get_app_window(app_name, title_fragment)
        return Window.get_foreground()

win_selector = RuleRef(WinSelectorRule(), name="win_selector")


#---------------------------------------------------------------------------
# Internal monitor selector rule and element.

class MonSelectorRule(CompoundRule):

    spec = config.lang.mon_selector
    extras = [mon_names_ref]
    exported = False

    def value(self, node):
        if node.has_child_with_name("mon_names"):
            return node.get_child_by_name("mon_names").value()
        return None

mon_selector = RuleRef(MonSelectorRule(), name="mon_selector")


#---------------------------------------------------------------------------
# Exported window focusing rule; brings named windows to the foreground.

class FocusWinRule(rule_ccr.CCRCompoundRule):
    spec = config.lang.focus_win
    extras = [win_selector]

    def _process_recognition(self, node, extras):
        window = extras["win_selector"]
        if not window:
            self._log.warning("No window with that name found.", exc_info=True)
            return
        self._log.debug("%s: bringing window '%s' to the foreground." % (self, window))
        for attempt in range(4):
            try:
                window.set_foreground()
            except Exception, e:
                self._log.warning("%s: set_foreground() failed: %s." % (self, e), exc_info=True)
                time.sleep(0.2)
            else:
                break


#---------------------------------------------------------------------------
# Exported window naming rule.
# Giving windows arbitrary names never seem to work properly for me. Naming a window would associate an arbitrary name
# with an in memory window object. But, in certain situations, the underlying window object for a given window could change
# and would not refresh, so that the name for the window would have an old, outdated window object.

# class NameWinRule(rule_ccr.CCRRule):
#
#     spec = config.lang.name_win
#     extras = [Dictation("name")]
#
#     def _process_recognition(self, node, extras):
#         name = str(extras["name"])
#         window = Window.get_foreground()
#         window.name = name
#         win_names[name] = window
#         self._log.debug("%s: named foreground window '%s'." % (self, window))



#---------------------------------------------------------------------------
# Exported window focusing rule; brings named windows to the foreground.

class FocusTitleRule(rule_ccr.CCRCompoundRule):

    spec = config.lang.focus_title
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        title = str(extras["text"])
        action = FocusWindow(title=title)
        try:
            action.execute()
        except ActionError:
            self._log.warning("No window with that name found.", exc_info=True)


#---------------------------------------------------------------------------
# Internal fraction rule.

class FractionRule(Rule):

    sections = config.settings.grid

    def __init__(self):
        Rule.__init__(self,
                      name="fraction",
                      element=Integer("_frac", 0, self.sections + 1),
                      exported=False)

    def value(self, node):
        value = node.get_child_by_name("_frac").value()
        return float(value) / self.sections

fraction_rule = FractionRule()


#---------------------------------------------------------------------------

horz_left    = Compound(config.lang.left,   name="horz", value=0.0)
horz_right   = Compound(config.lang.right,  name="horz", value=1.0)
vert_top     = Compound(config.lang.top,    name="vert", value=0.0)
vert_bottom  = Compound(config.lang.bottom, name="vert", value=1.0)
horz_frac    = RuleRef(fraction_rule, name="horz")
vert_frac    = RuleRef(fraction_rule, name="vert")

horz_expl    = Alternative([horz_left, horz_right],  name="horz_expl")
horz_all     = Alternative([horz_expl, horz_frac],   name="horz_all")
vert_expl    = Alternative([vert_top,  vert_bottom], name="vert_expl")
vert_all     = Alternative([vert_expl, vert_frac],   name="vert_all")


#---------------------------------------------------------------------------

position_element = Compound(
    spec="   <horz_expl>"              # 1D, horizontal
         " | <vert_expl>"              # 1D, vertical
         " | <horz_all> <vert_all>"    # 2D, horizontal-vertical
         " | <vert_expl> <horz_all>"   # 2D, vertical-horizontal
         " | <vert_all> <horz_expl>",  # 2D, vertical-horizontal
    extras=[horz_expl, horz_all, vert_expl, vert_all],
)
position_rule = Rule(
    name="position_rule",
    element=position_element,
    exported=False,
)
position = RuleRef(position_rule, name="position")


#---------------------------------------------------------------------------

class TranslateRule(rule_ccr.CCRCompoundRule):

    spec = config.lang.translate_win
    extras = [
        win_selector,                  # Window selector element
        mon_selector,                  # Monitor selector element
        position,                      # Position element
    ]

    def _process_recognition(self, node, extras):
        # Determine which window to place on which monitor.
        window = extras["win_selector"]

        # "monitor" is the destination monitor.
        if "mon_selector" in extras:
            monitor = extras["mon_selector"].rectangle
        else:
            monitor = window.get_containing_monitor().rectangle

        # Calculate available area within monitor.
        # x1, y1 is a (top?) left corner point. Not sure what the 1 is about.
        # dx, dy are dimensions of a rectangle.
        pos = window.get_position()       # Absolute position, across all monitors, of the window where it started before the move.
        m_x1 = monitor.x1 + pos.dx / 2    # The horizontal origin of the destination monitor, plus half the width of the original window.
        m_dx = monitor.dx - pos.dx        # The width of the destination monitor minus the width of the original window.
        m_y1 = monitor.y1 + pos.dy / 2
        m_dy = monitor.dy - pos.dy
        # print "pos.dx:" + str(pos.dx)
        # print "pos.dy:" + str(pos.dy)
        # print "mon.x1:" + str(monitor.x1)
        # print "mon.dx:" + str(monitor.dx)
        # print "mon.y1:" + str(monitor.y1)
        # print "mon.dy:" + str(monitor.dy)
        #
        # print "m__.x1:" + str(m_x1)
        # print "m__.dx:" + str(m_dx)
        # print "m__.y1:" + str(m_y1)
        # print "m__.dy:" + str(m_dy)


        # Get spoken position and calculate how far to move.
        # A command can specify a horizontal and/or vertical destination (left/right, top/bottom) or not.
        # If it doesn't, specify a horizontal, calculate the destination horizontal to be the same as the
        # start horizontal; that is, the window should be in the same position it was on the starting
        # monitor. THIS ASSUMES THE SIZE OF ALL MONITORS IS EQUAL.
        horizontal = node.get_child_by_name("horz")
        # print "horizontal: " + str(horizontal)

        if horizontal:
            # print "pos.center.x: " + str(pos.center.x)
            dx = m_x1 + (horizontal.value() * m_dx) - pos.center.x
            # print "horizontal_value: " + str(horizontal.value())
        else:
            # THE FOLLOWING CODE ASSUMES THE SIZE OF ALL MONITORS IS EQUAL.
            # If I don't specify a horizontal destination (left/right), then I want to move the window to exactly the same horizontal
            # on the new monitor -- the same horizontal it had the old monitor. This is just what I wanted -- it seemed to make the
            # most sense to me, and I couldn't understand why the existing code was defaulting to moving the window to the left-hand
            # side of the screen, even when I didn't specify "left". It turns out there's a reason :-)
            #
            # At this point in the code, we know the absolute (across all monitors) x,y starting point and original dimensions of the
            # window we are moving. We also know the absolute x,y corner and dimensions of the monitor we are moving to. BUT, we don't
            # know anything about _which_ monitor we started on, nor do we know anything (dimensions, etc.) about that monitor.
            # Without this information, it seems to be impossible (?) to "robustly" calculate the destination horizontal we want. By
            # "robustly", I mean to calculate the horizontal for all possible combinations of monitors of different sizes. For example,
            # if monitor one was 800x600, and monitor two was 1920 x 1200 (or possibly vice versa, or three monitors, all of different
            # sizes, etc.), it doesn't seem possible to calculate the horizontal that I want; that is, the same horizontal as a window
            # had before the move.
            #
            # I think that's why the original author chose to default to left. I decided that since both my monitors are the same size,
            # that I would just assume that, and write the code that I wanted. If at some point I had a laptop into the mix here, I
            # should revert back to the old code which is simply: 'dx = m_x1 - pos.center.x' -- see commented out code at the bottom of
            # the code block.

            # print "pos.x1: " + str(pos.x1)
            start_monitor = 1  # leftmost monitor
            target_monitor = 1
            if pos.x1 >= monitor.dx:
                start_monitor = 2  # rightmost monitor

            if monitor.x1 > 0:
                target_monitor = 2

            # print "start_monitor: " + str(start_monitor)
            # print "target_monitor: " + str(target_monitor)

            dx = 0
            if start_monitor == 1 and target_monitor == 2:
                dx = monitor.dx
            elif start_monitor == 2 and target_monitor == 1:
                dx = -monitor.dx

            # This is the original code that 'hard codes'the destination horizontal to 'left'. See comments above.
            #dx = m_x1 - pos.center.x


        vertical = node.get_child_by_name("vert")
        # print "vertical: " + str(vertical)
        if vertical:
            dy = m_y1 + vertical.value() * m_dy - pos.center.y
        else:
            dy = 0

        # print "dx: " + str(dx)
        # print "dy: " + str(dy)

        # Translate and move window.
        # dx and dy represent the distance values to move the window from its current position to its new position.
        # So, for example, -10, 20 would move the window 10 pixels left and 20 pixels up.
        # print "*******"
        # print str(dx) + ", " + str(dy)
        pos.translate(dx, dy)
        # window.move(pos, animate="spline")
        window.move(pos)


#---------------------------------------------------------------------------

nudge_increment = 20
direction_left    = Compound(config.lang.left,   name="direction_left", value=("x", -nudge_increment))
direction_right   = Compound(config.lang.right,  name="direction_right", value=("x", nudge_increment))
direction_up    = Compound(config.lang.up,    name="direction_up", value=("y", -nudge_increment))
direction_down  = Compound(config.lang.down, name="direction_down", value=("y", nudge_increment))

nudge_basic    = Alternative([direction_left, direction_right, direction_up, direction_down],  name="nudge_basic")

direction_up_left = Sequence([direction_up, direction_left])
direction_up_right = Sequence([direction_up, direction_right])
direction_down_left = Sequence([direction_down, direction_left])
direction_down_right = Sequence([direction_down, direction_right])
nudge_diagonal = Alternative([direction_up_left, direction_up_right, direction_down_left, direction_down_right], name="nudge_diagonal")

#nudge_multi     = Alternative([],   name="nudge_multi")

#---------------------------------------------------------------------------

direction_element = Compound(
    spec="   <nudge_basic>"
         " | <nudge_diagonal>",
    extras=[nudge_basic, nudge_diagonal],
)
direction_rule = Rule(
    name="direction_rule",
    element=direction_element,
    exported=False,
)
direction = RuleRef(direction_rule, name="direction")

nudge_multiplier = IntegerRef("nudge_multiplier", 1, 20)

def calculateNewPosition(direction_and_value, multiplier):
    new_position = [0, 0]
    if type(direction_and_value) is list:   # E.g., "nudge down right" --> [('y', 20), ('x', 20)]
        for direct in direction_and_value:
            val = direct[1] * multiplier
            if direct[0] == "x":
                new_position[0] += val
            else:
                new_position[1] += val
    else:  # we have a tuple with just one set of coordinates. For example: "nudge up" --> ('y', -20)
        val = direction_and_value[1] * multiplier
        if direction_and_value[0] == "x":
            new_position[0] = val
        else:
            new_position[1] = val
    return tuple(new_position)

class NudgeRule(rule_ccr.CCRCompoundRule):

    spec = config.lang.nudge_win
    extras = [
        win_selector,                  # Window selector element
        direction,
        nudge_multiplier
    ]

    def _process_recognition(self, node, extras):
        # Determine which window to place on which monitor.
        window = extras["win_selector"]
        a_direction = extras["direction"]
        multiplier = 1
        if "nudge_multiplier" in extras:
            multiplier = extras["nudge_multiplier"]

        pos = window.get_position()
        # print "direction: " + str(a_direction)
        # print calculateNewPosition(a_direction, multiplier)
        new_position = calculateNewPosition(a_direction, multiplier)
        pos.translate(new_position[0], new_position[1])
        window.move(pos)

#---------------------------------------------------------------------------

class ResizeRule(rule_ccr.CCRCompoundRule):

    spec = config.lang.resize_win
    extras = [
        win_selector,                  # Window selector element
        mon_selector,                  # Monitor selector element
        position,                      # Position element
    ]

    def _process_recognition(self, node, extras):
        # Determine which window to place on which monitor.
        window = extras["win_selector"]
        pos = window.get_position()
        monitor = window.get_containing_monitor().rectangle

        # Determine horizontal positioning.
        nodes = node.get_children_by_name("horz")
        horizontals = [(monitor.x1 + n.value() * monitor.dx) for n in nodes]
        if len(horizontals) == 1:
            horizontals.extend([pos.x1, pos.x2])
        elif len(horizontals) != 2:
            self._log.error("%s: Internal error."  % self, exc_info=True)
            return
        x1, x2 = min(horizontals), max(horizontals)

        # Determine vertical positioning.
        nodes = node.get_children_by_name("vert")
        verticals = [(monitor.y1 + n.value() * monitor.dy) for n in nodes]
        if len(verticals) == 1:
            verticals.extend([pos.y1, pos.y2])
        elif len(verticals) != 2:
            self._log.error("%s: Internal error."  % self, exc_info=True)
            return
        y1, y2 = min(verticals), max(verticals)

        # Move window.
        pos = Rectangle(x1, y1, x2-x1, y2-y1)
        window.move(pos, animate="spline")


#---------------------------------------------------------------------------

class StretchRule(rule_ccr.CCRCompoundRule):

    spec = config.lang.stretch_win
    extras = [
        win_selector,                  # Window selector element
        position,                      # Position element
    ]

    def _process_recognition(self, node, extras):
        # Determine which window to place.
        window = extras["win_selector"]
        pos = window.get_position()
        monitor = window.get_containing_monitor().rectangle

        # Determine horizontal positioning.
        horizontals = [pos.x1, pos.x2]
        child = node.get_child_by_name("horz")
        if child: horizontals.append(monitor.x1 + child.value() * monitor.dx)
        x1, x2 = min(horizontals), max(horizontals)

        # Determine vertical positioning.
        verticals = [pos.y1, pos.y2]
        child = node.get_child_by_name("vert")
        if child: verticals.append(monitor.y1 + child.value() * monitor.dy)
        y1, y2 = min(verticals), max(verticals)

        # Move window.
        pos = Rectangle(x1, y1, x2-x1, y2-y1)
        window.move(pos, animate="spline")


#---------------------------------------------------------------------------

screen_fraction = Choice("screen_fraction", config.lang.screen_fractions)

class PlaceFractionRule(rule_ccr.CCRCompoundRule):

    spec = config.lang.place_win_fraction
    extras = [
        win_selector,                  # Window selector element
        position,                      # Position element
        screen_fraction,               # Screen fraction element
    ]

    def _process_recognition(self, node, extras):
        # Determine which window to place.
        window = extras["win_selector"]
        #pos = window.get_position()
        monitor = window.get_containing_monitor().rectangle

        # Determine screen fraction.
        fraction = extras["screen_fraction"]

        # Determine horizontal positioning.
        child = node.get_child_by_name("horz")
        if child:
            dx = monitor.dx * fraction
            x1 = monitor.x1 + child.value() * (monitor.dx - dx)
        else:
            dx = monitor.dx
            x1 = monitor.x1

        # Determine vertical positioning.
        child = node.get_child_by_name("vert")
        if child:
            dy = monitor.dy * fraction
            y1 = monitor.y1 + child.value() * (monitor.dy - dy)
        else:
            dy = monitor.dy
            y1 = monitor.y1

        # Move window.
        pos = Rectangle(x1, y1, dx, dy)
        window.move(pos, animate="spline")

#---------------------------------------------------------------------------

# winctrl_grammar.load()
# def unload():
#     global winctrl_grammar
#     winctrl_grammar = utils.unloadHelper(winctrl_grammar, __name__)
