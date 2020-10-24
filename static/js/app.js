
const speed = 200

$('#mob-view').on({
    'click': () => {
        $('.mob-list').slideDown(speed);
        $('.mob-list').css('display', 'flex');
        closeOnScreenClick('.mob-list');
    },
});

$('#close-btn').on({
    'click': () => {
        $('.mob-list').slideUp(speed);
    },
})

function closeOnScreenClick(target) {
    const container = $(target);
    $(document).mouseup(function(e) {
        if(!container.is(e.target) && container.has(e.target).length === 0)
        {
            container.slideUp(speed);
            $(document).off("mouseup");
        }
    });
}