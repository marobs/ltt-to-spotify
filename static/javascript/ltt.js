/*
  2017-07-17 
*/

!function n(e,t,r){function o(c,l){if(!t[c]){if(!e[c]){var a="function"==typeof require&&require;if(!l&&a)return a(c,!0);if(i)return i(c,!0);var s=new Error("Cannot find module '"+c+"'");throw s.code="MODULE_NOT_FOUND",s}var u=t[c]={exports:{}};e[c][0].call(u.exports,function(n){var t=e[c][1][n];return o(t||n)},u,u.exports,n,e,t,r)}return t[c].exports}for(var i="function"==typeof require&&require,c=0;c<r.length;c++)o(r[c]);return o}({1:[function(n,e,t){"use strict";function r(n,e,t){this.uris=n,this.position=e,this.playlist=t}function o(n,e,t){this.range_start=n,this.range_length=1,this.insert_before=e,this.playlist=t}function i(n,e){return new Promise(function(t,r){$.post(n,e).done(function(n){t(n)}).fail(function(n){console.error(n),r(n)})})}function c(n){return new Promise(function(e,t){$.get(w,{playlist:n}).done(function(t){v[n]=t,e(t)}).fail(function(n){console.error(n),t(n)})})}function l(n){return new Promise(function(e,t){$.get(REDDIT_CATEGORY_URL,{category:n}).done(function(n){var t=10;"new"===newCateogry&&(t=2),lscache.set(newCategory,n,t),e(n)}).fail(function(n){console.error(n),t(n)})})}var a=$("#left-col"),s=document.getElementById("middle-col"),u=$(s),f=document.getElementsByClassName("rt-track-container"),d=($(f),document.getElementById("right-col")),h=$(d),g=Object.keys(f).map(function(n){return f[n]});g.push(s);var v=[],p=null,m=null,y=null,T=-1,w="/ltt/playlist";dragula(g,{copy:function(n,e){return console.log(e),console.log($(e)),console.log($(e).hasClass("rt-track-container")),$(e).hasClass("rt-track-container")},copySortSource:!1,accepts:function(n,e){return e===s}}).on("drop",function(n,e,t){if(e===s){var c=$(n);-1===T&&$(t).hasClass("rt-track-container")?i("/ltt/addTrack",new r("/ltt/addTrack",u.children(c).index(c),p)).catch(function(n){}):T>=0&&t===s&&i("/ltt/reorder",new o(T,u.children(c).index(c),p)).catch(function(n){})}T=-1}).on("drag",function(n,e){if(e===s){var t=$(n);T=u.children(t).index(t)}else T=-1}),window.onload=function(){var n=a.find(".selected")[0].innerHTML;p=n,v[n]=u[0].innerHTML},a.on("click",".playlist",function(n){var e=a.find(".selected"),t=$(n.target);if(e!==t){e.removeClass("selected"),t.addClass("selected");var r=e[0].innerHTML;v[r]=u[0].innerHTML;var o=t[0].innerHTML;if(o in v&&"undefined"!==v[o])u[0].innerHTML=v[o];else{console.log("making request");var i=c(o);m=i,i.then(function(n){i===m&&(u[0].innerHTML=n)}).catch(function(n){})}}}),h.on("click",".rch-text",function(n){var e=$(n.target),t=$("#right-col-header").find(".selected");if(e!==t){t.removeClass("selected"),e.addClass("selected");var r=e[0].innerHTML,o=lscache.get(r);if(null!==o&&"undefined"!==o)h[0].innerHTML=o;else{var i=l(r);y=i,i.then(function(n){i===y&&(h[0].innerHTML=n)}).catch(function(n){})}}})},{}]},{},[1]);