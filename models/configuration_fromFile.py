from configuration import Conf
import linecache
from _print import _print


class ConfFromFile(Conf):
    def load_conf(self, conf):
        """ loads given configuration file into this object

            :param conf: file
            """
        # conf info
        self.file_name = conf.readline()
        self.file_path = conf.readline()
        self.file_date = conf.readline()

        # basic conf
        self.basic.mm = linecache.getline(str(conf.name), 6).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.lclick = linecache.getline(str(conf.name), 7).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.rclick = linecache.getline(str(conf.name), 8).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.vscroll = linecache.getline(str(conf.name), 9).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.hscroll = linecache.getline(str(conf.name), 10).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.grabb = linecache.getline(str(conf.name), 11).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.changew = linecache.getline(str(conf.name), 12).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.closew = linecache.getline(str(conf.name), 13).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.minimizew = linecache.getline(str(conf.name), 14).split(":")[1].replace("\n", "").replace("\r", "")

        # extra conf
        """self.basic.mm = linecache.getline(str(conf.name), 6)
        self.basic.lclick = linecache.getline(str(conf.name), 7)
        self.basic.rclick = linecache.getline(str(conf.name), 8)"""
        print("->" + str(self.basic.closew))
        print("Content of configuration file " + str(conf.name) + ":")
        for line in conf:
            print("    " + str(line)),