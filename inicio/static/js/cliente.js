function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function(e) {
        document.getElementById('preview-img').src = e.target.result;
    };

    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]);
    }
}