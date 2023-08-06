from django.conf import settings

WIDGET_TEMPLATE = getattr(settings, 'MKEDITOR_WIDGET_TEMPLATE', 'editor.html')
WIDGET_CSS = getattr(settings, 'MKEDITOR_WIDGET_CSS', ('css/style.css','css/editormd.css' ))