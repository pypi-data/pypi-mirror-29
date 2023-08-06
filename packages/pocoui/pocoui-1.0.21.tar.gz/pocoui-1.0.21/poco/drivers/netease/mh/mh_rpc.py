# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-13 18:01:23
from poco.freezeui.hierarchy import FreezedUIHierarchy, FreezedUIDumper
from poco.sdk.interfaces.input import InputInterface
from poco.sdk.interfaces.screen import ScreenInterface
from poco.utils.simplerpc.utils import sync_wrapper


class MhScreen(ScreenInterface):
    def __init__(self, client):
        super(MhScreen, self).__init__()
        self.c = client

    @sync_wrapper
    def getPortSize(self):
        return self.c.call("get_size")

    @sync_wrapper
    def getScreen(self, width):
        # FIXME: get screen 是 get_size ？
        return self.c.call("get_size"), 'png'


class MhInput(InputInterface):
    def __init__(self, client):
        super(MhInput, self).__init__()
        self.c = client

    @sync_wrapper
    def click(self, x, y, op="left"):
        # FIXME: 这个函数签名不对
        print((x, y), op)
        return self.c.call("click", (x, y), op)

    def getTouchDownDuration(self):
        return 0.01


class MhDumper(FreezedUIDumper):
    def __init__(self, client):
        super(MhDumper, self).__init__()
        self.c = client

    @sync_wrapper
    def dumpHierarchy(self):
        return self.c.call("dump")


class MhHierarchy(FreezedUIHierarchy):
    def __init__(self, client):
        super(MhHierarchy, self).__init__(MhDumper(client))
        self.c = client

    def setAttr(self, node, name, val):
        if isinstance(node, (list, tuple)):
            node = node[0]
        node_id = node[0]["desc"]
        self._setattr(node_id, name, val)

    @sync_wrapper
    def _setattr(self, node_id, name, val):
        return self.c.call("setattr", node_id, name, val)


if __name__ == '__main__':
    from pprint import pprint
    r = MhHierarchy(addr=("10.254.245.124", 5001))
    # size = r.getPortSize()
    # r.click((0.5, 0.5))
    # dump = r.dump()
    # pprint(dump)
    # root = (dict_2_node(dump))
    # pprint(root)
    # pprint(root.getParent())
    # pprint(root.getChildren())
    nodes = r.select(["and", [["attr=", ["text", u"长安城"]]]])
    # nodes = r.select(["and",[["attr=",["type", "Text"]]]])
    pprint(nodes[0].node)
