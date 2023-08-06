$(document).ready(function(){
    var echart = null;

    var resizeECharts = function(obj, refresh) {
        if (refresh && obj) {
            obj.resize();
        }
    };

    $.fn.chart = function(){
      $(this).each(function(){
        var $chart = $(this);
        var obj = $chart.data('chart-obj');
        var o = obj ? obj.getOption() : null;
        if (obj && o) {
            echart = obj;
            resizeECharts(echart, true);
            return;
        }
        var echarts_o = echarts.init(this, 'vintage', {width: "auto", height: "auto"});
        echarts_o.showLoading();
        $.getJSON($chart.data('chart-url'), function(data){
            echarts_o.hideLoading();
            echarts_o.setOption(data);
            $chart.data('chart-obj', echarts_o);
        });
        echart = echarts_o;
      })
    };

    $('.chart-tab a').click(function(e){
      e.preventDefault();
      $(this).tab('show');
      $($(this).attr('href')).chart();
    });
    $('.chart-tab a:first').click();
    $('.chart.init').chart();

    window.onresize = function () {
        resizeECharts(echart, true);
    };
});