from config import cfg
from processors import processor_base


class LifeProcessor(processor_base.CProcessor):
    def __init__(self):
        self.component_name = "Life"

        super().__init__()

    def private_process(self, component):

        # adjust hp if changes are queued
        if len(component.hp_queue) > 0:
            self.adjust_hp(component)

        # check so entity isn't dead
        self.check_if_alive(component)

    def adjust_hp(self, component):
        """
        If uid has a hp-change queued, make it happen

        :param component:
        :return:
        """
        # print("Adjusting hp", component.uid)

        hq = component.hp_queue
        while len(hq) > 0:
            component.hp += hq.pop()

    def check_if_alive(self, component):
        if component.hp < 0:
            component.alive = False
            cfg.post_to_log(component.uid, "dead")


lp = LifeProcessor()
