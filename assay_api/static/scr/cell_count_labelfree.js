
ocument.addEventListener('DOMContentLoaded', function() {
  const imageInput = document.getElementById('id_image');
  const submitButton = document.getElementById('submit-btn');

  // Disable the submit button initially
  submitButton.disabled = true;

  // Enable the submit button when an image is selected
  imageInput.addEventListener('change', function() {
      if (this.files.length > 0) {
          submitButton.disabled = false;
      }
  });

  // Add an event listener to the form, not the button, to handle submission
  const form = document.getElementById('image-upload-form');

  form.addEventListener('submit', function(event) {
      // Disable the button to prevent multiple submissions
      submitButton.disabled = true;

      // Optionally, change the button text to indicate the action
      submitButton.value = "Submitting...";
  });
});
