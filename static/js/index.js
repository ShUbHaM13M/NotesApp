let fExtension = '.txt'; 

$('.home').addClass('active');
$('.about').removeClass('active');

document.execCommand('defaultParagraphSeparator', false, 'p');

document.addEventListener('keydown', event => {
    if (event.key === "enter") {
        document.execCommand('insertLineBreak');
        event.preventDefault();
    };
});

function getFileInfo() {
    const title = $('.title-input').text();
    const content = document.querySelector('.editor');
    let contentText 

    if (fExtension === '.txt' || fExtension === '.rtf')
        contentText = document.querySelector('.editor').innerText;
    else
        contentText = document.querySelector('.editor').innerHTML;

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

$('#btn-download').on('click', (event) => {
    $('.file-ext-dialog').slideToggle(
            250,
            () => {
                closeOnScreenClick('.file-ext-dialog');
            }
        );
    });

$(document).ready(function (event) {
    $('#btn-save').on('click', function (event) {
        const fileInfo = getFileInfo();
        const title = fileInfo[0];
        const file_contents = fileInfo[1];
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
    });
});

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

function downloadFile(fileName) {
    var blob = new Blob([[fileName]], { type: 'text/html;charset=utf-8' });
    var link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName + fExtension;
    setTimeout(link.click(), 1000);
}

window.addEventListener('load', function () {
    document.querySelector('#sampleeditor').setAttribute('contenteditable', 'true');
});

function format(command, value) {
    document.execCommand(command, false, value);
}

function setUrl() {
    var url = document.getElementById('txtFormatUrl').value;
    var sText = document.getSelection();
    document.execCommand('insertHTML', false, '<a href="' + url + '" target="_blank">' + sText + '</a>');
    document.getElementById('txtFormatUrl').value = '';
}

const formatToolsContainer = $('.formatting-tools')
for (const child of formatToolsContainer.children()) {
    child.addEventListener('click', () => {
        const temp = child.querySelector('span');
        temp.classList.toggle('selected');
    });
}