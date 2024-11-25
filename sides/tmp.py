from appmodel import ModelDefault

from appcommands import *

m = ModelDefault("file3")


print(m.str_sub_sys.find_to(5, 3, "73", "TOP"))


