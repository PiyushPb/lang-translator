const dropZone = document.querySelector("#drop-zone");
const inputElement = document.querySelector("input");
const img = document.querySelector("#img");
let p = document.querySelector("#p");

const dropdowns = document.querySelectorAll(".dropdown-container"),
  outputLanguageDropdown = document.querySelector("#output-language");

function populateDropdown(dropdown, options) {
  dropdown.querySelector("ul").innerHTML = "";
  options.forEach((option) => {
    const li = document.createElement("li");
    const title = option.name + " (" + option.native + ")";
    li.innerHTML = title;
    li.dataset.value = option.code;
    li.classList.add("option");
    dropdown.querySelector(".dropdown-menu").appendChild(li);
  });
}

populateDropdown(outputLanguageDropdown, languages);

dropdowns.forEach((dropdown) => {
  dropdown.addEventListener("click", (e) => {
    dropdown.classList.toggle("active");
  });

  dropdown.querySelectorAll(".option").forEach((item) => {
    item.addEventListener("click", (e) => {
      //remove active class from current dropdowns
      dropdown.querySelectorAll(".option").forEach((item) => {
        item.classList.remove("active");
      });
      item.classList.add("active");
      const selected = dropdown.querySelector(".selected");
      selected.innerHTML = item.innerHTML;
      selected.dataset.value = item.dataset.value;
      translate();
    });
  });
});
document.addEventListener("click", (e) => {
  dropdowns.forEach((dropdown) => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove("active");
    }
  });
});

function isFileValid(file) {
  const allowedExtensions = ["jpg", "jpeg", "png"];
  const extension = file.name.split(".").pop().toLowerCase();
  return allowedExtensions.includes(extension);
}

function showAlert(message) {
  Toastify({
    text: message,
    duration: 3000,
    newWindow: true,
    close: true,
    gravity: "bottom",
    position: "left",
    stopOnFocus: true,
    style: {
      background: "red",
    },
  }).showToast();
}

inputElement.addEventListener("change", function (e) {
  const clickFile = this.files[0];
  if (clickFile && isFileValid(clickFile)) {
    img.style = "display:block;";
    p.style = "display: none";
    const reader = new FileReader();
    reader.readAsDataURL(clickFile);
    reader.onloadend = function () {
      const result = reader.result;
      let src = this.result;
      img.src = src;
      img.alt = clickFile.name;
    };
  } else {
    showAlert("Invalid file format. Please upload a JPG or PNG file.");
    this.value = null;
  }
});

dropZone.addEventListener("click", () => inputElement.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  img.style = "display:block;";
  let file = e.dataTransfer.files[0];

  if (file && isFileValid(file)) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
      e.preventDefault();
      p.style = "display: none";
      let src = this.result;
      img.src = src;
      img.alt = file.name;
    };
  } else {
    showAlert("Invalid file format. Please upload a JPG or PNG file.");
  }
});

const outputLanguage = outputLanguageDropdown.querySelector(".selected"),
  outputTextElem = document.querySelector("#output-text"),
  translatebtn = document.querySelector("#translatebtn"),
  inputchars = document.getElementById("input-chars");

translatebtn.addEventListener("click", () => {
  translate();
});

async function translate() {
  const outputLanguageCode = outputLanguage.dataset.value;
  const imageFile = inputElement.files[0];

  translatebtn.classList.add("inprogress");
  translatebtn.innerHTML = "Translation in progress please wait!";

  if (!imageFile || !isFileValid(imageFile)) {
    showAlert("Invalid file format. Please upload a JPG or PNG file.");
    return;
  }

  const formData = new FormData();
  formData.append("image", imageFile);
  formData.append("target_language", outputLanguageCode);

  await fetch("http://localhost:8000/translate-image", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => (outputTextElem.value = data.translated_text))
    .catch((error) => {
      translatebtn.classList.remove("inprogress");
      translatebtn.innerHTML = "Upload and Translate";

      console.error("Error during translation:", error);
      showAlert("Error during translation. Please try again.");
    });

  translatebtn.classList.remove("inprogress");
  translatebtn.innerHTML = "Upload and Translate";
}
