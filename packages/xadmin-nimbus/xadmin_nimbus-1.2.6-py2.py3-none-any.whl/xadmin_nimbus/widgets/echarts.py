# -*- coding: utf-8 -*-
from __future__ import absolute_import

import calendar
import datetime
import decimal
import logging
import copy

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.template import loader
from django.utils.encoding import smart_unicode, smart_str, smart_bytes
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _, ugettext
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.util import lookup_field, label_for_field, force_unicode, json
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.views.base import filter_hook, csrf_protect_m
from xadmin.views.dashboard import ModelBaseWidget, widget_manager

from .mixin import EChartsMixin

__all__ = [
    "EChartsPlugin",
    "EChartsView",
    "EChartsWidget",
]

logger = logging.getLogger(__name__)


@widget_manager.register
class EChartsWidget(ModelBaseWidget):
    widget_type = 'echarts'
    description = _('Show models echarts chart.')
    template = 'xadmin/widgets/echarts.html'
    widget_icon = 'fa fa-bar-chart-o'

    def convert(self, data):
        self.list_params = data.pop('params', {})
        self.chart = data.pop('chart', None)

    def setup(self):
        super(EChartsWidget, self).setup()

        self.charts = {}
        self.one_chart = False
        model_admin = self.admin_site._registry[self.model]
        chart = self.chart

        if hasattr(model_admin, 'echarts_charts'):
            if chart and chart in model_admin.echarts_charts:
                self.charts = {chart: model_admin.echarts_charts[chart]}
                self.one_chart = True
                if self.title is None:
                    self.title = model_admin.echarts_charts[chart].get('title')
            else:
                self.charts = model_admin.echarts_charts
                if self.title is None:
                    self.title = ugettext("%s Charts") % self.model._meta.verbose_name_plural

    def filte_choices_model(self, model, modeladmin):
        return bool(getattr(modeladmin, 'echarts_charts', None)) and \
            super(EChartsWidget, self).filte_choices_model(model, modeladmin)

    def get_chart_url(self, name, v):
        return self.model_admin_url('echarts', name) + "?" + urlencode(self.list_params)

    def get_chart_height(self, v):
        return v.get("height", "300px")

    def context(self, context):
        context.update({
            'charts': [{
                "name": name,
                "title": v['title'],
                "url": self.get_chart_url(name, v),
                "height": self.get_chart_height(v),
            } for name, v in self.charts.items()],
        })

    # Media
    def media(self):
        return self.vendor('xadmin.echarts.min.js', 'xadmin.echarts.theme.vintage.js', 'xadmin.plugin.widget.echarts.js')


class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return calendar.timegm(o.timetuple()) * 1000
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            try:
                return super(JSONEncoder, self).default(o)
            except Exception:
                return smart_unicode(o)


class EChartsPlugin(BaseAdminPlugin):
    echarts_charts = {}

    def init_request(self, *args, **kwargs):
        return bool(self.echarts_charts)

    def get_chart_url(self, name, v):
        return self.admin_view.model_admin_url('echarts', name) + self.admin_view.get_query_string()

    def get_chart_height(self, v):
        return v.get("height", "300px")

    # Media
    def get_media(self, media):
        return media + self.vendor('xadmin.echarts.min.js', 'xadmin.echarts.theme.vintage.js', 'xadmin.plugin.echarts.js')

    # Block Views
    def block_results_top(self, context, nodes):
        context.update({
            'charts': [{
                "name": name,
                "title": v['title'],
                "url": self.get_chart_url(name, v),
            } for name, v in self.echarts_charts.items()],
        })
        nodes.append(loader.render_to_string(
            'xadmin/blocks/model_list.results_top.echarts.html',
            context=get_context_dict(context))
        )


class EChartsView(EChartsMixin, ListAdminView):
    echarts_charts = {}

    def get_ordering(self):
        if 'order' in self.chart:
            return self.chart['order']
        else:
            return super(EChartsView, self).get_ordering()

    @filter_hook
    def make_chart_xfield(self, name=None, chart=None, xfield=None, obj=None, format="%Y-%m-%d %H:%M:%S"):
        xf, xattrs, value = lookup_field(xfield, obj, self)
        x_field = self.opts.get_field(xfield)
        if format and type(x_field) in (models.DateTimeField, models.DateField, models.TimeField):
            if type(x_field) is models.DateField:
                x_format = format
            elif type(x_field) is models.TimeField:
                x_format = format
            else:
                x_format = format
            value = value.strftime(x_format)
        return value

    @filter_hook
    def make_chart_yfield(self, name=None, chart=None, yfield=None, obj=None):
        yf, yattrs, value = lookup_field(yfield, obj, self)
        return value

    @filter_hook
    def make_chart_result_list(self, name=None, chart=None, echarts_type=None, xfield=None, yfields=None):
        self.make_result_list()
        return self.result_list

    def get_echarts_xfield(self, name=None, chart=None, xfield=None, obj=None, format="%Y-%m-%d %H:%M:%S"):
        st, value = super(EChartsView, self).get_echarts_xfield(name=name, chart=chart, xfield=xfield, obj=obj, format=format)
        if st:
            return value
        return self.make_chart_xfield(name=name, chart=chart, xfield=xfield, obj=obj, format=format)

    def get_echarts_yfield(self, name=None, chart=None, yfield=None, obj=None):
        st, value = super(EChartsView, self).get_echarts_yfield(name=name, chart=chart, yfield=yfield, obj=obj)
        if st:
            return value
        return self.make_chart_yfield(name=name, chart=chart, yfield=yfield, obj=obj)

    def get_echarts_label(self, name=None, option=None, yfield=None):
        label = super(EChartsView, self).get_echarts_label(name, option, yfield)
        return label or force_unicode(label_for_field(yfield, self.model, model_admin=self))

    def get_echarts_options(self, name=None, chart=None, echarts_type=None, xfield=None, yfields=None, datas=None):
        return super(EChartsView, self).get_echarts_options(name, chart, echarts_type, xfield, yfields, datas)

    def get_echarts_datas(self, name=None, chart=None, echarts_type=None, xfield=None, yfields=None):
        return self.make_chart_result_list(name=name, chart=chart, echarts_type=echarts_type, xfield=xfield, yfields=yfields)

    @csrf_protect_m
    @filter_hook
    def get(self, request, name):
        return self.get_echarts_response(request=request, name=name)


site.register_plugin(EChartsPlugin, ListAdminView)
site.register_modelview(r'^echarts/(.+)/$', EChartsView, name='%s_%s_echarts')

