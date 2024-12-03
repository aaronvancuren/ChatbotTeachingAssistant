let currentUpdateFileName = null;

// Handle Upload Form Submission
document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData();
    const fileField = document.getElementById('file');

    formData.append('file', fileField.files[0]);

    try {
        showLoading();
        const response = await fetch('/files/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message, 'success');
            addFileToList(result.file_name);
            fileField.value = ''; // Clear the file input
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('An unexpected error occurred.', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

// Function to Display Messages
function showMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerText = message;
    messageContainer.appendChild(messageDiv);

    // Remove message after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode === messageContainer) {
            messageContainer.removeChild(messageDiv);
        }
    }, 5000);
}

// Function to Add a File to the List
function addFileToList(fileName) {
    const fileList = document.getElementById('file-list');
    const listItem = document.createElement('li');
    // Sanitize fileName for use in ID
    const safeFileName = fileName.replace(/[^a-zA-Z0-9-_]/g, '_');
    listItem.id = `file-${safeFileName}`;
    listItem.innerHTML = `
        ${fileName}
        <button onclick="deleteFile('${encodeURIComponent(fileName)}')">Delete</button>
        <button onclick="initiateUpdate('${encodeURIComponent(fileName)}')">Update</button>
    `;
    fileList.appendChild(listItem);
}

// Function to Delete a File
async function deleteFile(fileName) {
    if (!confirm(`Are you sure you want to delete "${decodeURIComponent(fileName)}"?`)) {
        return;
    }

    try {
        showLoading();
        const response = await fetch(`/files/delete/${fileName}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message, 'success');
            removeFileFromList(fileName);
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('An unexpected error occurred.', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Function to Remove a File from the List
function removeFileFromList(fileName) {
    const safeFileName = decodeURIComponent(fileName).replace(/[^a-zA-Z0-9-_]/g, '_');
    const listItem = document.getElementById(`file-${safeFileName}`);
    if (listItem) {
        listItem.remove();
    }
}

// Function to Initiate Update
function initiateUpdate(fileName) {
    currentUpdateFileName = fileName;
    const updateFileInput = document.getElementById('update-file-input');
    updateFileInput.value = ''; // Reset the file input
    updateFileInput.click(); // Open the file dialog
}

// Function to Handle Update File Selection
async function handleUpdateFile(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (!file) {
        // No file selected
        return;
    }

    if (!currentUpdateFileName) {
        showMessage('No file selected for update.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading();
        const response = await fetch(`/files/update/${currentUpdateFileName}`, {
            method: 'PUT',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message, 'success');
            // Optionally, update the file list if needed
            // For simplicity, we can reload the page or update specific entries
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('An unexpected error occurred.', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
        currentUpdateFileName = null;
    }
}

// Loading Indicator Functions
function showLoading() {
    let loadingIndicator = document.getElementById('loading-indicator');
    if (!loadingIndicator) {
        loadingIndicator = document.createElement('div');
        loadingIndicator.id = 'loading-indicator';
        loadingIndicator.innerHTML = '<div class="spinner"></div>';
        loadingIndicator.style.position = 'fixed';
        loadingIndicator.style.top = '50%';
        loadingIndicator.style.left = '50%';
        loadingIndicator.style.transform = 'translate(-50%, -50%)';
        loadingIndicator.style.zIndex = '1000';
        loadingIndicator.style.display = 'none';
        document.body.appendChild(loadingIndicator);
    }
    loadingIndicator.style.display = 'block';
}

function hideLoading() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
}