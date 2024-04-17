// script.js
function uploadImage() {
  const input = document.querySelector("#image_input");
  const formData = new FormData();
  formData.append("file", input.files[0]);

  fetch("/upload/", {
      method: "POST",
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      const filename = data.filename;
      displayImage(filename);
  })
  .catch(error => {
      console.error("Error:", error);
  });
}

function displayImage(filename) {
  const displayDiv = document.querySelector("#display_image");
  displayDiv.style.backgroundImage = `url(${filename})`;
}
