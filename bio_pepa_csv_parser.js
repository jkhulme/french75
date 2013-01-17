function prep(){
    if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
        alert('The File APIs are not fully supported in this browser.');
    }
    
    document.getElementById('csvbp').addEventListener('change', readFile, false);
}

function readFile(evt) { 
    var files = evt.target.files;
    var output = [];
    var valid_files = [];
    for (var i = 0, f; f = files[i]; i++) {
        if (escape(f.type) != 'text/csv') {
            document.getElementById('file_warnings').innerHTML = 'Some files ignored due to incorrect type';
        } else {
            output.push('<li><strong>', escape(f.name), '</strong> </li>');
            
            var reader = new FileReader();
            reader.onload = (function(csv_file) {
                return function(e) {
                    var span = document.createElement('span');
                    span.innerHTML = ['<p>', e.target.result, '</p>'].join('');
                    document.getElementById('file_text').appendChild(span);
                    alert('fuck');
                };
            })(f);
            
            reader.readAsText(f,"UTF-8");
            valid_files += i;
        }
    }
    
    document.getElementById('file_list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

