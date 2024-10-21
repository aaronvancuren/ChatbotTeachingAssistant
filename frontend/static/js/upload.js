document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    
    const files = document.getElementById("fileInput").files; // Get the selected files
    const fileDetailsDiv = document.getElementById("fileDetails");

    if (files.length > 0) {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append("files", files[i]);
        }

        fetch("/process", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            fileDetailsDiv.innerHTML = ""; // Clear previous file details

            // Process the response and display file details
            data.forEach(fileData => {
                const fileResultDiv = document.createElement("div");
                fileResultDiv.innerHTML = `
                    <h3>File: ${fileData.filename}</h3>
                    <p>Number of Chunks: ${fileData.num_chunks}</p>
                    <p>Extracted Text:</p>
                    <pre>${fileData.extracted_text.join("\n\n")}</pre>
                    <p>Embeddings:</p>
                    <pre>${JSON.stringify(fileData.embeddings, null, 2)}</pre>
                `;
                fileDetailsDiv.appendChild(fileResultDiv);
            });
        })
        .catch(error => {
            fileDetailsDiv.innerHTML = `<p>Error processing files: ${error.message}</p>`;
        });
    }
});