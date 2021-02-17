import time
import sys

toolbar_width = 80

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width + 1)) # return to start of line, after '['

# for i in range(toolbar_width):
#     time.sleep(0.1)
#     # update the bar
#     sys.stdout.write("#")
#     sys.stdout.flush()

j = 0
for i in range(55000):
    j += 1
    time.sleep(0.0001)
    if j == int(55000/toolbar_width):
        sys.stdout.write("#")
        sys.stdout.flush()
        j = 0

sys.stdout.write("\n")
