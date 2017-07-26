//
// CONST Variables
//
const GET_DATA_URL = '/playlists/data';
const GET_OWNERS_URL = '/playlists/owners';

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
function playlistBatchCallback(playlistData, batchSize) {
    if (playlistData != null) {
        console.log(playlistData);
        for (let dataIndex = 0; dataIndex < playlistData.length; dataIndex++) {
            let numFollowers = playlistData[dataIndex].followers.total;
            $("#" + playlistData[dataIndex].id + " .overlay-followers-text").text(numFollowers);

            let totalLength = playlistData[dataIndex].totalLength;
            $("#" + playlistData[dataIndex].id + " .overlay-length-text").text(totalLength);

            $("#" + playlistData[dataIndex].id).removeClass("incomplete");
        }
    }

    let nextIdPairBatch = getNextIdPairBatch(batchSize);
    if (nextIdPairBatch.length > 0) {
        $.get(GET_DATA_URL, {'idPairList': JSON.stringify(nextIdPairBatch)})
            .done(function (data) {
                playlistBatchCallback(data, null);
            })
            .fail(function (data) {
                console.log(data);
            });
    }
}

function getNextIdPairBatch(batchSize) {
    let remainingPlaylists = $(".incomplete");
    let requestSize = Math.min(remainingPlaylists.length, playlistBatchSize);
    if (batchSize != null && batchSize > 0) {
        requestSize = Math.min(requestSize, batchSize);
    }

    let idPairList = [];
    for (let batchIndex = 0; batchIndex < requestSize; batchIndex++) {
        let playlistId = $(remainingPlaylists[batchIndex]).attr('id');
        let ownerId = $(remainingPlaylists[batchIndex]).data('owner-id');

        idPairList.push({'playlistId': playlistId, 'ownerId': ownerId});
    }

    return idPairList;
}

function getOwnerNames() {
    let ownerIdSet = Set();
    $(".playlist-container").each(function() {
        ownerIdSet.add($(this).data('owner-id'));
    });

    let ownerIdArray = Array.from(ownerIdSet);
    $.get(GET_OWNERS_URL, {'ownerIdList': ownerIdArray})
        .done(function(data) {
            fillOwnerNames(data);
        })
        .fail(function(data) {
            console.log(data);
        });
}

function fillOwnerNames(data) {
    console.log("Filling owner names");
    let ownerObj = jQuery.parseJSON(data);
    console.log(ownerObj);

    $(".no-owner").each(function() {
        let ownerId = $(this).data('owner-id');
        if (ownerId in ownerObj) {
            let ownerName = ownerObj[ownerId];
            $(this).find(".playlist-overlay-owner").text(ownerName);
        }
    });
}

//
// On document ready
//
$(document).ready(function() {
    getOwnerNames();
    playlistBatchCallback(null);
});