class Color:
    def color(self, string):
        return self.red(string) if string == 'False' else self.green(string) if  string == 'True' else self.yellow(string)
    def red(self, string):
        return '\033[1;31m' + string + '\033[1;0m'
    def green(self, string):
        return '\033[1;32m' + string + '\033[1;0m'
    def yellow(self, string):
        return '\033[1;33m' + string + '\033[1;0m'
    def white(self, string):
        return '\033[1;37m' + string + '\033[1;0m'
