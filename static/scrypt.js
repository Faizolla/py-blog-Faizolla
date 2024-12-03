function show_files_name(target) {
    const selectedFilesDiv = document.getElementById('selected-files');
  
    const files = target.files;
    selectedFilesDiv.innerHTML = '';
  
    for (const file of files) {
        const fileName = file.name;
        const fileItem = document.createElement('p');
        fileItem.textContent = fileName;
        selectedFilesDiv.appendChild(fileItem);
    }
  }