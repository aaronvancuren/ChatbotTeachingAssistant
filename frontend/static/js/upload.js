const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const fileQueueEl = document.getElementById("fileQueue");
const removeAllBtn = document.getElementById("removeAllBtn"); // <-- NEW
const uploadBtn = document.getElementById("uploadBtn");
const progressBar = document.getElementById("uploadProgress");
const uploadResult = document.getElementById("uploadResult");

const allowedExtensions = [".txt", ".pdf", ".doc", ".docx", ".html", ".css"];

// A DataTransfer that holds all staged files
let combinedFilesDataTransfer = new DataTransfer();

// Dropzone click => open file dialog
dropzone.addEventListener("click", () => {
  fileInput.click();
});

// Drag & Drop
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("bg-info", "text-white");
});
dropzone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  dropzone.classList.remove("bg-info", "text-white");
});
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("bg-info", "text-white");

  for (const file of e.dataTransfer.files) {
    const extension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (allowedExtensions.includes(extension)) {
      combinedFilesDataTransfer.items.add(file);
    } else {
      alert(`"${file.name}" is not an allowed file type.`);
    }
  }
  fileInput.files = combinedFilesDataTransfer.files;

  displayQueuedFiles(fileInput.files);
});

// File dialog selection
fileInput.addEventListener("change", (e) => {
  for (const file of e.target.files) {
    const extension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (allowedExtensions.includes(extension)) {
      combinedFilesDataTransfer.items.add(file);
    } else {
      alert(`"${file.name}" is not an allowed file type.`);
    }
  }
  fileInput.files = combinedFilesDataTransfer.files;
  displayQueuedFiles(fileInput.files);
});

// Display the queued files with a Remove button
function displayQueuedFiles(fileList) {
  fileQueueEl.innerHTML = "";

  if (!fileList.length) {
    const li = document.createElement("li");
    li.className = "list-group-item text-muted";
    li.textContent = "No files queued";
    fileQueueEl.appendChild(li);
    return;
  }

  for (let i = 0; i < fileList.length; i++) {
    const file = fileList[i];
    const li = document.createElement("li");
    li.className = "list-group-item d-flex justify-content-between align-items-center";
    li.textContent = file.name;

    // "Remove" button for single file
    const removeBtn = document.createElement("button");
    removeBtn.className = "btn btn-danger btn-sm ms-3";
    removeBtn.textContent = "Remove";
    removeBtn.addEventListener("click", () => removeFileFromQueue(i));

    li.appendChild(removeBtn);
    fileQueueEl.appendChild(li);
  }
}

// Remove a single file from the queue
function removeFileFromQueue(index) {
  const newDataTransfer = new DataTransfer();

  const currentFiles = combinedFilesDataTransfer.files;
  for (let i = 0; i < currentFiles.length; i++) {
    if (i !== index) {
      newDataTransfer.items.add(currentFiles[i]);
    }
  }

  combinedFilesDataTransfer = newDataTransfer;
  fileInput.files = combinedFilesDataTransfer.files;
  displayQueuedFiles(fileInput.files);
}

// "Remove All" button => clear entire queue
removeAllBtn.addEventListener("click", removeAllFromQueue);

function removeAllFromQueue() {

  combinedFilesDataTransfer = new DataTransfer();
  fileInput.value = ""; // reset the file input
  displayQueuedFiles([]); // refresh UI
}

// Click "Upload"
uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("No files to upload.");
    return;
  }

  // show spinner in button
  uploadBtn.disabled = true;
  uploadBtn.innerHTML = `Uploading...
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`;

  // Reset progress
  updateProgress(0);

  // Build FormData
  const formData = new FormData();
  for (let i = 0; i < fileInput.files.length; i++) {
    formData.append("files", fileInput.files[i]);
  }

  try {
    const response = await fetch("/files/upload", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Upload failed.");
    }

    updateProgress(100);
    const data = await response.json();
    showUploadResult(data.uploaded_files);

    // Clear queue on success
    removeAllFromQueue(); 

  } catch (error) {
    console.error("Upload Error:", error);
    alert(`Error: ${error.message}`);
  } finally {
    // Re-enable upload button
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload";
  }
});

//update progress bar
function updateProgress(value) {
  progressBar.style.width = `${value}%`;
  progressBar.textContent = `${value}%`;
  progressBar.setAttribute("aria-valuenow", value);
}

// show results after upload
function showUploadResult(files) {
  uploadResult.innerHTML = "";
  uploadResult.classList.remove("d-none");

  files.forEach((file) => {
    const li = document.createElement("li");
    li.className = "list-group-item";
    if (file.error) {
      li.textContent = `Error uploading ${file.filename}: ${file.error}`;
    } else {
      li.textContent = `File: ${file.filename} - Uploaded Successfully`;
    }
    uploadResult.appendChild(li);
  });
}

// Update progress bar
function updateProgress(value) {
  progressBar.style.width = `${value}%`;
  progressBar.textContent = `${value}%`;
  progressBar.setAttribute("aria-valuenow", value);
}

// Display result from server
function showUploadResult(files) {
  uploadResult.innerHTML = "";
  uploadResult.classList.remove("d-none");

  files.forEach((file) => {
    const li = document.createElement("li");
    li.className = "list-group-item";
    if (file.error) {
      li.textContent = `Error uploading ${file.filename}: ${file.error}`;
    } else {
      li.textContent = `File: ${file.filename} - Uploaded Successfully`;
    }
    uploadResult.appendChild(li);
  });
}

// Delete file
async function deleteFile(fileName) {
  if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
    return;
  }
  try {
    const response = await fetch(`/files/delete/${fileName}`, {
      method: "DELETE"
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Delete failed.");
    }
    // Remove from UI or reload
    document.getElementById(`file-${sanitizeId(fileName)}`).remove();
    alert(`File "${fileName}" has been deleted.`);
  } catch (error) {
    console.error(error);
    alert(`Error deleting file: ${error.message}`);
  }
}

// Update File
function initiateUpdate(fileName) {
  // Trigger hidden input
  const updateInput = document.getElementById("update-file-input");
  updateInput.setAttribute("data-filename", fileName);
  updateInput.click();
}

async function handleUpdateFile(event) {
  const fileInput = event.target;
  const fileName = fileInput.getAttribute("data-filename");

  if (!fileInput.files.length) {
    return;
  }

  const newFile = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", newFile);

  try {
    const response = await fetch(`/files/update/${fileName}`, {
      method: "PUT",
      body: formData
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Update failed.");
    }
    alert(`File "${fileName}" has been updated successfully.`);
    // location.reload();
  } catch (error) {
    console.error(error);
    alert(`Error updating file: ${error.message}`);
  } finally {
    // Reset the file input
    fileInput.value = "";
    fileInput.removeAttribute("data-filename");
  }
}

// Utility to sanitize an ID-friendly string
function sanitizeId(filename) {
  return filename.replace(/\s/g, "_").replace(/[\\/]/g, "_");
}

async function deleteAllFiles() {
    const deleteAllBtn = document.getElementById("deleteAllBtn");
  
    if (!confirm("Are you sure you want to delete ALL files?")) {
      return;
    }
  
    // Disable the button, change text, add spinner
    deleteAllBtn.disabled = true;
    deleteAllBtn.innerHTML = `Deleting...
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`;
  
    try {
      const response = await fetch("/files/delete_all", {
        method: "DELETE",
      });
  
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Failed to delete all files.");
      }
  
      alert("All files have been deleted successfully.");
      location.reload();
    } catch (error) {
      console.error("Error deleting all files:", error);
      alert(`Error deleting all files: ${error.message}`);
    } finally {
      // Re-enable the button and restore text/spinner
      deleteAllBtn.disabled = false;
      deleteAllBtn.textContent = "Delete All";
    }
  }