let $sliderContainer = $('.slider-container');

$sliderContainer.on('click', function(e) {
  let $this = $(this);
  let seekPos = $this.offset();
  let clickPos = e.clientX - seekPos.left;
  let width = $this.width();

  let clickPercent = (clickPos/width)*100;
  $this.find(".slider-left").css({width: clickPercent+"%"});
  $this.find('.slider-thumb').css({left: clickPercent+"%"});
  $this.find(".slider-right").css({width: (100-clickPercent)+"%"});
});

$sliderContainer.mousemove(function(e) {
  if (e.which !== 1) {
    return;
  }

  let $this = $(this);
  let seekPos = $this.offset();
  let clickPos = e.clientX - seekPos.left;
  let width = $this.width();

  let clickPercent = (clickPos/width)*100;
  $this.find(".slider-left").css({width: clickPercent+"%"});
  $this.find('.slider-thumb').css({left: clickPercent+"%"});
  $this.find(".slider-right").css({width: (100-clickPercent)+"%"});
});

$sliderContainer.hover(function() {
  $(this).children().addClass('hovering');
}, function() {
    $(this).children().removeClass('hovering');
});
