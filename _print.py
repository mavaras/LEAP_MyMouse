from gvariables import gv


def _print(string):
    print(string)
    gv.stdout += "__> " + string + "\n"
    gv.main_window.textArea_logs.setPlainText(gv.stdout)
