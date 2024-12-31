// ==UserScript==
// @name        免登录
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  try to take over the world!
// @author       ysl
// @match        https://mp.163.com/*
// @match        https://mp.sina.com.cn/*
// @match        https://www.sina.com.cn/
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @grant        GM_cookie
// @grant        GM_setClipboard
// ==/UserScript==




var verify = 1;






(function() {
    'use strict';
    GM_registerMenuCommand("发送登录信息", sendCookie, "h");
    // GM_registerMenuCommand("登录", login, "l");
})();

function sendCookie() {
    // GM_cookie("list", {damain:'.sina.com.cn'}, function(){
    GM_cookie("list", {url:window.location.href}, function(){
        // console.log(arguments)
        var cookie_json = JSON.stringify(arguments[0]);
        const data = {
            'url': window.location.href,
            'cookie': cookie_json
        }
        //console.log(cookie_json)
        //console.log(data)
        GM_xmlhttpRequest({
            method: "POST",
            url: 'http://xxxx.com/send_cookie',
            data: JSON.stringify(data),
            headers: { "Content-Type": "application/json" },
            onload: function(response){
                alert('已发送成功');
            }
        });
    });
}
