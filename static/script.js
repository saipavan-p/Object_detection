// const image_input = document.querySelector("#image_input");
// var uploaded_image = " ";

// image_input.addEventListener("change", function(){
//     const reader = new FileReader();
//    reader.addEventListener("load", () => {
//         uploaded_image = reader.result;
//         document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`;
//    });
//    reader.readAsDataURL(this.files[0]);
// })

const image_input = document.querySelector("#image_input");
const upload_button = document.querySelector("#upload_button");

upload_button.addEventListener("click", function () {
  image_input.click();  // Simulate clicking the hidden input
});

image_input.addEventListener("change", async function () {
  // Rest of your existing upload functionality goes here...
  const reader = new FileReader();
   reader.addEventListener("load", () => {
        uploaded_image = reader.result;
        document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`;
   });
   reader.readAsDataURL(this.files[0]);
  const formData = new FormData();
  formData.append("image", this.files[0]);

  const response = await fetch("/upload-image", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  console.log(data.message); // Display success message
});
