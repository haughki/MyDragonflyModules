from dragonfly import CompoundRule

class CompoundTestCCR(CompoundRule):
    spec = "compound testing"

    def _process_recognition(self, node, extras):
        print "testing the compound"