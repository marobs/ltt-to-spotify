//
// CONST Variables
//
const GET_DATA_URL = '/playlists/data';

const playlistBatchSize = 20;

//
// Functionality
//

/**
 * @param {object|null} playlistData     Array of playlist data
 * @param playlistData.length            Built-in javascript length function...
 * @param playlistData.followers.total   Total number of followers of the playlist.
 * @param playlistData.totalLength       String representation of the duration of the playlist in X hr Y min
 */
function playlistBatchCallback(playlistData) {
    if (playlistData != null) {
        alert("Attempting to fill");
        console.log(playlistData);
        for (let dataIndex = 0; dataIndex < playlistData.length; dataIndex++) {
            let numFollowers = playlistData[dataIndex].followers.total;
            $("#" + playlistData[dataIndex].id + " .overlay-followers-text").text(numFollowers);

            let totalLength = playlistData[dataIndex].totalLength;
            $("#" + playlistData[dataIndex].id + " .overlay-length-text").text(totalLength);

            $("#" + playlistData[dataIndex].id).removeClass("incomplete");
        }
    }

    alert("Getting next");
    let nextIdPairBatch = getNextIdPairBatch();
    if (nextIdPairBatch.length > 0) {
        $.get(GET_DATA_URL, {'idPairList': JSON.stringify(nextIdPairBatch)})
            .done(function (data) {
                playlistBatchCallback(data);
            })
            .fail(function (data) {
                console.log(data);
            });
    }
}

function getNextIdPairBatch() {
    let remainingPlaylists = $(".incomplete");
    let batchSize = Math.min(remainingPlaylists.length, playlistBatchSize);
    let idPairList = [];
    for (let batchIndex = 0; batchIndex < batchSize; batchIndex++) {
        let playlistId = $(remainingPlaylists[batchIndex]).attr('id');
        let ownerId = $(remainingPlaylists[batchIndex]).data('owner-id');

        idPairList.push({'playlistId': playlistId, 'ownerId': ownerId});
    }

    return idPairList;
}

//
// On document ready
//
$(document).ready(function() {
    //playlistBatchCallback(null);
});