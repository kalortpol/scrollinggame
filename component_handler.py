from config import cfg
"""
    Processors
"""
from processors import life_processor
from processors import csprite_processor
"""
    Body
"""


class ComponentHandler:
    """
    System handling components.

    Methods for controlling all components

    * Load JSON file with templates of entities (combinations of components and their values)

    * Add component to UID -> handled by component processor
    * Change component in UID -> handled by component processor
    * Remove component from UID -> handled by component processor

    * Make UID - Components directory for reversed iteration
        - Allows for iterating through only active UIDs components
        - Probably huge performance boost

    * Iterate through all components (ie subclasses of component)
    * Iterate through a component's instances

    * Check if UID has component
    * Check all components of UID
    * Get all UID in component
    * Check if component has UID

    * Get var from UIDs component instance
    * Set var from UIDs component instance

    * Create UID with arbitrary components
    """

    def __init__(self):
        self.processors = {"Life": life_processor.lp,
                           "CSprite": csprite_processor.csp}

    def get_all_component_classes(self) -> list:
        """

        :return list of all component sub-classes:
        """

        complist = list()

        for x in cfg.components.keys():
            complist.append(x)
        return complist

    def get_all_component_instances(self, component: str) -> list:
        """
        Returns list of component instances of a specific component.
        Iterate over this list in component processor

        :return list of instances:
        """

        if component in cfg.components:
            return cfg.components[component]

    def check_if_uid_has_component(self, component: str, uid: int) -> bool:
        """
        Self explanatory

        :return bool:
        """

        return self.check_component_has_uid(component, uid)

    def get_all_uid_in_component(self, component: str) -> list:
        """
        Returns all UIDs that has component

        :return list:
        """

        uidlist = list()
        comp_instances = self.get_all_component_instances(component)
        ll = len(comp_instances)

        for i in range(ll):
            uidlist.append(comp_instances[i].uid)

        return uidlist

    def check_component_has_uid(self, component: str, uid: int) -> bool:
        """
        Self explanatory

        :return bool:
        """

        if cfg.components[component]: comp = cfg.components[component]

        if uid in self.get_all_uid_in_component(component): return True

        else: return False

    def get_component_object_from_uid(self, component: str, uid: int) -> object:
        """
        Returns the component instance coupled with the UID

        :return object:
        """

        if self.check_component_has_uid(component, uid):
            uid_obj = None

            for x in cfg.components[component]:
                if x.uid == uid:
                    return x

    def get_cattr_list_uid(self, component: str, uid: int) -> dict:
        """
        Returns dict of component instance's attributes

        :return dict, or None if no component found for UID:
        """

        if self.check_component_has_uid(component, uid):
            uid_obj = None

            for x in cfg.components[component]:
                if x.uid == uid:
                    return vars(x)
        else:
            return None

    def get_cattr_uid(self, component: str, uid: int, var_name) -> vars:
        """
        Returns variable value of component belonging to UID
        Can be used to MANIPULATE THE VALUE! EASIER THAN USING SET_CATTR OR CHANGE_CATTR :)

        :return value:
        """

        if self.get_cattr_list_uid(component, uid):
            varlist = self.get_cattr_list_uid(component, uid)

            component_instance = self.get_component_object_from_uid(component, uid)

            if var_name in varlist:
                return varlist[var_name]

    def set_cattr_uid(self, component: str, uid: int, var_name, var_val) -> None:
        """
        Sets attribute of component belonging to UID

        :return None:
        """

        if self.get_cattr_list_uid(component, uid):
            varlist = self.get_cattr_list_uid(component, uid)

            component_instance = self.get_component_object_from_uid(component, uid)

            if var_name in varlist:
                setattr(component_instance, var_name, var_val)

    def change_cattr_uid(self, component: str, uid: int, var_name, var_change) -> None:
        """
        Changes the attribute value in component belonging to UID
        Only addition and subtraction

        :return None:
        """

        if self.get_cattr_list_uid(component, uid):
            varlist = self.get_cattr_list_uid(component, uid)

            component_instance = self.get_component_object_from_uid(component, uid)

            if var_name in varlist:
                old_val = varlist[var_name]
                new_val = old_val + var_change
                setattr(component_instance, var_name, new_val)

    """
        Specific component methods
    """

    def get_position(self, uid):
        return self.get_cattr_uid("CSprite", uid, "pos")

    def set_position(self, uid, pos):
        self.set_cattr_uid("Csprite", uid, "pos", pos)

    def try_move_sprite(self, uid, x, y):
        self.get_component_object_from_uid("CSprite", uid).move_queue.append((x, y))

    def force_move_sprite(self, uid, x, y):
        self.get_component_object_from_uid("CSprite", uid).pos[0] += x
        self.get_component_object_from_uid("CSprite", uid).pos[1] += y

    """
     Methods calling component processors
    """

    def iterate_components(self):
        """
        Iterate over component types and call processors for each instance
        Adjust order in this method
        :return:
        """
        pass

    def iterate_processor(self, component: str):
        """
        Runs param components processor if it is specified in self.processors

        Works :)

        :param component:
        :return:
        """
        component_instances = self.get_all_component_instances(component)

        assert component_instances is not None, "[iterate_processor] no component instance found"

        for x in component_instances:
            self.processors[component].process(x)


component_handler = ComponentHandler()
