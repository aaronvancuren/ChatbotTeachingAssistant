const studentDropzone = document.getElementById("studentDropzone");
const fileDropzone = document.getElementById("fileDropzone");
const studentFileInput = document.getElementById("studentFileInput");
const uploadFileInput = document.getElementById("uploadFileInput");
const fileQueueEl = document.getElementById("fileQueue");
const studentList = document.getElementById("studentList"); // NEW
const removeAllBtn = document.getElementById("removeAllBtn"); // <-- NEW
const uploadBtn = document.getElementById("uploadBtn");
const progressBar = document.getElementById("uploadProgress");
const uploadResult = document.getElementById("uploadResult");

const allowedExtensions = [".txt", ".pdf", ".doc", ".docx", ".html", ".css"];

// DataTransfer that holds all staged files
let combinedFilesDataTransfer = new DataTransfer();

// Dropzone click => open file dialog
studentDropzone.addEventListener("click", () => {
  studentFileInput.click();
});

fileDropzone.addEventListener("click", () => {
  uploadFileInput.click();
});

// Drag & Drop
studentDropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  studentDropzone.classList.add("bg-info", "text-white");
});
studentDropzone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  studentDropzone.classList.remove("bg-info", "text-white");
});
studentDropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  studentDropzone.classList.remove("bg-info", "text-white");
  handleFileDrop(e, "student");
});

fileDropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  fileDropzone.classList.add("bg-info", "text-white");
});
fileDropzone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  fileDropzone.classList.remove("bg-info", "text-white");
});
fileDropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  fileDropzone.classList.remove("bg-info", "text-white");
  handleFileDrop(e, "upload");
});

// File dialog selection
uploadFileInput.addEventListener("change", (e) => {
  handleFileSelection(e, "upload");
});

studentFileInput.addEventListener("change", (e) => {
  handleFileSelection(e, "student");
});

function handleFileSelection(e, type) {
  const targetInput = type === "upload" ? uploadFileInput : studentFileInput;
  const fileQueue = type === "upload" ? fileQueueEl : studentList;
  const allowedExtensions = type === "upload" 
    ? [".txt", ".pdf", ".doc", ".docx", ".html", ".css"] 
    : [".txt", ".csv", ".xls", ".xlsx"];

  const newDataTransfer = new DataTransfer();

  for (const file of e.target.files) {
    const extension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (allowedExtensions.includes(extension)) {
      newDataTransfer.items.add(file);
    } else {
      alert(`"${file.name}" is not an allowed file type.`);
    }
  }

  targetInput.files = newDataTransfer.files;
  displayQueuedFiles(targetInput.files, fileQueue);
}

function handleFileDrop(e, type) {
  const targetInput = type === "upload" ? uploadFileInput : studentFileInput;
  const fileQueue = type === "upload" ? fileQueueEl : studentList;
  const allowedExtensions = type === "upload" 
    ? [".txt", ".pdf", ".doc", ".docx", ".html", ".css"] 
    : [".txt", ".csv", ".xls", ".xlsx"];

  const newDataTransfer = new DataTransfer();

  for (const file of e.dataTransfer.files) {
    const extension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (allowedExtensions.includes(extension)) {
      newDataTransfer.items.add(file);
    } else {
      alert(`"${file.name}" is not an allowed file type.`);
    }
  }

  targetInput.files = newDataTransfer.files;
  displayQueuedFiles(targetInput.files, fileQueue);
}

// Display the queued files with a Remove button
function displayQueuedFiles(fileList, queueElement) {
  queueElement.innerHTML = "";

  if (!fileList.length) {
    const li = document.createElement("li");
    li.className = "list-group-item text-muted";
    li.textContent = "No files queued";
    queueElement.appendChild(li);
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
    removeBtn.addEventListener("click", () => removeFileFromQueue(i, queueElement));

    li.appendChild(removeBtn);
    queueElement.appendChild(li);
  }
}

// Remove a single file from the queue
function removeFileFromQueue(index, queueElement) {
  const newDataTransfer = new DataTransfer();

  const currentFiles = queueElement === fileQueueEl 
    ? uploadFileInput.files 
    : studentFileInput.files;

  for (let i = 0; i < currentFiles.length; i++) {
    if (i !== index) {
      newDataTransfer.items.add(currentFiles[i]);
    }
  }

  if (queueElement === fileQueueEl) {
    uploadFileInput.files = newDataTransfer.files;
    displayQueuedFiles(uploadFileInput.files, fileQueueEl);
  } else {
    studentFileInput.files = newDataTransfer.files;
    displayQueuedFiles(studentFileInput.files, studentList);
  }
}

// "Remove All" button => clear entire queue
removeAllBtn.addEventListener("click", removeAllFromQueue);

function removeAllFromQueue() {

  combinedFilesDataTransfer = new DataTransfer();
  uploadFileInput.value = ""; // reset the file input
  displayQueuedFiles([], fileQueueEl); // refresh UI
  displayQueuedFiles([], studentList); // refresh student UI
}

// Click "Upload"
uploadBtn.addEventListener("click", async () => {
  if (!uploadFileInput.files.length) {
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
  for (let i = 0; i < uploadFileInput.files.length; i++) {
    formData.append("files", uploadFileInput.files[i]);
  }

  try {
    const response = await fetch("/dashboard/upload", {
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

// Delete file
async function deleteFile(fileName) {
  if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
    return;
  }
  try {
    const response = await fetch(`/dashboard/delete/${fileName}`, {
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
    const response = await fetch(`/dashboard/update/${fileName}`, {
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
      const response = await fetch("/dashboard/delete_all", {
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