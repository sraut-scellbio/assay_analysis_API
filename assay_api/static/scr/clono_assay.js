document.addEventListener('DOMContentLoaded', function() {
  // Get all radio buttons with name 'option'
  const analysisType = document.getElementById('id_analysis_type');
  const nwellsDn = document.getElementById('id_num_wells');

  // when the number of wells is toggled
  nwellsDn.addEventListener('change', function() {
    // disable everything
   document.querySelectorAll('.image-inputs input').forEach(function(input){
     input.disabled = true
   var inputs1 = document.querySelectorAll('.d-1 input')
   var inputsn = document.querySelectorAll('.d-n input')
   var numWells = document.getElementById('id_num_wells').value;
   if (document.getElementById('id_analysis_type').value == 'Single Day') {
     for (var i = 0; i < 2*numWells; i++) {
       inputs1[i].disabled = false
       inputsn[i].disabled = true
     }
   }
   else if (document.getElementById('id_analysis_type').value == 'Multi Day') {
     for (var i = 0; i < 2*numWells; i++) {
       inputs1[i].disabled = false
       inputsn[i].disabled = false
     }
   }
  });
 });

 analysisType.addEventListener('change', function() {
   var inputs1 = document.querySelectorAll('.d-1 input')
   var inputsn = document.querySelectorAll('.d-n input')
   var numWells = document.getElementById('id_num_wells').value;
   if (analysisType.value == 'Single Day') {
     for (var i = 0; i < 2*numWells; i++) {
       inputs1[i].disabled = false
       inputsn[i].disabled = true
     }
   }
   else if (analysisType.value == 'Multi Day') {
     for (var i = 0; i < 2*numWells; i++) {
       inputs1[i].disabled = false
       inputsn[i].disabled = false
     }
   }
 });
});
