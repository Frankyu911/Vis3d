function changeAgentContent(){
    document.getElementById("inputFileAgent").value = document.getElementById("inputFile").value;
}

         $(function(){
            $('#username').bind('input propertychange', function() {
                $('#result').html($(this).val());
                });
          });

function changeAgentContents(){
    document.getElementById("inputFileAgents").value = document.getElementById("inputFiles").value;
}

 $(function(){
    $('#username').bind('input propertychange', function() {
        $('#result').html($(this).val());
        });
  });


