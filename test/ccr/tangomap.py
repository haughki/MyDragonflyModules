from dragonfly import MappingRule, Function, Config, Section, Item

def printTango(): print "tango"
def printUniform(): print "uniform"


config = Config("test map")
config.cmd = Section("Command section")
config.cmd.map = Item(
    # Here we define the *default* command map.  If you would like to modify it to your personal taste, please *do not* make changes
    #  here.  Instead change the *config file* called "_multiedit.txt".  If it exists, the map there will replace this one.
    {
        "print tango": Function(printTango),
        "print uniform": Function(printUniform),
    },
    doc="Default window names. Maps spoken-forms to {executable name, title, executable path} dict."
)
config.load()



class TangoMap(MappingRule):
    mapping = config.cmd.map