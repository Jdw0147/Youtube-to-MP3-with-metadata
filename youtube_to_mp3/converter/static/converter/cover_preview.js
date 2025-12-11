document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById("id_cover_art");
    const previewDiv = document.getElementById("cover-art-preview");
    let img = document.getElementById("cover-art-img");
    let placeholder = document.getElementById("cover-art-placeholder");

    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (!img) {
                        img = document.createElement('img');
                        img.id = "cover-art-img";
                        previewDiv.innerHTML = "";
                        previewDiv.appendChild(img);
                    }
                    img.src = e.target.result;
                    if (placeholder) {
                        placeholder.style.display = "none";
                    }
                };
                reader.readAsDataURL(file);
            } else {
                if (img) {
                    img.remove();
                    img = null;
                }
                if (placeholder) {
                    placeholder.style.display = "block";
                }
            }
        });
    }
});