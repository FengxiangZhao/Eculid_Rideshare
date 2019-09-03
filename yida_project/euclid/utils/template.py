# subject_template_location = os.path.join(template_location, "email_%s_subject.txt") % template_prefix
# body_template_location = os.path.join(template_location, "email_%s_body.txt") % template_prefix
#
# subject = render_to_string(subject_template_location, context=context)
# body = render_to_string(body_template_location, context=context)

import os

from django.template.loader import render_to_string


def load_template_to_string(template_location, template_name, context):
    template_path = os.path.join(template_location, template_name)
    return render_to_string(template_path, context=context)

def load_fcm_text_message_from_template(template_location, template_prefix, context):
    title = load_template_to_string(template_location, "fcm_{:s}_title.txt".format(template_prefix), context)
    body = load_template_to_string(template_location, "body_{:s}_body.txt".format(template_prefix), context)
    return title, body

