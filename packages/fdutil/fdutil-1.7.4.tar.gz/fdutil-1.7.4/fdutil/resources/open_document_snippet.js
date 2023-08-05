
function open_document(text, title, focus){
    /* Create a new window. */
    var w = window.open();

    /* Set windows title. */
    w.document.title = (title !== undefined) ? title : 'Unknown text';

    /* Add the text to the document body. */
    w.document.body.innerHTML += text;

    /* focus the window if param is true */
    if (focus) {
        w.focus();
    }
}
