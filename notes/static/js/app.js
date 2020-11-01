
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

function saveFile(title, file_contents) {
    $.ajax({
        data: {
            fileTitle: title,
            fileContent: file_contents,
        },
        type: 'POST',
        url: '/home',
        success: () => {
            showSavedMessage();
        }
    });
}

function showSavedMessage() {
    $('.saved-message').animate(
        {
            opacity: "1",
        }, 500, () => {
            setTimeout(
                () => {
                    $('.saved-message').animate({
                        opacity: "0",
                    }, 500);
                }, 1000
            );
        }
    );
}