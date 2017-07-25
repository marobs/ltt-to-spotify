let $seekContainer = $('#seek-container');
let $volumeContainer = $('#volume-container');

$seekContainer.on('click', function(e) {
    let $this = $(this);
    let seekPos = $this.offset();
    let clickPos = e.clientX - seekPos.left;
    let width = $this.width();

    let clickPercent = Math.max(Math.min((clickPos/width)*100, 100), 0);
    $this.find(".slider-left").css({width: clickPercent+"%"});
    $this.find('.slider-thumb').css({left: clickPercent+"%"});
    $this.find(".slider-right").css({width: (100-clickPercent)+"%"});

    if (currentPreviewElement !== null) {
        currentPreviewHowl.seek(30*clickPos/width);
    }

    if (windowInterval === -1) {
        windowInterval = setInterval(updateSeekBar, 50, currentPreviewHowl);
    }
});

$seekContainer.mousemove(function(e) {
    if (e.which !== 1) {
        return;
    }

    if (windowInterval !== -1) {
        clearInterval(windowInterval);
        windowInterval = -1;
    }

    let $this = $(this);
    let seekPos = $this.offset();
    let clickPos = e.clientX - seekPos.left;
    let width = $this.width();

    let clickPercent = Math.max(Math.min((clickPos/width)*100, 100), 0);
    $this.find(".slider-left").css({width: clickPercent+"%"});
    $this.find('.slider-thumb').css({left: clickPercent+"%"});
    $this.find(".slider-right").css({width: (100-clickPercent)+"%"});
});

$seekContainer.hover(function() {
    $(this).children().addClass('hovering');
}, function() {
    $(this).children().removeClass('hovering');
});

$volumeContainer.on('click', function(e) {
    let $this = $(this);
    let seekPos = $this.offset();
    let clickPos = e.clientX - seekPos.left;
    let width = $this.width();

    let clickPercent = Math.max(Math.min((clickPos/width)*100, 100), 0);
    $this.find(".slider-left").css({width: clickPercent+"%"});
    $this.find('.slider-thumb').css({left: clickPercent+"%"});
    $this.find(".slider-right").css({width: (100-clickPercent)+"%"});
});

$volumeContainer.mousemove(function(e) {
    if (e.which !== 1) {
        return;
    }

    let $this = $(this);
    let seekPos = $this.offset();
    let clickPos = e.clientX - seekPos.left;
    let width = $this.width();

    let clickPercent = Math.max(Math.min((clickPos/width)*100, 100), 0);
    $this.find(".slider-left").css({width: clickPercent+"%"});
    $this.find('.slider-thumb').css({left: clickPercent+"%"});
    $this.find(".slider-right").css({width: (100-clickPercent)+"%"});
});

$volumeContainer.hover(function() {
    $(this).children().addClass('hovering');
}, function() {
    $(this).children().removeClass('hovering');
});
