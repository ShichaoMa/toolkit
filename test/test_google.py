from translate import Translate


with Translate("google") as t:
    t.set_logger()
    print(t.translate("my name is tom, i come from nanjing, I like eat shit, what about yours?"))