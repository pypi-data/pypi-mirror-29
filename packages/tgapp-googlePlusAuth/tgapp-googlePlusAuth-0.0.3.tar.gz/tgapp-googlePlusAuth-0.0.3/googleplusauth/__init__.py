# -*- coding: utf-8 -*-
"""The tgapp-googlePlusAuth package"""
from tg.configuration import milestones


def plugme(app_config, options):
    from .model import import_models
    milestones.config_ready.register(import_models)

    return dict(appid='googleplusauth', global_helpers=False)