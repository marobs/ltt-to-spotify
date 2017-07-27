let $leftCol = $('#left-col');
let midCol = document.getElementById('middle-col');
let $midCol = $(midCol);
let spotifyTrackContainer = document.getElementById('spotify-track-container');
let $spotifyTrackContainer = $(spotifyTrackContainer);
let rightColTracks = document.getElementsByClassName('rt-track-container');
let $rightColTracks = $(rightColTracks);
let rightCol = document.getElementById('right-col');
let $rightCol = $(rightCol);

let windowInterval = -1;

let dragulaElements = Object.keys(rightColTracks).map(function (key) { return rightColTracks[key]; });
dragulaElements.push(spotifyTrackContainer);

let playlists = [];
let selectedPlaylist = null;
let switchPlaylistRequest = null;

let switchRedditCategoryRequest = null;

let currentPreviewHowl = null;
let currentPreviewElement = null;

let dragIndex = -1;


const ADD_URL = '/ltt/addTrack';
const REORDER_URL = '/ltt/reorder';
const PLAYLIST_URL = '/ltt/playlist';
const REDDIT_CATEGORY_URL = '/ltt/reddit';
const PREVIEW_URL = '/ltt/previewTrack';

function AddOptions(uris, position, playlist) {
    this.trackURI = uris;
    this.position = position-1;
    this.playlistId = playlist;
}

function ReorderOptions(range_start, insert_before, playlist) {
    this.rangeStart = range_start;
    this.rangeLength = 1;

    if (range_start <= insert_before) {
        this.insertBefore = insert_before+1;
    }
    else {
        this.insertBefore = insert_before;
    }

    this.playlistId = playlist;
}

function sendAddTrackRequest(options) {
    return new Promise((resolve, reject) => {
        $.post(ADD_URL, options)
        .done((response) => {
            resolve(response);
        }).fail((e) => {
            console.error(e);
            reject(e);
        });
    });
}

function sendReorderRequest(options) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: REORDER_URL,
            method: 'PUT',
            data: options
        }).done((response) => {
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
        return target === spotifyTrackContainer;
    }
}).on('drop', (el, target, source) => {
    if (target === spotifyTrackContainer) {
        let $el = $(el);
        // Make call to serve to reorder tracks on playlist
        // Requires: range_start, range_length (1), insert_before, snapshot_id (on server? Is optional)

        if (dragIndex === -1 && $(source).hasClass('rt-track-container')) { // Add Song
            let playlistId = $('#left-col').find('.selected').attr('data-playlistId');
            let trackURI = $el.attr('data-uri');
            let options = new AddOptions(trackURI, $spotifyTrackContainer.children($el).index($el), playlistId);
            sendAddTrackRequest(options)
            .catch((e) => {
                // TODO: something with error?
                // Handle error
            });
        }
        else if (dragIndex >= 0 && source === spotifyTrackContainer) { // Re-order Song
            let playlistId = $('#left-col').find('.selected').attr('data-playlistId');
            let options = new ReorderOptions(dragIndex, $spotifyTrackContainer.children($el).index($el), playlistId);
            sendReorderRequest(options)
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
    if (source === spotifyTrackContainer) {
        let $el = $(el);
        dragIndex = $spotifyTrackContainer.children($el).index($el);
    }
    else {
        dragIndex = -1;
    }
});

window.onload = () => {
    // Store playlist information
    let playlistId = $leftCol.find('.selected').attr('data-ownerId');
    playlists[playlistId] = $spotifyTrackContainer[0].innerHTML;

    $volumeContainer.find(".slider-left").css({width: "50%"});
    $volumeContainer.find('.slider-thumb').css({left: "50%"});
    $volumeContainer.find(".slider-right").css({width: "50%"});
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
    playlists[oldPlaylistId] = $spotifyTrackContainer[0].innerHTML;

    if (playlistId in playlists && playlists[playlistId] !== 'undefined') {
        // Playlist information cached, set html
        $spotifyTrackContainer[0].innerHTML = playlists[playlistId];
    }
    else {
        // No playlist information cached, make request on server
        let requestPromise = getPlaylistInfo(playlistId, ownerId);
        switchPlaylistRequest = requestPromise;
        requestPromise.then((response) => {
            if (requestPromise === switchPlaylistRequest) {
                $spotifyTrackContainer[0].innerHTML = response;
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

/*------------------------*/
/* Track Preview Handlers */
/*------------------------*/
$rightCol.on('click', '.rt-track-preview', function(e) {
    let $newPreview = $(e.target).closest('.rt-track-preview');
    $('#footer').removeClass('hidden');

    if (currentPreviewHowl === null) { // First time preview clicked
        currentPreviewHowl = new Howl({
            src: [$newPreview.attr('data-preview-url')],
            format: ['mp3'],
            volume: currentVolume/100,
            onload: function() {
                $newPreview.addClass('previewing');
            }
        });
        currentPreviewHowl.play();
        currentPreviewHowl.on('play', function() {
            windowInterval = setInterval(updateSeekBar, 50, currentPreviewHowl);
        });
        currentPreviewElement = $newPreview;
    }
    else if (currentPreviewElement[0] === $newPreview[0]) { // Pause
        if (currentPreviewHowl.playing()) {
            currentPreviewHowl.pause();
            clearInterval(windowInterval);
            windowInterval = -1;

            pauseRTPreview($newPreview);
            return;
        }

        playRTPreview($newPreview);
        currentPreviewHowl.play();
        updateSeekBar(currentPreviewHowl);
    }
    else { // Switch Tracks
        currentPreviewHowl.stop();
        resetRTPreview(currentPreviewElement);

        if (windowInterval !== -1) {
            clearInterval(windowInterval);
            windowInterval = -1;
        }

        currentPreviewHowl = new Howl({
            src: [$newPreview.attr('data-preview-url')],
            format: ['mp3'],
            volume: currentVolume/100,
            onload: function() {
                $newPreview.addClass('previewing');
            }
        });
        currentPreviewHowl.play();
        currentPreviewHowl.on('play', function() {
            updateSeekBar(currentPreviewHowl);
            windowInterval = setInterval(updateSeekBar, 50, currentPreviewHowl);
        });
        currentPreviewElement = $newPreview;
        playRTPreview($newPreview);
    }

});


function updateSeekBar(howl) {
    if (howl === null) {
        return;
    }
    if (howl.playing()) {
        let seek = howl.seek();
        let playPercent = (seek/30)*100;
        $seekContainer.find(".slider-left").css({width: playPercent+"%"});
        $seekContainer.find('.slider-thumb').css({left: playPercent+"%"});
        $seekContainer.find(".slider-right").css({width: (100-playPercent)+"%"});
    }
}

function pauseRTPreview($newPreview) {
    let computedStyle = window.getComputedStyle($newPreview[0]);
    $newPreview[0].style.backgroundPosition = computedStyle.getPropertyValue('background-position');
    $newPreview.removeClass('previewing');
}

function playRTPreview($newPreview) {
    let computedStyle = window.getComputedStyle($newPreview[0]);
    let backgroundPos = computedStyle.getPropertyValue('background-position');
    let percentToComplete = parseFloat(backgroundPos.split('%')[0]);
    let timeToComplete = parseFloat(30*percentToComplete/100);

    $newPreview[0].removeAttribute('style');
    $newPreview.addClass('previewing');
    $newPreview[0].style.backgroundPosition = 'left';
    $newPreview[0].style.transition = 'all '+timeToComplete+'s linear';
}

function updateRTPreview($newPreview) {
    $newPreview.removeClass('previewing');
    let curSeek = currentPreviewHowl.seek();
    let currentPercent = ((curSeek/30)*100).toFixed(2);
    $newPreview[0].style.transition = 'all 1s linear';
    $newPreview[0].style.backgroundPosition = (100-currentPercent)+'% 50%';
}

function resetRTPreview($oldPreview) {
    $oldPreview.removeClass('previewing');
    $oldPreview[0].style.transition = 'all 1s linear';
    $oldPreview[0].style.backgroundPosition = 'right';
}

document.body.onkeydown = function(e){
    if(e.keyCode === 32){
        e.preventDefault();
        if (currentPreviewHowl === null) {
            return;
        }

        if (currentPreviewHowl.playing()) {
            currentPreviewHowl.pause();
            clearInterval(windowInterval);
            pauseRTPreview(currentPreviewElement);
        }
        else {
            currentPreviewHowl.play();
            windowInterval = setInterval(updateSeekBar, 50, currentPreviewHowl);
            playRTPreview(currentPreviewElement);
        }
    }
};
