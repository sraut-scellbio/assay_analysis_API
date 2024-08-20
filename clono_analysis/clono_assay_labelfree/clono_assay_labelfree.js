document.addEventListener('DOMContentLoaded', function() {
  // Get all radio buttons with name 'option'
  const radios = document.querySelectorAll('input[name="analysis_type"]');
  var nwellsDn = document.getElementById('num_wells');

  // when the number of wells is toggled
  nwellsDn.addEventListener('change', function() {
    // disable everything
   document.querySelectorAll('.image-inputs input').forEach(function(input){
     input.disabled = true
   var inputs1 = document.querySelectorAll('.d-1 input')
   var inputsn = document.querySelectorAll('.d-n input')
   var numWells = document.getElementById('num_wells').value;
   if (document.getElementById('single_day').checked) {
     for (var i = 0; i < numWells; i++) {
       inputs1[i].disabled = false
       inputsn[i].disabled = true
     }
   }
   else if (document.getElementById('multi_day').checked) {
     for (var i = 0; i < numWells; i++) {
       inputs1[i].disabled = false
       inputsn[i].disabled = false
     }
   }
  });
 });
 radios.forEach(function(radio) {
   radio.addEventListener('change', function() {
     var inputs1 = document.querySelectorAll('.d-1 input')
     var inputsn = document.querySelectorAll('.d-n input')
     var numWells = document.getElementById('num_wells').value;
     if (document.getElementById('single_day').checked) {
       for (var i = 0; i < numWells; i++) {
         inputs1[i].disabled = false
         inputsn[i].disabled = true
       }
     }
     else if (document.getElementById('multi_day').checked) {
       for (var i = 0; i < numWells; i++) {
         inputs1[i].disabled = false
         inputsn[i].disabled = false
       }
     }
   });
 });
});

// if the form is submitted
document.querySelectorAll('input').eq(-1).onclick(function() {
  // save user inputs and send to backend
});
