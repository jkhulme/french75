function prep(){
    if (window.File && window.FileReader && window.FileList && window.Blob) {
      alert('File APIs are supported');
    } else {
      alert('The File APIs are not fully supported in this browser.');
    }
    alert('fuck');
    //document.getElementById('csvbp').addEventListener('change', readFile, false);
    alert('fuck');
}

function readFile(evt) { 
    var files = evt.target.files;
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                  f.size, ' bytes, last modified: ',
                  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                  '</li>');
    }
    document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

