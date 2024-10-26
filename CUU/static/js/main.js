$(document).ready(function () {
    // Initialize: Hide sections and elements on page load
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview Function
    function readURL(input) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css({
                    'background-image': `url(${e.target.result})`,
                    'background-size': 'cover',
                    'background-position': 'center',
                    'width': '200px',
                    'height': '200px',
                    'display': 'block'
                }).hide().fadeIn(650); // Smoothly fade in the preview
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Show the preview when the user selects an image
    $("#imageUpload").change(function () {
        $('.image-section').show();  // Reveal the image section
        $('#btn-predict').show();    // Show the predict button
        $('#result').text('').hide();  // Clear and hide previous results
        readURL(this);  // Display the uploaded image preview
    });

    // Handle Predict Button Click
    $('#btn-predict').click(function () {
        let form_data = new FormData($('#upload-file')[0]);  // Form data including the uploaded image

        // Show loading animation and hide predict button
        $(this).hide();
        $('.loader').show();

        // Make the AJAX call to the /predict endpoint
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Hide the loader and display the result
                console.log(data)
                $('.loader').hide();
                $('#result').fadeIn(600).text('Result: ' + data.predicted_class);
                console.log('Prediction successful!');
            },
            error: function (xhr, status, error) {
                // Handle any errors from the server
                $('.loader').hide();
                $('#result').fadeIn(600).text('An error occurred. Please try again.');
                console.error('Error:', status, error);
            }
        });
    });
});

