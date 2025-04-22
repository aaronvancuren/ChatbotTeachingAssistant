async function submitNewCourseForm() {
    const form = document.getElementById("newClassForm");
    const formData = new FormData(form);

    // Include default values
    formData.append("model", "gpt-4");

    const response = await fetch("/dashboard/create_course-course", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        alert("Class created!");
        window.location.reload();
    } else {
        alert("Failed to create class: " + result.error);
    }
}