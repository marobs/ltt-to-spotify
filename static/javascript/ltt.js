let $leftCol = $('#left-col');
let midCol = document.getElementById('middle-col');
let $midCol = $(midCol);
let rightCol = document.getElementById('right-col');
let $rightCol = $(rightCol);

let selectedPlaylist = null;
let switchPlaylistRequest = null;

let dragIndex = -1;

let playlists = {};

const ADD_ENDPOINT = '/add';
const REORDER_ENDPOINT = '/reorder';

function AddOptions(uris, position, playlist) {
    this.uris = uris;
    this.position = position;
    this.playlist = playlist;
}

function ReorderOptions(range_start, insert_before, playlist) {
    this.range_start = range_start;
    this.range_length = 1;
    this.insert_before = insert_before;
    this.playlist = playlist
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

function getPlaylistInfo(playlistName) {
    return new Promise((resolve, reject) => {
        $.get('/playlist', { "playlist": playlistName })
        .done((response) => {
            playlists[playlistName] = response;
            resolve(response);
        }).fail((e) => {
            console.error(e);
            reject(e);
        });
    });
}

dragula([midCol, rightCol], {
    copy: (el, source) => {
        return source === rightCol
    },
    copySortSource: false,
    accepts: (el, target) => {
        return target === midCol
    }
}).on('drop', (el, target, source) => {
    if (target === midCol) {
        let $el = $(el);
        // Make call to serve to reorder tracks on playlist
        // Requires: range_start, range_length (1), insert_before, snapshot_id (on server? Is optional)

        if (dragIndex === -1 && source === rightCol) { // Add Song
            let options = new AddOptions(ADD_ENDPOINT, $midCol.children($el).index($el), selectedPlaylist);
            sendEndpointRequest(ADD_ENDPOINT, options)
            .catch((e) => {
                // TODO: something with error?
                // Handle error
            });
        }
        else if (dragIndex >= 0 && source === midCol) { // Re-order Song
            let options = new ReorderOptions(dragIndex, $midCol.children($el).index($el), selectedPlaylist);
            sendEndpointRequest(REORDER_ENDPOINT, options)
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
    let playlistName = $leftCol.find('.selected')[0].innerHTML;
    selectedPlaylist = playlistName;
    playlists[playlistName] = $midCol[0].innerHTML;
};


// Event handlers
$leftCol.on('click', '.playlist', function(e) {
    let selected = $leftCol.find('.selected');
    let newSelected = $(e.target);

    if (selected === newSelected) {
        return;
    }

    selected.removeClass('selected');
    newSelected.addClass('selected');

    let playlistName = newSelected.innerHTML;

    if (playlistName in playlists && playlists[playlistName] !== 'undefined') {
        // Playlist information cached, set html
        $midCol[0].innerHTML = playlists[playlistName];
    }
    else {
        // No playlist information cached, make request on server
        let requestPromise = getPlaylistInfo(playlistName);
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