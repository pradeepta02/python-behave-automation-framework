# -*- coding: UTF-8 -*-


from features.support.core.elementaction import ElementAction


class BasePage(object):
    """All page classes must extend this class in order to use the webdriver actions
    """
    def __init__(self, context):
        self.context = context
        self.element_action = ElementAction(context)
