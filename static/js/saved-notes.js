const deleteButtons = document.querySelectorAll('.delete-btn');
deleteButtons.forEach(element => {
    element.addEventListener('click', () => {
        const parentOfButton = element.parentNode;
        const noteContainer = parentOfButton.parentNode;
        const noteTitleDiv = noteContainer.querySelector('.note-title');
        let fileName = noteTitleDiv.textContent;
        
        const deleteTitle = $('.main .filename');
        deleteTitle.html(`<span style="color: var(--color-primary);">${fileName}</span> will be deleted..!`);

        const deleteContainer = $('.delete-container');
        deleteContainer.addClass('delete-container-active');
        deleteContainer.on({
            'click': () => {
                $('#delete').off('click');
                deleteContainer.removeClass('delete-container-active');
            },
        });

        $('#delete').click( () => {
            $.ajax({
                type: 'POST',
                url: '/delete-file/' + fileName,
                success: function(response) {
                    if (response) {
                        noteContainer.classList.add('delete');
                        setTimeout(() => {
                            noteContainer.style.display = "none";
                        }, 350);
                        return;
                    }
                }
            });
        });
    });
});
