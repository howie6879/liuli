"""
    Created by howie.hu at 2021-12-20.
    Description: 基于 微信搜狗搜索 进行公众号最新文章获取
        Home: https://weixin.sogou.com/
        Solution: https://playwright.dev/python/docs/intro
    Changelog: all notable changes to this file will be documented
"""

demo = """

<head>
    <link rel="shortcut icon" href="//www.sogou.com/images/logo/new/favicon.ico?v=4" type="image/x-icon">
    <link href="//dlweb.sogoucdn.com/logo/images/2018/apple-touch-icon.png" id="apple-touch-icon" rel="apple-touch-icon-precomposed">
    <link href="//www.sogou.com/sug/css/m3.min.v.7.css" rel="stylesheet" type="text/css">
    <link href="/new/pc/css/weixin-public-new.min.css?v=20190822" rel="stylesheet" type="text/css">
    
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="Access-Control-Allow-Origin" content="*">
    <meta content="width=device-width,initial-scale=1.0" id="vp" name="viewport">
    <title>小众消息的相关微信公众号 – 搜狗微信搜索</title>
    
    <script>
        var sst = {h_s :(new Date()).getTime()};
        var newpage = 1;
        var passportUserId = "";
        var oldQuery = "小众消息";
        var gbkQuery = "%D0%A1%D6%DA%CF%FB%CF%A2";
        var uuid = "a5c739d6-b5d4-44ba-8111-1f477552929a";
        var keywords_string = "小众消息";
        var sab = "6";
        var keywords = oldQuery.split(' ');
        var now = 1639993357303;
        var idc = "sjs";
        var clientIp = "117.28.113.193";
        var isIpad = false;
        //var article_anti_url = "";
        var  ssToken = "CA9DD7534FFE92FB8F8B5D1F3AF03C588F91490761C0500D";
    </script>
    <script>
        //以下为动态的全局 js，防止外部网站通过 window.opener.location 篡改我们的页面，以后不要通过 window.location 获取当前地址，只能用 document.location
        
    </script>
    <script src="/js/jquery-1.11.0.min.js" charset="gbk"></script>
    <script src="/new/pc/js/https_util.min.js?v=20180607"></script>
    <script src="/js/lib/juicer-min.js"></script>
    <script src="/new/weixin/js/common.min.js?v=20200414"></script>
    <script src="/new/pc/js/common.min.js?v=20180607"></script>
    
    <script>
        var uigs_para = {
            "uigs_t": "1639993357303",
            "uigs_productid": "vs_web",
            "terminal"      : "web",
            "vstype"        : "weixin",
            "pagetype"      : "result",
            "channel"       : "result_account",
            "s_from"        : "input",
            "sourceid"      : "",
            "type"          : "weixin_search_pc",
            "uigs_cookie"   : "SUID,sct",
            "uuid"          : "a5c739d6-b5d4-44ba-8111-1f477552929a",
            "query"         : "小众消息",
            "weixintype"    : "1",
            "exp_status"    : "-1",
            "exp_id_list"   : "0_0",
            "wuid"          : "004324AA751C715861C0500D54AED165",
            "snuid"         : "4FFE92FB8F8B5D1F3AF03C588F914907",
            "rn"            : 1,
            "login"         : passportUserId ? "1" : "0",
            "uphint"        : 0,
            "bottomhint"    : 0,
            "page"          : "1"
        };
        $.get('/approve?uuid=' + window.uigs_para.uuid + '&token=' + "CA9DD7534FFE92FB8F8B5D1F3AF03C588F91490761C0500D" + '&from=search');
    </script>
</head>
<body style="">
    

<!--start header-->
<div class="header-box" style="height: 86px;">
    
    <div class="login-info">
        <a href="javascript:void(0)" id="cniil_wza" style="text-decoration: none;color: #999;padding-right: 20px;border-right: 1px solid #e7e7e7;line-height: 14px;margin-right: 20px;">无障碍</a>
        <a id="top_login" href="javascript:void(0);" uigs="home_login_top">登录</a>
    </div>

<style id="loginStyle" type="text/css">
    .login-skin{position: fixed;_position: absolute;top:0;left:0;width: 100%;height: 100%;_height:expression(document.body.scrollHeight+"px");z-index: 2100;background-color: #000;opacity:0.4;filter:alpha(opacity=40);}.login-pop-wx{background-color: #fff;border: 1px solid #ebebeb;width: 510px;height: 420px;position:fixed;_position: absolute;margin-left:-225px;left: 50%;top: 200px;_top:expression(document.documentElement.scrollTop+200+"px");font-family: Microsoft YaHei;z-index: 2200;}}
</style>
<div class="login-skin" style="display: none"></div>
<script src="/new/pc/js/login.min.js?v=20170315"></script>
    <div class="header" id="scroll-header">
        <a title="回到搜狗首页" href="/" name="scroll-nav" class="logo" uigs="home"></a>
        <ul class="searchnav" name="scroll-nav">
            <li><a id="sogou_xinwen" href="https://www.sogou.com/sogou?ie=utf8&amp;p=40230447&amp;interation=1728053249&amp;interV=&amp;pid=sogou-wsse-7050094b04fd9aa3&amp;query=小众消息" onclick="navBar(this,'query=');" uigs="nav_xinwen">资讯</a></li>
            <li><a id="sogou_wangye" href="http://www.sogou.com/web?ie=utf8&amp;query=小众消息" onclick="navBar(this,'query=');" uigs="nav_wangye">网页</a></li>
            <li class="cur"><a href="javascript:void(0)">微信</a></li>
            <li><a id="sogou_zhihu" href="http://zhihu.sogou.com/zhihu?ie=utf8&amp;p=73351201&amp;query=小众消息" onclick="navBar(this,'query=')" uigs="nav_zhihu">知乎</a></li>
            <li><a id="sogou_tupian" href="http://pic.sogou.com/pics?ie=utf8&amp;p=40230504&amp;query=小众消息" onclick="navBar(this,'query=')" uigs="nav_tupian">图片</a></li>
            <li><a id="sogou_shipin" href="https://v.sogou.com/v?ie=utf8&amp;p=40230608&amp;query=小众消息" onclick="navBar(this,'query=')" uigs="nav_shipin">视频</a></li>
            <li><a id="sogou_mingyi" href="https://www.sogou.com/web?m2web=mingyi.sogou.com&amp;ie=utf8&amp;query=小众消息" onclick="navBar(this,'query=')" uigs="nav_mingyi">医疗</a></li>
            <li><a id="sogou_science" href="http://baike.sogou.com/kexue/home.htm?query=小众消息" onclick="navBar(this,'query=')" uigs="nav_science">科学</a></li>
            <li><a id="sogou_yingwen" href="http://english.sogou.com/english?b_o_e=1&amp;ie=utf8&amp;query=小众消息" onclick="navBar(this,'query=')" uigs="nav_yingwen">英文</a></li>
            <li><a id="sogou_wenwen" href="http://wenwen.sogou.com/s/?ch=weixinsearch&amp;w=小众消息" data-index="http://wenwen.sogou.com/?ch=weixinsearch" onclick="navBar(this,'w=')" uigs="nav_wenwen">问问</a></li>
            <li><a id="sogou_xueshu" href="http://scholar.sogou.com/xueshu?ie=utf-8&amp;query=小众消息" onclick="navBar(this,'query=')" uigs="nav_xueshu">学术</a></li>
            <li><a id="top_more" href="http://www.sogou.com/docs/more.htm?v=1" target="_blank" uigs="nav_more">更多&gt;&gt;</a></li>
        </ul>
        

<form name="searchForm" action="/weixin">
    <div class="querybox">
        <div class="qborder">
            <div class="qborder2">
                <input type="hidden" name="type" value="1">
                <input type="hidden" name="s_from" value="input">
                <input type="text" class="query" name="query" id="query" ov="小众消息" value="小众消息" autocomplete="off">
                
                    <input type="hidden" name="ie" value="utf8">
                
                <a href="javascript:void(0)" class="qreset2" name="reset" uigs="search_reset"></a>
            </div>
        </div>
        <input type="button" value="搜文章" class="swz" onclick="search(this,2)" uigs="search_article">
        <input type="button" value="搜公众号" class="swz2" onclick="search(this,1)" uigs="search_account">
        <input type="hidden" name="_sug_" value="n">
        <input type="hidden" name="_sug_type_" value="">
    </div>
</form>
    </div>
</div>
<!--end header-->
    
    <div class="wrapper" id="wrapper">
        <div class="main-left" id="main">
            
<div class="dy-pop2 dy-pop5 float" id="erweima_box" style="display: none"></div>
<script type="text/template" id="erweima_tpl">
    <a href="javascript:void(0)" class="close" data-except="1" uigs="other_float_weixin_close"></a>
    <div class="fxico-box2">微信扫一扫关注<br/><img width="104" height="104" src="${imgsrc}"/></div>
</script>
            

<script>
    //高级工具参数对象
    var toolParas = {
        tsn : '0',
        ft : '',
        et : '',
        interation : '',
        wxid : '',
        usip : ''
    };
    var from_tool = '0';
</script>
<div class="wx-topbox">
    <div class="all-time">
        <div class="all-time-y2 ">
            <div class="all-time-y all-time-y-v1" id="text">
                以下内容来自微信公众号
            </div>
            
        </div>
    </div>
</div>




<div class="news-box">
    
<ul class="news-list2">

                <!-- a -->
                <li id="sogou_vr_11002301_box_0" d="oIWsFt86NKeSGd_BQKp1GcDkYpv0">
<div class="gzh-box2">
<div class="img-box">
<a target="_blank" uigs="account_image_0" href="/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqiHhcbzLjdISBg9JTvqEM2QwvDqyjOWdzQnIEQNy9nmMfkAlUinwjSOXOX1_8NXgxzVpwlB9lCZwi4YTSuMJU8DyB6_CzmEtDAKA2IJC6x8MQE2CNHg_ATNsmy_N7Q2LMX2ROIYsv4Fv4IYGBVNUO4-O00efWrWmm&amp;type=1&amp;query=%E5%B0%8F%E4%BC%97%E6%B6%88%E6%81%AF&amp;token=CA9DD7534FFE92FB8F8B5D1F3AF03C588F91490761C0500D"><span></span><img src="//img01.sogoucdn.com/app/a/100520090/oIWsFt86NKeSGd_BQKp1GcDkYpv0" onload="resizeImage(this,58,58)" onerror="errorHeadImage(this)" style="width: 58px; height: auto; margin-top: 0px;"></a>
</div>
<div class="txt-box">
<p class="tit">
<a target="_blank" uigs="account_name_0" href="/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqiHhcbzLjdISBg9JTvqEM2QwvDqyjOWdzQnIEQNy9nmMfkAlUinwjSOXOX1_8NXgxzVpwlB9lCZwi4YTSuMJU8DyB6_CzmEtDAKA2IJC6x8MQE2CNHg_ATNsmy_N7Q2LMX2ROIYsv4Fv4IYGBVNUO4-O00efWrWmm&amp;type=1&amp;query=%E5%B0%8F%E4%BC%97%E6%B6%88%E6%81%AF&amp;token=CA9DD7534FFE92FB8F8B5D1F3AF03C588F91490761C0500D"><em><!--red_beg-->小众消息<!--red_end--></em></a>
</p>
<p class="info">微信号：<label name="em_weixinhao">WebNotes</label>
<span class="line-s"></span>月发文&nbsp;18&nbsp;篇</p>
</div>
<div style="display:none;" class="pop-tip" data="/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqiHhcbzLjdISBg9JTvqEM2QwvDqyjOWdzQnIEQNy9nmMfkAlUinwjSOXOX1_8NXgxzVpwlB9lCZwi4YTSuMJU8DyB6_CzmEtDAKA2IJC6x8MQE2CNHg_ATNsmy_N7Q2LMX2ROIYsv4Fv4IYGBVNUO4-O00efWrWmm&amp;type=1&amp;query=小众消息&amp;token=CA9DD7534FFE92FB8F8B5D1F3AF03C588F91490761C0500D">
<p>查阅公众号的历史文章，建议前往微信客户端</p>
<p>温馨提示：点击右侧二维码标识并用微信扫一扫即可快速传送哦~</p>
</div>
<div class="ew-pop">
<a class="code" href="javascript:void(0)"><img height="24" width="24" src="/new/pc/images/ico_ewm.png"></a><span style="display:none;" class="pop"><i></i>微信扫一扫关注<br>
<img height="104" width="104" src="https://img04.sogoucdn.com/v2/thumb?t=2&amp;url=http%3A%2F%2Fmp.weixin.qq.com%2Frr%3Fsrc%3D3%26timestamp%3D1639993357%26ver%3D1%26signature%3D7lll1GaNdFG84H3EqqprJeZY65Da8ySy8Yga60Fipxy6J35DH1iETbgt1C-c1Bnywjm*skG3Xqg2TV08yCylkQRg7EQuZyASr4KkO15859M%3D&amp;appid=200580" data-id="oIWsFt86NKeSGd_BQKp1GcDkYpv0" onerror="qrcodeShowError('http://mp.weixin.qq.com/rr?src=3&amp;timestamp=1639993357&amp;ver=1&amp;signature=7lll1GaNdFG84H3EqqprJeZY65Da8ySy8Yga60Fipxy6J35DH1iETbgt1C-c1Bnywjm*skG3Xqg2TV08yCylkQRg7EQuZyASr4KkO15859M=',4,'oIWsFt86NKeSGd_BQKp1GcDkYpv0')"><img height="32" width="32" class="shot-img" src="//img01.sogoucdn.com/app/a/100520090/oIWsFt86NKeSGd_BQKp1GcDkYpv0" onerror="errorHeadImage(this)"></span>
</div>
</div>
<dl>
<dt>功能介绍：</dt>
<dd>有价值的<em><!--red_beg-->消息<!--red_end--></em>,常常是从<em><!--red_beg-->小众<!--red_end--></em>传播到大众.曾用名「小道<em><!--red_beg-->消息<!--red_end--></em>」,苦于总被误解.特此更名</dd>
</dl>
<dl>
<dt>
<script>document.write(authname('2'))</script>微信认证：</dt>
<dd>
<i class="identify"></i>冯大辉</dd>
</dl>
<dl>
<dt>最近文章：</dt>
<dd>
<a target="_blank" uigs="account_article_0" href="/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS24YF3-cyBXbhD-zqnjFqdsnlCA70ccHJ1qXa8Fplpd9ZF63AaN8W3CMkoFKMQCKp0qBiB72JqoYr2jheiQsiVkP11DLQZT-cVsSxPnJaeJgDEMXGrpCx43ygbOlF26a9mjHvWRI-iF0qlK9F5-qUc5iwqNFrCCjU8IggQ4Q9IBZetS765YFYCytfxYwoi3_2B1rX4WxFHtQHeuqmxqzg2xhlgeRt7bSzA..&amp;type=1&amp;query=%E5%B0%8F%E4%BC%97%E6%B6%88%E6%81%AF&amp;token=CA9DD7534FFE92FB8F8B5D1F3AF03C588F91490761C0500D">B 站是怎么赚钱的?</a><span><script>document.write(timeConvert('1639903911'))</script>1天前</span>
</dd>
</dl>
</li>

                <!-- z -->

</ul>
    
</div>


        </div>
        
            <script>var account_anti_url = "/websearch/weixin/pc/anti_account.jsp?t=1639993357300&signature=QAgnxSYRli6w2ponQosSsJVxQmKqXsdOfdQ0c2tTqVgRTkfNLl3zlrrC4ggE*GGHbforKAxTFNqHc*o2HCap7w==";</script>
        
    </div>
    <div class="back-top" style="display: none;"><a href="javascript:void(0);" uigs="other_float_back_top"></a></div>
    
    <div class="bottom-form">
        

<form name="searchForm" action="/weixin">
    <div class="querybox">
        <div class="qborder">
            <div class="qborder2">
                <input type="hidden" name="type" value="1">
                <input type="hidden" name="s_from" value="input">
                <input type="text" class="query" name="query" id="query_bottom" ov="小众消息" value="小众消息" autocomplete="off">
                
                    <input type="hidden" name="ie" value="utf8">
                
                <a href="javascript:void(0)" class="qreset2" name="reset" uigs="search_reset"></a>
            </div>
        </div>
        <input type="button" value="搜文章" class="swz" onclick="search(this,2)" uigs="search_article">
        <input type="button" value="搜公众号" class="swz2" onclick="search(this,1)" uigs="search_account">
        <input type="hidden" name="_sug_" value="n">
        <input type="hidden" name="_sug_type_" value="">
    </div>
</form>
    </div>

<div class="footer-box" id="s_footer">
    <div class="footer">
        <a id="sogou_webhelp" href="http://help.sogou.com/" target="_blank" uigs="bottom_ssbz">搜索帮助</a><a href="http://mp.weixin.qq.com/profile?src=3&amp;timestamp=1639993357&amp;ver=1&amp;signature=baOLTxelfBmfpqmkaSGFLCQK4LzlS5kKa3qu*wYyzCHr-tPiMoFUdyzQRu46hUCtqvoLxjPogJNJGtLn6LnWjQ==" target="_blank" data-uigs="bottom_gfwx">官方微信</a>&nbsp;<a href="http://fankui.help.sogou.com/index.php/web/web/index/type/4" target="_blank" uigs="bottom_yjfk">意见反馈及投诉</a>&nbsp;<script src="/websearch/wexinurlenc_sogou_profile.jsp"></script>©&nbsp;2021&nbsp;SOGOU.COM&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://www.sogou.com/docs/terms.htm" target="_blank" uigs="bottom_mzsm">免责声明</a>&nbsp;<a href="http://corp.sogou.com/private.html" target="_blank" uigs="bottom_yszc">隐私政策</a>
    </div>
</div>
    
        <script src="/new/pc/js/account.min.js?v=20190822"></script>
    
    <script>
        var WX_SUGG_PAGE_FROM="pcGzhSearch";
        
        var SugPara = {
            "bigsize":true,
            "enableSug":true,
            "sugType":"wxpub",
            "domain":"w.sugg.sogou.com",
            "productId":"web",
            "sugFormName":"sf",
            "submitId":"stb",
            "suggestRid":"01015002",
            "normalRid":"01019900",
            "oms":1,
            "nofixwidth":1,
            "useParent":1
        };
        uigs_para.exp_id = "null_0-";
        uigs_para.exp_id = uigs_para.exp_id.substring(0, uigs_para.exp_id.length - 1);
    </script>
    <script src="/new/weixin/js/uigs.min.js?v=20180607"></script>
    <script src="/new/pc/js/log.min.js?v=20170321"></script>
    <script src="/new/pc/js/event.min.js?v=20190822"></script>
    <script src="/new/pc/js/search.min.js?v=20161107"></script>
    <script src="/new/pc/js/suggestion.min.js?v=20200702"></script><script charset="gb2312" src="/sugg/ajaj_json.jsp?type=getpinyin&amp;key=%E5%B0%8F%E4%BC%97%E6%B6%88%E6%81%AF&amp;cb=window.sogou.sugpy"></script>
    <script src="/new/weixin/js/form.min.js?v=20170101"></script>
    <script src="//dlweb.sogoucdn.com/hhytrace/trace_2021122017.js"></script>
    

<script>
    (function(){$("a").on("mousedown click contextmenu",function(){var b=Math.floor(100*Math.random())+1,a=this.href.indexOf("url="),c=this.href.indexOf("&k=");-1!==a&&-1===c&&(a=this.href.substr(a+4+parseInt("21")+b,1),this.href+="&k="+b+"&h="+a)})})();
</script>

    <script defer="" async="" type="text/javascript" src="//dlweb.sogoucdn.com/barrier_free/pc/wzaV6/aria.js?appid=c4d5562ec7daa12a5a351cbe1a292da1" charset="utf-8"></script>


<!--1639993357303-->
<!--zly--><!--weixin-->
</body>
"""
