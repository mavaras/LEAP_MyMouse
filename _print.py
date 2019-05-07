import gvariables


def _print(string):
    print(string)
    gvariables.stdout += "__> " + string + "\n"
    gvariables.main_window.textArea_logs.setPlainText(gvariables.stdout)
