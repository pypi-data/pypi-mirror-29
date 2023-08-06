
function clickable_popover(element_id, content_div_id) {
    $(document).ready(function () {
        $('#' + element_id).popover({
            trigger: 'manual',
            html: true,
            animation: false,
            content: function () {
                return $('#' + content_div_id).html();
            }
        }).on('mouseenter', mouseenter).on('mouseleave', mouseleave);
    });
}

function mouseenter() {
    var _this = this;

    $(_this).popover('show');
    $('.popover').on('mouseleave', function () {
        $(_this).popover('hide');
    });
}

function mouseleave() {
    var _this = this;
    setTimeout(function () {
        if (!$('.popover:hover').length) {
            $(_this).popover('hide');
        }
    }, 50);
}
