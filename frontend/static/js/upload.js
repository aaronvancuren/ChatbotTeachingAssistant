// frontend/static/js/main.js

// Handle Upload Form Submission
document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData();
    const fileField = document.getElementById('file');

    formData.append('file', fileField.files[0]);

    try {
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
        messageContainer.removeChild(messageDiv);
    }, 5000);
}

// Function to Add a File to the List
function addFileToList(fileName) {
    const fileList = document.getElementById('file-list');
    const listItem = document.createElement('li');
    listItem.id = `file-${fileName}`;
    listItem.innerHTML = `
        ${fileName}
        <button onclick="deleteFile('${fileName}')">Delete</button>
        <button onclick="showUpdateForm('${fileName}')">Update</button>
    `;
    fileList.appendChild(listItem);
}

// Function to Delete a File
async function deleteFile(fileName) {
    if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`/files/delete/${encodeURIComponent(fileName)}`, {
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
    }
}

// Function to Remove a File from the List
function removeFileFromList(fileName) {
    const listItem = document.getElementById(`file-${fileName}`);
    if (listItem) {
        listItem.remove();
    }
}

// Function to Show the Update Form
function showUpdateForm(fileName) {
    document.getElementById('update-file-name').innerText = fileName;
    document.getElementById('update-modal').classList.remove('hidden');
}

// Function to Hide the Update Form
function hideUpdateForm() {
    document.getElementById('update-modal').classList.add('hidden');
    document.getElementById('update-form').reset();
}

// Handle Update Form Submission
document.getElementById('update-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    const fileName = document.getElementById('update-file-name').innerText;
    const content = document.getElementById('update-content').value;

    const formData = new FormData();
    formData.append('content', content);

    try {
        const response = await fetch(`/files/update/${encodeURIComponent(fileName)}`, {
            method: 'PUT',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message, 'success');
            hideUpdateForm();
            // Optionally, update the file list if needed
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('An unexpected error occurred.', 'error');
        console.error('Error:', error);
    }
});