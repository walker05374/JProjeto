function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function() {
        var imgElement = document.getElementById('preview-img');
        imgElement.src = reader.result;
    };

    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]);
    }
}