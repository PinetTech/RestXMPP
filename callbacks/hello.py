from callback import Callback

class Hello(Callback):
    def run(self, args = None):
        print "Hello, run"
        print args


    def test(self, args = None):
        print "Hello, test"
        print args

