from sys import stdout

class Progress_Bar(object):
    def __init__(self, N, max_bar_num=50, prefix='Progress:'):
        self.N = N
        self.max_bar_num = max_bar_num
        self.prefix = prefix
    
    def print(self,i, always_print_new_line=False):
        if i >= self.N: raise IndexError("index, %d, out of range 0 ~ %d" % (i, self.N-1))
        bar_num = int((i+1) / self.N * self.max_bar_num)
        bar_string = ''
        for idx in range(bar_num): bar_string += '='
        bar_string += '>'
        for idx in range(self.max_bar_num - bar_num): bar_string += ' '
        percent = int((i+1) / self.N * 100)
        progress_report = '\r%s%s[%03d%%]' % (self.prefix, bar_string, percent)
        stdout.write(progress_report)
        stdout.flush()
        if ((i+1) == self.N) or always_print_new_line:
            stdout.write('\n')


