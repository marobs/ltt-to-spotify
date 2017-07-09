let midCol = document.getElementById('middle-col');
let $midCol = $(midCol);
let rightCol = document.getElementById('right-col');
let $rightCol = $(rightCol);

let dragIndex = -1;

const ADD_ENDPOINT = '/add';
const REORDER_ENDPOINT = '/reorder';

function AddOptions(uris, position) {
    this.uris = uris;
    this.position = position;
}

function ReorderOptions(range_start, range_length, insert_before) {
    this.range_start = range_start;
    this.range_length = range_length;
    this.insert_before = insert_before;
}

function sendEndpointRequest(url, options) {
    return new Promise((resolve, reject) => {
        $.post(url, options)
        .done((response) => {
            resolve(response);
        }).fail((e) => {
            // Error
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
            let options = new AddOptions(uris, $midCol.children($el).index($el));
            sendEndpointRequest(ADD_ENDPOINT, options)
            .fail((e) => {
                // Handle error
            });
        }
        else if (dragIndex >= 0 && source === midCol) { // Re-order Song
            let options = new ReorderOptions(dragIndex, 1, $midCol.children($el).index($el));
            sendEndpointRequest(REORDER_ENDPOINT, options)
            .fail((e) => {
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