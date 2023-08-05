# -*- coding: utf-8 -*-

from styles_events import update_PODtemplate_styles


def set_initial_md5(pod_template, event):
    """
    Set the md5 of the initial document template in 'initial_md5' field.
    """
    md5 = pod_template.current_md5
    if not pod_template.initial_md5:
        pod_template.initial_md5 = md5
        pod_template.style_modification_md5 = md5

    update_PODtemplate_styles(pod_template, event)
