// This function is used to process files - it calls 'loadAsText'
function readFiles(event) {
    var fileList = event.target.files;

    for (var i=0; i < fileList.length; i++) {
        loadAsText(fileList[i]);
    }
}

// This function converts newline characters into <br /> characters, for HTML output only
function nl2br(str, is_xhtml) {
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
}

// This function reads a text file into a variable then displays it in the webpage
function loadAsText(theFile) {
    var reader = new FileReader();

    reader.onload = function(loadedEvent) {
        // loadedEvent.target.result has the loaded text file

        // Clear all text in <div id="file_contents">
        $("#file_contents").empty()

        // Convert plaintext to HTML, you won't need to do this when you process the data
        var file_content_str = nl2br(loadedEvent.target.result);

        // Add the file contents to <div id="file_contents"
        $("#file_contents").append(file_content_str);
    }

    reader.readAsText(theFile);
}

//change image

