(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

var $leftCol = $('#left-col');
var midCol = document.getElementById('middle-col');
var $midCol = $(midCol);
var rightColTracks = document.getElementsByClassName('rt-track-container');
var $rightColTracks = $(rightColTracks);
var rightCol = document.getElementById('right-col');
var $rightCol = $(rightCol);

var dragulaElements = Object.keys(rightColTracks).map(function (key) {
    return rightColTracks[key];
});
dragulaElements.push(midCol);

var playlists = [];
var selectedPlaylist = null;
var switchPlaylistRequest = null;

var switchRedditCategoryRequest = null;

var dragIndex = -1;

var ADD_URL = '/ltt/addTrack';
var REORDER_URL = '/ltt/reorder';
var PLAYLIST_URL = '/ltt/playlist';

function AddOptions(uris, position, playlist) {
    this.uris = uris;
    this.position = position;
    this.playlist = playlist;
}

function ReorderOptions(range_start, insert_before, playlist) {
    this.range_start = range_start;
    this.range_length = 1;
    this.insert_before = insert_before;
    this.playlist = playlist;
}

function sendEndpointRequest(url, options) {
    return new Promise(function (resolve, reject) {
        $.post(url, options).done(function (response) {
            resolve(response);
        }).fail(function (e) {
            console.error(e);
            reject(e);
        });
    });
}

function getPlaylistInfo(playlistName) {
    return new Promise(function (resolve, reject) {
        $.get(PLAYLIST_URL, { "playlist": playlistName }).done(function (response) {
            playlists[playlistName] = response;
            resolve(response);
        }).fail(function (e) {
            console.error(e);
            reject(e);
        });
    });
}

function getCategoryTracks(category) {
    return new Promise(function (resolve, reject) {
        $.get(REDDIT_CATEGORY_URL, { category: category }).done(function (response) {
            var expirationTime = 10; // Minutes
            if (newCateogry === 'new') {
                expirationTime = 2; // Minutes
            }
            lscache.set(newCategory, response, expirationTime);

            resolve(response);
        }).fail(function (e) {
            console.error(e);
            reject(e);
        });
    });
}

dragula(dragulaElements, {
    copy: function copy(el, source) {
        console.log(source);
        console.log($(source));
        console.log($(source).hasClass('rt-track-container'));
        return $(source).hasClass('rt-track-container');
    },
    copySortSource: false,
    accepts: function accepts(el, target) {
        return target === midCol;
    }
}).on('drop', function (el, target, source) {
    if (target === midCol) {
        var $el = $(el);
        // Make call to serve to reorder tracks on playlist
        // Requires: range_start, range_length (1), insert_before, snapshot_id (on server? Is optional)

        if (dragIndex === -1 && $(source).hasClass('rt-track-container')) {
            // Add Song
            var options = new AddOptions(ADD_URL, $midCol.children($el).index($el), selectedPlaylist);
            sendEndpointRequest(ADD_URL, options).catch(function (e) {
                // TODO: something with error?
                // Handle error
            });
        } else if (dragIndex >= 0 && source === midCol) {
            // Re-order Song
            var _options = new ReorderOptions(dragIndex, $midCol.children($el).index($el), selectedPlaylist);
            sendEndpointRequest(REORDER_URL, _options).catch(function (e) {
                // TODO: something with error?
                // Handle error
            });
        } else {
            // Error (either source doesn't match the dragIndex or dragIndex is less than -1)
        }
    }

    dragIndex = -1;
}).on('drag', function (el, source) {
    if (source === midCol) {
        var $el = $(el);
        dragIndex = $midCol.children($el).index($el);
    } else {
        dragIndex = -1;
    }
});

window.onload = function () {
    // Store playlist information
    var playlistName = $leftCol.find('.selected')[0].innerHTML;
    selectedPlaylist = playlistName;
    playlists[playlistName] = $midCol[0].innerHTML;
};

// Event handlers
$leftCol.on('click', '.playlist', function (e) {
    var selected = $leftCol.find('.selected');
    var newSelected = $(e.target);

    if (selected === newSelected) {
        return;
    }

    selected.removeClass('selected');
    newSelected.addClass('selected');

    // Updated cahced dom for this playlist
    var oldPlaylistName = selected[0].innerHTML;
    playlists[oldPlaylistName] = $midCol[0].innerHTML;

    var playlistName = newSelected[0].innerHTML;

    if (playlistName in playlists && playlists[playlistName] !== 'undefined') {
        // Playlist information cached, set html
        $midCol[0].innerHTML = playlists[playlistName];
    } else {
        // No playlist information cached, make request on server
        console.log("making request");
        var requestPromise = getPlaylistInfo(playlistName);
        switchPlaylistRequest = requestPromise;
        requestPromise.then(function (response) {
            if (requestPromise === switchPlaylistRequest) {
                $midCol[0].innerHTML = response;
            }
        }).catch(function (error) {
            // TODO: something with error?
            return;
        });
    }
});

$rightCol.on('click', '.rch-text', function (e) {
    var newSelected = $(e.target);
    var oldSelected = $('#right-col-header').find('.selected');

    if (newSelected === oldSelected) {
        return;
    }

    oldSelected.removeClass('selected');
    newSelected.addClass('selected');

    var newCategory = newSelected[0].innerHTML;

    // Always fetch if new
    var newCategoryHTML = lscache.get(newCategory);
    if (newCategoryHTML !== null && newCategoryHTML !== 'undefined') {
        $rightCol[0].innerHTML = newCategoryHTML;
    } else {
        var requestPromise = getCategoryTracks(newCategory);
        switchRedditCategoryRequest = requestPromise;
        requestPromise.then(function (response) {
            if (requestPromise === switchRedditCategoryRequest) {
                $rightCol[0].innerHTML = response;
            }
        }).catch(function (error) {
            // TODO: something with error?
            return;
        });
    }
});

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvanMvbHR0LmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7QUNBQSxJQUFJLFdBQVcsRUFBRSxXQUFGLENBQWY7QUFDQSxJQUFJLFNBQVMsU0FBUyxjQUFULENBQXdCLFlBQXhCLENBQWI7QUFDQSxJQUFJLFVBQVUsRUFBRSxNQUFGLENBQWQ7QUFDQSxJQUFJLGlCQUFpQixTQUFTLHNCQUFULENBQWdDLG9CQUFoQyxDQUFyQjtBQUNBLElBQUksa0JBQWtCLEVBQUUsY0FBRixDQUF0QjtBQUNBLElBQUksV0FBVyxTQUFTLGNBQVQsQ0FBd0IsV0FBeEIsQ0FBZjtBQUNBLElBQUksWUFBWSxFQUFFLFFBQUYsQ0FBaEI7O0FBRUEsSUFBSSxrQkFBa0IsT0FBTyxJQUFQLENBQVksY0FBWixFQUE0QixHQUE1QixDQUFnQyxVQUFVLEdBQVYsRUFBZTtBQUFFLFdBQU8sZUFBZSxHQUFmLENBQVA7QUFBNkIsQ0FBOUUsQ0FBdEI7QUFDQSxnQkFBZ0IsSUFBaEIsQ0FBcUIsTUFBckI7O0FBRUEsSUFBSSxZQUFZLEVBQWhCO0FBQ0EsSUFBSSxtQkFBbUIsSUFBdkI7QUFDQSxJQUFJLHdCQUF3QixJQUE1Qjs7QUFFQSxJQUFJLDhCQUE4QixJQUFsQzs7QUFFQSxJQUFJLFlBQVksQ0FBQyxDQUFqQjs7QUFHQSxJQUFNLFVBQVUsZUFBaEI7QUFDQSxJQUFNLGNBQWMsY0FBcEI7QUFDQSxJQUFNLGVBQWUsZUFBckI7O0FBRUEsU0FBUyxVQUFULENBQW9CLElBQXBCLEVBQTBCLFFBQTFCLEVBQW9DLFFBQXBDLEVBQThDO0FBQzFDLFNBQUssSUFBTCxHQUFZLElBQVo7QUFDQSxTQUFLLFFBQUwsR0FBZ0IsUUFBaEI7QUFDQSxTQUFLLFFBQUwsR0FBZ0IsUUFBaEI7QUFDSDs7QUFFRCxTQUFTLGNBQVQsQ0FBd0IsV0FBeEIsRUFBcUMsYUFBckMsRUFBb0QsUUFBcEQsRUFBOEQ7QUFDMUQs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LENBQXdCLFVBQXhCO0FBQ0EsZ0JBQVksUUFBWixDQUFxQixVQUFyQjs7QUFFQSxRQUFJLGNBQWMsWUFBWSxDQUFaLEVBQWUsU0FBakM7O0FBRUE7QUFDQSxRQUFJLGtCQUFrQixRQUFRLEdBQVIsQ0FBWSxXQUFaLENBQXRCO0FBQ0EsUUFBSSxvQkFBb0IsSUFBcEIsSUFBNEIsb0JBQW9CLFdBQXBELEVBQWlFO0FBQzdELGtCQUFVLENBQVYsRUFBYSxTQUFiLEdBQXlCLGVBQXpCO0FBQ0gsS0FGRCxNQUdLO0FBQ0QsWUFBSSxpQkFBaUIsa0JBQWtCLFdBQWxCLENBQXJCO0FBQ0Esc0NBQThCLGNBQTlCO0FBQ0EsdUJBQWUsSUFBZixDQUFvQixVQUFDLFFBQUQsRUFBYztBQUM5QixnQkFBSSxtQkFBbUIsMkJBQXZCLEVBQW9EO0FBQ2hELDBCQUFVLENBQVYsRUFBYSxTQUFiLEdBQXlCLFFBQXpCO0FBQ0g7QUFDSixTQUpELEVBSUcsS0FKSCxDQUlTLFVBQUMsS0FBRCxFQUFXO0FBQ2hCO0FBQ0E7QUFDSCxTQVBEO0FBUUg7QUFDSixDQTlCRCIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCJsZXQgJGxlZnRDb2wgPSAkKCcjbGVmdC1jb2wnKTtcbmxldCBtaWRDb2wgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbWlkZGxlLWNvbCcpO1xubGV0ICRtaWRDb2wgPSAkKG1pZENvbCk7XG5sZXQgcmlnaHRDb2xUcmFja3MgPSBkb2N1bWVudC5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKCdydC10cmFjay1jb250YWluZXInKTtcbmxldCAkcmlnaHRDb2xUcmFja3MgPSAkKHJpZ2h0Q29sVHJhY2tzKTtcbmxldCByaWdodENvbCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyaWdodC1jb2wnKTtcbmxldCAkcmlnaHRDb2wgPSAkKHJpZ2h0Q29sKTtcblxubGV0IGRyYWd1bGFFbGVtZW50cyA9IE9iamVjdC5rZXlzKHJpZ2h0Q29sVHJhY2tzKS5tYXAoZnVuY3Rpb24gKGtleSkgeyByZXR1cm4gcmlnaHRDb2xUcmFja3Nba2V5XTsgfSk7XG5kcmFndWxhRWxlbWVudHMucHVzaChtaWRDb2wpO1xuXG5sZXQgcGxheWxpc3RzID0gW107XG5sZXQgc2VsZWN0ZWRQbGF5bGlzdCA9IG51bGw7XG5sZXQgc3dpdGNoUGxheWxpc3RSZXF1ZXN0ID0gbnVsbDtcblxubGV0IHN3aXRjaFJlZGRpdENhdGVnb3J5UmVxdWVzdCA9IG51bGw7XG5cbmxldCBkcmFnSW5kZXggPSAtMTtcblxuXG5jb25zdCBBRERfVVJMID0gJy9sdHQvYWRkVHJhY2snO1xuY29uc3QgUkVPUkRFUl9VUkwgPSAnL2x0dC9yZW9yZGVyJztcbmNvbnN0IFBMQVlMSVNUX1VSTCA9ICcvbHR0L3BsYXlsaXN0JztcblxuZnVuY3Rpb24gQWRkT3B0aW9ucyh1cmlzLCBwb3NpdGlvbiwgcGxheWxpc3QpIHtcbiAgICB0aGlzLnVyaXMgPSB1cmlzO1xuICAgIHRoaXMucG9zaXRpb24gPSBwb3NpdGlvbjtcbiAgICB0aGlzLnBsYXlsaXN0ID0gcGxheWxpc3Q7XG59XG5cbmZ1bmN0aW9uIFJlb3JkZXJPcHRpb25zKHJhbmdlX3N0YXJ0LCBpbnNlcnRfYmVmb3JlLCBwbGF5bGlzdCkge1xuICAgIHRoaXMucmFuZ2Vfc3RhcnQgPSByYW5nZV9zdGFydDtcbiAgICB0aGlzLnJhbmdlX2xlbmd0aCA9IDE7XG4gICAgdGhpcy5pbnNlcnRfYmVmb3JlID0gaW5zZXJ0X2JlZm9yZTtcbiAgICB0aGlzLnBsYXlsaXN0ID0gcGxheWxpc3Q7XG59XG5cbmZ1bmN0aW9uIHNlbmRFbmRwb2ludFJlcXVlc3QodXJsLCBvcHRpb25zKSB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgICAgJC5wb3N0KHVybCwgb3B0aW9ucylcbiAgICAgICAgLmRvbmUoKHJlc3BvbnNlKSA9PiB7XG4gICAgICAgICAgICByZXNvbHZlKHJlc3BvbnNlKTtcbiAgICAgICAgfSkuZmFpbCgoZSkgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihlKTtcbiAgICAgICAgICAgIHJlamVjdChlKTtcbiAgICAgICAgfSk7XG4gICAgfSk7XG59XG5cbmZ1bmN0aW9uIGdldFBsYXlsaXN0SW5mbyhwbGF5bGlzdE5hbWUpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICAkLmdldChQTEFZTElTVF9VUkwsIHsgXCJwbGF5bGlzdFwiOiBwbGF5bGlzdE5hbWUgfSlcbiAgICAgICAgLmRvbmUoKHJlc3BvbnNlKSA9PiB7XG4gICAgICAgICAgICBwbGF5bGlzdHNbcGxheWxpc3ROYW1lXSA9IHJlc3BvbnNlO1xuICAgICAgICAgICAgcmVzb2x2ZShyZXNwb25zZSk7XG4gICAgICAgIH0pLmZhaWwoKGUpID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoZSk7XG4gICAgICAgICAgICByZWplY3QoZSk7XG4gICAgICAgIH0pO1xuICAgIH0pO1xufVxuXG5mdW5jdGlvbiBnZXRDYXRlZ29yeVRyYWNrcyhjYXRlZ29yeSkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgICQuZ2V0KFJFRERJVF9DQVRFR09SWV9VUkwsIHtjYXRlZ29yeTogY2F0ZWdvcnl9KVxuICAgICAgICAuZG9uZSgocmVzcG9uc2UpID0+IHtcbiAgICAgICAgICAgIGxldCBleHBpcmF0aW9uVGltZSA9IDEwOyAvLyBNaW51dGVzXG4gICAgICAgICAgICBpZiAobmV3Q2F0ZW9ncnkgPT09ICduZXcnKSB7XG4gICAgICAgICAgICAgICAgZXhwaXJhdGlvblRpbWUgPSAyOyAvLyBNaW51dGVzXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBsc2NhY2hlLnNldChuZXdDYXRlZ29yeSwgcmVzcG9uc2UsIGV4cGlyYXRpb25UaW1lKTtcblxuICAgICAgICAgICAgcmVzb2x2ZShyZXNwb25zZSk7XG4gICAgICAgIH0pLmZhaWwoKGUpID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoZSk7XG4gICAgICAgICAgICByZWplY3QoZSk7XG4gICAgICAgIH0pO1xuXG4gICAgfSk7XG59XG5cbmRyYWd1bGEoZHJhZ3VsYUVsZW1lbnRzLCB7XG4gICAgY29weTogKGVsLCBzb3VyY2UpID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coc291cmNlKTtcbiAgICAgICAgY29uc29sZS5sb2coJChzb3VyY2UpKTtcbiAgICAgICAgY29uc29sZS5sb2coJChzb3VyY2UpLmhhc0NsYXNzKCdydC10cmFjay1jb250YWluZXInKSk7XG4gICAgICAgIHJldHVybiAkKHNvdXJjZSkuaGFzQ2xhc3MoJ3J0LXRyYWNrLWNvbnRhaW5lcicpO1xuICAgIH0sXG4gICAgY29weVNvcnRTb3VyY2U6IGZhbHNlLFxuICAgIGFjY2VwdHM6IChlbCwgdGFyZ2V0KSA9PiB7XG4gICAgICAgIHJldHVybiB0YXJnZXQgPT09IG1pZENvbDtcbiAgICB9XG59KS5vbignZHJvcCcsIChlbCwgdGFyZ2V0LCBzb3VyY2UpID0+IHtcbiAgICBpZiAodGFyZ2V0ID09PSBtaWRDb2wpIHtcbiAgICAgICAgbGV0ICRlbCA9ICQoZWwpO1xuICAgICAgICAvLyBNYWtlIGNhbGwgdG8gc2VydmUgdG8gcmVvcmRlciB0cmFja3Mgb24gcGxheWxpc3RcbiAgICAgICAgLy8gUmVxdWlyZXM6IHJhbmdlX3N0YXJ0LCByYW5nZV9sZW5ndGggKDEpLCBpbnNlcnRfYmVmb3JlLCBzbmFwc2hvdF9pZCAob24gc2VydmVyPyBJcyBvcHRpb25hbClcblxuICAgICAgICBpZiAoZHJhZ0luZGV4ID09PSAtMSAmJiAkKHNvdXJjZSkuaGFzQ2xhc3MoJ3J0LXRyYWNrLWNvbnRhaW5lcicpKSB7IC8vIEFkZCBTb25nXG4gICAgICAgICAgICBsZXQgb3B0aW9ucyA9IG5ldyBBZGRPcHRpb25zKEFERF9VUkwsICRtaWRDb2wuY2hpbGRyZW4oJGVsKS5pbmRleCgkZWwpLCBzZWxlY3RlZFBsYXlsaXN0KTtcbiAgICAgICAgICAgIHNlbmRFbmRwb2ludFJlcXVlc3QoQUREX1VSTCwgb3B0aW9ucylcbiAgICAgICAgICAgIC5jYXRjaCgoZSkgPT4ge1xuICAgICAgICAgICAgICAgIC8vIFRPRE86IHNvbWV0aGluZyB3aXRoIGVycm9yP1xuICAgICAgICAgICAgICAgIC8vIEhhbmRsZSBlcnJvclxuICAgICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoZHJhZ0luZGV4ID49IDAgJiYgc291cmNlID09PSBtaWRDb2wpIHsgLy8gUmUtb3JkZXIgU29uZ1xuICAgICAgICAgICAgbGV0IG9wdGlvbnMgPSBuZXcgUmVvcmRlck9wdGlvbnMoZHJhZ0luZGV4LCAkbWlkQ29sLmNoaWxkcmVuKCRlbCkuaW5kZXgoJGVsKSwgc2VsZWN0ZWRQbGF5bGlzdCk7XG4gICAgICAgICAgICBzZW5kRW5kcG9pbnRSZXF1ZXN0KFJFT1JERVJfVVJMLCBvcHRpb25zKVxuICAgICAgICAgICAgLmNhdGNoKChlKSA9PiB7XG4gICAgICAgICAgICAgICAgLy8gVE9ETzogc29tZXRoaW5nIHdpdGggZXJyb3I/XG4gICAgICAgICAgICAgICAgLy8gSGFuZGxlIGVycm9yXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgIC8vIEVycm9yIChlaXRoZXIgc291cmNlIGRvZXNuJ3QgbWF0Y2ggdGhlIGRyYWdJbmRleCBvciBkcmFnSW5kZXggaXMgbGVzcyB0aGFuIC0xKVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgZHJhZ0luZGV4ID0gLTE7XG59KS5vbignZHJhZycsIChlbCwgc291cmNlKSA9PiB7XG4gICAgaWYgKHNvdXJjZSA9PT0gbWlkQ29sKSB7XG4gICAgICAgIGxldCAkZWwgPSAkKGVsKTtcbiAgICAgICAgZHJhZ0luZGV4ID0gJG1pZENvbC5jaGlsZHJlbigkZWwpLmluZGV4KCRlbCk7XG4gICAgfVxuICAgIGVsc2Uge1xuICAgICAgICBkcmFnSW5kZXggPSAtMTtcbiAgICB9XG59KTtcblxud2luZG93Lm9ubG9hZCA9ICgpID0+IHtcbiAgICAvLyBTdG9yZSBwbGF5bGlzdCBpbmZvcm1hdGlvblxuICAgIGxldCBwbGF5bGlzdE5hbWUgPSAkbGVmdENvbC5maW5kKCcuc2VsZWN0ZWQnKVswXS5pbm5lckhUTUw7XG4gICAgc2VsZWN0ZWRQbGF5bGlzdCA9IHBsYXlsaXN0TmFtZTtcbiAgICBwbGF5bGlzdHNbcGxheWxpc3ROYW1lXSA9ICRtaWRDb2xbMF0uaW5uZXJIVE1MO1xufTtcblxuXG4vLyBFdmVudCBoYW5kbGVyc1xuJGxlZnRDb2wub24oJ2NsaWNrJywgJy5wbGF5bGlzdCcsIGZ1bmN0aW9uKGUpIHtcbiAgICBsZXQgc2VsZWN0ZWQgPSAkbGVmdENvbC5maW5kKCcuc2VsZWN0ZWQnKTtcbiAgICBsZXQgbmV3U2VsZWN0ZWQgPSAkKGUudGFyZ2V0KTtcblxuICAgIGlmIChzZWxlY3RlZCA9PT0gbmV3U2VsZWN0ZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHNlbGVjdGVkLnJlbW92ZUNsYXNzKCdzZWxlY3RlZCcpO1xuICAgIG5ld1NlbGVjdGVkLmFkZENsYXNzKCdzZWxlY3RlZCcpO1xuXG4gICAgLy8gVXBkYXRlZCBjYWhjZWQgZG9tIGZvciB0aGlzIHBsYXlsaXN0XG4gICAgbGV0IG9sZFBsYXlsaXN0TmFtZSA9IHNlbGVjdGVkWzBdLmlubmVySFRNTDtcbiAgICBwbGF5bGlzdHNbb2xkUGxheWxpc3ROYW1lXSA9ICRtaWRDb2xbMF0uaW5uZXJIVE1MO1xuXG4gICAgbGV0IHBsYXlsaXN0TmFtZSA9IG5ld1NlbGVjdGVkWzBdLmlubmVySFRNTDtcblxuICAgIGlmIChwbGF5bGlzdE5hbWUgaW4gcGxheWxpc3RzICYmIHBsYXlsaXN0c1twbGF5bGlzdE5hbWVdICE9PSAndW5kZWZpbmVkJykge1xuICAgICAgICAvLyBQbGF5bGlzdCBpbmZvcm1hdGlvbiBjYWNoZWQsIHNldCBodG1sXG4gICAgICAgICRtaWRDb2xbMF0uaW5uZXJIVE1MID0gcGxheWxpc3RzW3BsYXlsaXN0TmFtZV07XG4gICAgfVxuICAgIGVsc2Uge1xuICAgICAgICAvLyBObyBwbGF5bGlzdCBpbmZvcm1hdGlvbiBjYWNoZWQsIG1ha2UgcmVxdWVzdCBvbiBzZXJ2ZXJcbiAgICAgICAgY29uc29sZS5sb2coXCJtYWtpbmcgcmVxdWVzdFwiKTtcbiAgICAgICAgbGV0IHJlcXVlc3RQcm9taXNlID0gZ2V0UGxheWxpc3RJbmZvKHBsYXlsaXN0TmFtZSk7XG4gICAgICAgIHN3aXRjaFBsYXlsaXN0UmVxdWVzdCA9IHJlcXVlc3RQcm9taXNlO1xuICAgICAgICByZXF1ZXN0UHJvbWlzZS50aGVuKChyZXNwb25zZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHJlcXVlc3RQcm9taXNlID09PSBzd2l0Y2hQbGF5bGlzdFJlcXVlc3QpIHtcbiAgICAgICAgICAgICAgICAkbWlkQ29sWzBdLmlubmVySFRNTCA9IHJlc3BvbnNlO1xuICAgICAgICAgICAgfVxuICAgICAgICB9KS5jYXRjaCgoZXJyb3IpID0+IHtcbiAgICAgICAgICAgIC8vIFRPRE86IHNvbWV0aGluZyB3aXRoIGVycm9yP1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9KTtcbiAgICB9XG59KTtcblxuJHJpZ2h0Q29sLm9uKCdjbGljaycsICcucmNoLXRleHQnLCBmdW5jdGlvbihlKSB7XG4gICAgbGV0IG5ld1NlbGVjdGVkID0gJChlLnRhcmdldCk7XG4gICAgbGV0IG9sZFNlbGVjdGVkID0gJCgnI3JpZ2h0LWNvbC1oZWFkZXInKS5maW5kKCcuc2VsZWN0ZWQnKTtcblxuICAgIGlmIChuZXdTZWxlY3RlZCA9PT0gb2xkU2VsZWN0ZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIG9sZFNlbGVjdGVkLnJlbW92ZUNsYXNzKCdzZWxlY3RlZCcpO1xuICAgIG5ld1NlbGVjdGVkLmFkZENsYXNzKCdzZWxlY3RlZCcpO1xuXG4gICAgbGV0IG5ld0NhdGVnb3J5ID0gbmV3U2VsZWN0ZWRbMF0uaW5uZXJIVE1MO1xuXG4gICAgLy8gQWx3YXlzIGZldGNoIGlmIG5ld1xuICAgIGxldCBuZXdDYXRlZ29yeUhUTUwgPSBsc2NhY2hlLmdldChuZXdDYXRlZ29yeSk7XG4gICAgaWYgKG5ld0NhdGVnb3J5SFRNTCAhPT0gbnVsbCAmJiBuZXdDYXRlZ29yeUhUTUwgIT09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgICRyaWdodENvbFswXS5pbm5lckhUTUwgPSBuZXdDYXRlZ29yeUhUTUw7XG4gICAgfVxuICAgIGVsc2Uge1xuICAgICAgICBsZXQgcmVxdWVzdFByb21pc2UgPSBnZXRDYXRlZ29yeVRyYWNrcyhuZXdDYXRlZ29yeSk7XG4gICAgICAgIHN3aXRjaFJlZGRpdENhdGVnb3J5UmVxdWVzdCA9IHJlcXVlc3RQcm9taXNlO1xuICAgICAgICByZXF1ZXN0UHJvbWlzZS50aGVuKChyZXNwb25zZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHJlcXVlc3RQcm9taXNlID09PSBzd2l0Y2hSZWRkaXRDYXRlZ29yeVJlcXVlc3QpIHtcbiAgICAgICAgICAgICAgICAkcmlnaHRDb2xbMF0uaW5uZXJIVE1MID0gcmVzcG9uc2U7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0pLmNhdGNoKChlcnJvcikgPT4ge1xuICAgICAgICAgICAgLy8gVE9ETzogc29tZXRoaW5nIHdpdGggZXJyb3I/XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH0pO1xuICAgIH1cbn0pO1xuIl19
