dragula([document.getElementById('middle-col'), document.getElementById('right-col')], {
    copy: (el, source) => {
        return source === document.getElementById('right-col');
    },
    copySortSource: false,
    accepts: (el, target) => {
        return target === document.getElementById('middle-col');
    }
});