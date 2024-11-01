document.addEventListener('DOMContentLoaded', function() {
    // Get all radio buttons with name 'option'
    const nwellsDn = document.getElementById('id_num_wells');
  
    // when the number of wells is toggled
    nwellsDn.addEventListener('change', function() {
      // disable everything
     document.querySelectorAll('.image-inputs input').forEach(function(input){
        input.disabled = true
        var inputs1 = document.querySelectorAll('.d-1 input')
        var numWells = document.getElementById('id_num_wells').value;
        for (var i = 0; i < numWells; i++) {
            inputs1[i].disabled = false
        }
    });
   });

  });
  