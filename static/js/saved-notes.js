
let fExtension = ".txt";

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
            deleteFile(fileName)
            noteContainer.classList.add('delete');
            setTimeout(() => {
                noteContainer.style.display = "none";
            }, 350);
        }); 
        
    });
});

const editButtons = document.querySelectorAll('.edit-btn');
editButtons.forEach(element => {
    element.addEventListener('click', () => {
        const noteActions = element.parentNode;
        const parent = noteActions.parentNode;
        editNote(parent);
    });
});


const noteContents = document.querySelectorAll('.note-contents');
const editNoteContainer = $('.edit-note-container');
const editNoteTitle = $('.title');
const editNoteContents = $('.contents');
const editNoteCloseBtn = $('.close');

noteContents.forEach(note => {
    note.addEventListener('click', () => {
        const parent = note.parentNode;
        editNote(parent);
    });
});

function editNote(parent) {
    const noteTitle = parent.querySelector('.note-title').innerHTML;
    const noteContents = parent.querySelector('.note-contents').innerHTML;

    editNoteTitle.text(noteTitle);
    editNoteContents.text(noteContents);
    editNoteContents.attr("contenteditable", "true");
    editNoteContainer.animate({
        opacity: "1",
    }, 250, () => {
        editNoteContainer.css("pointer-events", "all");
        editNoteContents.focus();
        editNoteCloseBtn.attr("onClick", "hideEditNote()");
        
        const saveBtn = $('#save-btn');
        saveBtn.on('click', () => {
            const contents = editNoteContents.text();
            saveEditedFile(noteTitle, contents);
        });

        $('#btn-download').on('click', () => {
            $('.file-ext-dialog').slideDown(
                    250,
                    () => {
                        $('.file-ext-dialog').css("display", "flex");
                        closeOnScreenClick('.file-ext-dialog');
                    }
                );
        });
    });
}

function getFileInfo() {
    const title = document.querySelector('.title').textContent;
    let contentText;

    if (fExtension === '.txt' || fExtension === '.rtf')
        contentText = editNoteContents.text();
    else
        contentText = editNoteContents.html();

    return [title, contentText];
} 

const extensionBtns = document.querySelectorAll('.ext');
extensionBtns.forEach((btn) => {
    btn.addEventListener(
        'click', () => {
            const btnText = btn.children[0].getAttribute('value');
            fExtension = btnText;
            const fileInfo = getFileInfo();
            const fileTitle = fileInfo[0];
            const fileContents = fileInfo[1];
            download(fileContents, fileTitle+fExtension, "text/html");
        }
    );
});

function saveEditedFile(_fileTitle, _fileContent) {
    $.ajax({
        data: {
            fileTitle: _fileTitle,
            fileContent: _fileContent,
        },
        type: 'POST',
        url: '/saved-notes',
        success: () => {
            showSavedMessage();
        }
    });
    setTimeout(() => {
        location.reload();
    }, 1300);
}


function deleteFile(fileName) {
    $.ajax({
        type: 'POST',
        url: '/delete-file/' + fileName,
    });
}

function hideEditNote() {
    editNoteContainer.css("pointer-events", "none");
    editNoteContainer.animate({
        opacity: "0",
    }, 250, );
}