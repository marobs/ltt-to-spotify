let $leftCol = $('#left-col');
let midCol = document.getElementById('middle-col');
let $midCol = $(midCol);
let rightColTracks = document.getElementsByClassName('rt-track-container');
let $rightColTracks = $(rightColTracks);
let rightCol = document.getElementById('right-col');
let $rightCol = $(rightCol);

let dragulaElements = Object.keys(rightColTracks).map(function (key) { return rightColTracks[key]; });
dragulaElements.push(midCol);

let playlists = [];
let selectedPlaylist = null;
let switchPlaylistRequest = null;

let switchRedditCategoryRequest = null;

let dragIndex = -1;


const ADD_URL = '/ltt/addTrack';
const REORDER_URL = '/ltt/reorder';
const PLAYLIST_URL = '/ltt/playlist';

function AddOptions(uris, position, playlist) {
    this.trackURI = uris;
    this.position = position-1;
    this.playlistId = playlist;
}

function ReorderOptions(range_start, insert_before, playlist) {
    this.range_start = range_start;
    this.range_length = 1;
    this.insert_before = insert_before;
    this.playlist = playlist;
}

function sendEndpointRequest(url, options) {
    return new Promise((resolve, reject) => {
        $.post(url, options)
        .done((response) => {
            resolve(response);
        }).fail((e) => {
            console.error(e);
            reject(e);
        });
    });
}

function getPlaylistInfo(playlistId, ownerId) {
    return new Promise((resolve, reject) => {
        $.get(PLAYLIST_URL, { 'playlistId': playlistId, 'userId': ownerId })
        .done((response) => {
            playlists[playlistId] = response;
            resolve(response);
        }).fail((e) => {
            console.error(e);
            reject(e);
        });
    });
}

function getCategoryTracks(category) {
    return new Promise((resolve, reject) => {
        $.get(REDDIT_CATEGORY_URL, {category: category})
        .done((response) => {
            let expirationTime = 10; // Minutes
            if (newCateogry === 'new') {
                expirationTime = 2; // Minutes
            }
            lscache.set(newCategory, response, expirationTime);

            resolve(response);
        }).fail((e) => {
            console.error(e);
            reject(e);
        });

    });
}

dragula(dragulaElements, {
    copy: (el, source) => {
        return $(source).hasClass('rt-track-container');
    },
    copySortSource: false,
    accepts: (el, target) => {
        return target === midCol;
    }
}).on('drop', (el, target, source) => {
    if (target === midCol) {
        let $el = $(el);
        // Make call to serve to reorder tracks on playlist
        // Requires: range_start, range_length (1), insert_before, snapshot_id (on server? Is optional)

        if (dragIndex === -1 && $(source).hasClass('rt-track-container')) { // Add Song
            let playlistId = $('#left-col').find('.selected').attr('data-playlistId');
            let trackURI = $el.attr('data-uri');
            let options = new AddOptions(trackURI, $midCol.children($el).index($el), playlistId);
            sendEndpointRequest(ADD_URL, options)
            .catch((e) => {
                // TODO: something with error?
                // Handle error
            });
        }
        else if (dragIndex >= 0 && source === midCol) { // Re-order Song
            let playlistId = $('#left-col').find('.selected').attr('data-playlistId');
            let options = new ReorderOptions(dragIndex, $midCol.children($el).index($el), playlistId);
            sendEndpointRequest(REORDER_URL, options)
            .catch((e) => {
                // TODO: something with error?
                // Handle error
            });
        }
        else {
            // Error (either source doesn't match the dragIndex or dragIndex is less than -1)
        }
    }

    dragIndex = -1;
}).on('drag', (el, source) => {
    if (source === midCol) {
        let $el = $(el);
        dragIndex = $midCol.children($el).index($el);
    }
    else {
        dragIndex = -1;
    }
});

window.onload = () => {
    // Store playlist information
    let playlistId = $leftCol.find('.selected').attr('data-ownerId');
    playlists[playlistId] = $midCol[0].innerHTML;
};


// Event handlers
$leftCol.on('click', '.playlist', function(e) {
    let selected = $leftCol.find('.selected');
    let newSelected = $(e.target);
    let playlistId = newSelected.attr('data-playlistId');
    let ownerId = newSelected.attr('data-ownerId');

    if (selected === newSelected) {
        return;
    }

    selected.removeClass('selected');
    newSelected.addClass('selected');

    // Updated cahced dom for this playlist
    let oldPlaylistId = selected.attr('data-playlistId');
    playlists[oldPlaylistId] = $midCol[0].innerHTML;

    if (playlistId in playlists && playlists[playlistId] !== 'undefined') {
        // Playlist information cached, set html
        $midCol[0].innerHTML = playlists[playlistId];
    }
    else {
        // No playlist information cached, make request on server
        let requestPromise = getPlaylistInfo(playlistId, ownerId);
        switchPlaylistRequest = requestPromise;
        requestPromise.then((response) => {
            if (requestPromise === switchPlaylistRequest) {
                $midCol[0].innerHTML = response;
            }
        }).catch((error) => {
            // TODO: something with error?
            return;
        });
    }
});

$rightCol.on('click', '.rch-text', function(e) {
    let newSelected = $(e.target);
    let oldSelected = $('#right-col-header').find('.selected');

    if (newSelected === oldSelected) {
        return;
    }

    oldSelected.removeClass('selected');
    newSelected.addClass('selected');

    let newCategory = newSelected[0].innerHTML;

    // Always fetch if new
    let newCategoryHTML = lscache.get(newCategory);
    if (newCategoryHTML !== null && newCategoryHTML !== 'undefined') {
        $rightCol[0].innerHTML = newCategoryHTML;
    }
    else {
        let requestPromise = getCategoryTracks(newCategory);
        switchRedditCategoryRequest = requestPromise;
        requestPromise.then((response) => {
            if (requestPromise === switchRedditCategoryRequest) {
                $rightCol[0].innerHTML = response;
            }
        }).catch((error) => {
            // TODO: something with error?
            return;
        });
    }
});
