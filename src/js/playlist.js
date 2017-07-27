//
// CONST Variables
//
const GET_DATA_URL = '/playlists/data';
const GET_OWNERS_URL = '/playlists/owners';

const playlistBatchSize = 20;

//////////////////////////////////////////////
//                                          //
//             Playlist Data                //
//                                          //
//////////////////////////////////////////////

function playlistBatchCallback(playlistData, batchSize) {
    if (playlistData != null) {
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
         .done(function (data) { playlistBatchCallback(data, null); })
         .fail(function (data) { console.log(data); });
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

//////////////////////////////////////////////
//                                          //
//              Owner Names                 //
//                                          //
//////////////////////////////////////////////

function getOwnerNames() {
    let ownerIdSet = new Set();
    $(".playlist-container").each(function() {
        ownerIdSet.add($(this).data('owner-id'));
    });

    let ownerIdArray = Array.from(ownerIdSet);

    let requestData = {'ownerIdList': JSON.stringify(ownerIdArray)};
    $.get(GET_OWNERS_URL, requestData)
     .done(function(data) { fillOwnerNames(data); })
     .fail(function(data) { console.log(data); });
}

function fillOwnerNames(data) {
    $(".no-owner").each(function() {
        let ownerId = $(this).data('owner-id');
        if (ownerId in data) {
            $(this).find(".playlist-overlay-owner").text(data[ownerId]);
        }
    });
}

//////////////////////////////////////////////
//                                          //
//             Document Ready               //
//                                          //
//////////////////////////////////////////////

$(document).ready(function() {
    getOwnerNames();
    playlistBatchCallback(null);
});