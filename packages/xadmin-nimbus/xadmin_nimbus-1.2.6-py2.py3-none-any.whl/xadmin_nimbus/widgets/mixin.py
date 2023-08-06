# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import uuid
import copy
import logging
import calendar
import datetime
import decimal
import collections
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import widgets
from django.contrib.admin.utils import label_for_field, lookup_field
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import resolve_url
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate, Max, Min
from django.db.models.fields import BLANK_CHOICE_DASH
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.sessions.models import Session
from django.utils.html import escape
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_unicode, force_unicode
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

from pyecharts import (
    Bar,
    Line,
    Line3D,
    Pie,
    Gauge,
    Geo,
    GeoLines,
    Graph,
    Liquid,
    Radar,
    Scatter,
    EffectScatter,
    WordCloud,
    Funnel,
    Map,
    Parallel,
    Polar,
    HeatMap,
    TreeMap,
    Kline,
    Boxplot,

    Style,
    Page,
    Overlap,
    Grid,
    Timeline,
)

from .constants import *


__all__ = [
    "EChartsMixin",
]

logger = logging.getLogger(__name__)


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


class EChartsMixin(object):
    echarts_charts = {}

    def get_echarts_type(self, chart):
        if isinstance(chart, dict):
            return chart.get("echarts_type", ECHARTS_TYPE_LINE)
        return ECHARTS_TYPE_LINE

    def get_echarts_xfield(self, name=None, chart=None, xfield=None, obj=None, format="%Y-%m-%d %H:%M:%S"):
        if isinstance(obj, dict):
            value = obj.get(xfield, None)
        else:
            value = getattr(obj, xfield, None)
        st = False if value is None else True
        return st, value

    def get_echarts_yfield(self, name=None, chart=None, yfield=None, obj=None):
        if isinstance(obj, dict):
            value = obj.get(yfield, None)
        else:
            value = getattr(obj, yfield, None)
        st = False if value is None else True
        return st, value

    def get_echarts_label(self, name=None, option=None, yfield=None):
        key = u"{}_label".format(yfield)
        if isinstance(option, dict):
            value = option.get(key, "")
        else:
            value = ""
        return value

    def get_echarts_options(self, name=None, chart=None, echarts_type=None, xfield=None, yfields=None, datas=None):
        datas = [] if datas is None else datas
        page = Page()
        title = chart.get("title", "")
        subtitle = chart.get("subtitle", "")
        option = chart.get("option", {})
        x_option = option.get(xfield, {})
        x_format = x_option.pop("x-format", None)

        style = Style(title=title, subtitle=subtitle, **x_option)
        echart = ""
        if echarts_type == ECHARTS_TYPE_LINE:
            echart = Line(**style.init_style)
            for i, yfname in enumerate(yfields):
                e_label = self.get_echarts_label(name=name, option=option, yfield=yfname)
                # e_label = force_unicode(label_for_field(yfname, self.model, model_admin=self))
                e_attrs = []
                e_values = []
                for index, obj in enumerate(datas, start=1):
                    xvalue = self.get_echarts_xfield(name=name, chart=chart, xfield=xfield, obj=obj, format=x_format)
                    yvalue = self.get_echarts_yfield(name=name, chart=chart, yfield=yfname, obj=obj)
                    e_attrs.append(xvalue)
                    e_values.append(yvalue)
                kwargs = option.get(yfname, {})
                echart.add(e_label, e_attrs, e_values, **kwargs)
        elif echarts_type == ECHARTS_TYPE_BAR:
            echart = Bar(**style.init_style)
            for i, yfname in enumerate(yfields):
                e_label = self.get_echarts_label(name=name, option=option, yfield=yfname)
                # e_label = force_unicode(label_for_field(yfname, self.model, model_admin=self))
                e_attrs = []
                e_values = []
                for index, obj in enumerate(datas, start=1):
                    xvalue = self.get_echarts_xfield(name=name, chart=chart, xfield=xfield, obj=obj, format=x_format)
                    yvalue = self.get_echarts_yfield(name=name, chart=chart, yfield=yfname, obj=obj)
                    e_attrs.append(xvalue)
                    e_values.append(yvalue)
                kwargs = option.get(yfname, {})
                echart.add(e_label, e_attrs, e_values, **kwargs)
        elif echarts_type == ECHARTS_TYPE_PIE:
            echart = Pie(**style.init_style)
            for i, yfname in enumerate(yfields):
                e_label = self.get_echarts_label(name=name, option=option, yfield=yfname)
                # e_label = force_unicode(label_for_field(yfname, self.model, model_admin=self))
                e_attrs = []
                e_values = []
                for index, obj in enumerate(datas, start=1):
                    xvalue = self.get_echarts_xfield(name=name, chart=chart, xfield=xfield, obj=obj, format=x_format)
                    yvalue = self.get_echarts_yfield(name=name, chart=chart, yfield=yfname, obj=obj)
                    e_attrs.append(xvalue)
                    e_values.append(yvalue)
                kwargs = option.get(yfname, {})
                echart.add(e_label, e_attrs, e_values, **kwargs)
        elif echarts_type == ECHARTS_TYPE_LIQUID:
            echart = Liquid(**style.init_style)
            echart.add(u"Liquid", [0.6])

        elif echarts_type == ECHARTS_TYPE_LINE3D:
            echart = Line3D(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_GAUGE:
            echart = Gauge(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_GEO:
            echart = Geo(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_GEOLINES:
            echart = GeoLines(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_GRAPH:
            echart = Graph(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_RADAR:
            echart = Radar(**style.init_style)
            config = chart.get("config", {})
            echart.config(**config)

        elif echarts_type == ECHARTS_TYPE_SCATTER:
            echart = Scatter(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_WORDCLOUD:
            echart = WordCloud(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_FUNNEL:
            echart = Funnel(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_MAP:
            echart = Map(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_PARALLEL:
            echart = Parallel(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_POLAR:
            echart = Polar(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_HEATMAP:
            echart = HeatMap(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_TREEMAP:
            echart = TreeMap(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_BOXPLOT:
            echart = Boxplot(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_KLINE:
            echart = Kline(**style.init_style)

        elif echarts_type == ECHARTS_TYPE_TIMELINE:
            echart = Timeline(**x_option)

        elif echarts_type == ECHARTS_TYPE_OVERLAp:
            echart = Overlap(**option)

        elif echarts_type == ECHARTS_TYPE_GRID:
            echart = Grid(**option)

        elif echarts_type == ECHARTS_TYPE_PAGE:
            echart = Page()

        if not echart:
            return copy.deepcopy(DEMO)
        # page.add(echart)
        return echart.options

    def get_echarts_datas(self, name=None, chart=None, echarts_type=None, xfield=None, yfields=None):
        result_list = []
        return result_list

    def get_echarts_response(self, request=None, name=None, **kwargs):
        if name not in self.echarts_charts:
            return HttpResponseNotFound()
        self.chart = self.echarts_charts[name]
        echarts_type = self.get_echarts_type(self.chart)
        logger.info(u"name:{} echarts_type:{} self.chart:{}".format(name, echarts_type, self.chart))

        xfield = self.chart['x-field']
        yfields = self.chart['y-field']
        yfields = (yfields,) if not isinstance(yfields, (list, tuple)) else yfields

        datas = self.get_echarts_datas(
            name=name,
            chart=self.chart,
            echarts_type=echarts_type,
            xfield=xfield,
            yfields=yfields,
        )

        content = self.get_echarts_options(
            name=name,
            chart=self.chart,
            echarts_type=echarts_type,
            xfield=xfield,
            yfields=yfields,
            datas=datas,
        )

        result = json.dumps(content, cls=JSONEncoder, ensure_ascii=False)
        logger.info(u"option:{}".format(result))
        return HttpResponse(result)


