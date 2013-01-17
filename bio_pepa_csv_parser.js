function prep(){
    if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
        alert('The File APIs are not fully supported in this browser.');
    }
    
    document.getElementById('csvbp').addEventListener('change', readFile, false);
}

function readFile(evt) { 
    var files = evt.target.files;
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
        if (escape(f.type) != 'text/csv') {
            document.getElementById('file_warnings').innerHTML = 'Some files ignored due to incorrect type';
        } else {
            output.push('<li><strong>', escape(f.name), '</strong> </li>');
        }
    }
    document.getElementById('file_list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

