

// header time value
var token = localStorage.getItem("token");
document.querySelector('.custom-file-input').addEventListener('change', function (e) {
  var name = document.getElementById("customFileInput").files[0].name;
  var nextSibling = e.target.nextElementSibling
  nextSibling.innerText = name
})

  $("#fileUplaod").click(function(){
      var token = localStorage.getItem("token");
      var customFileInput = $('#customFileInput')[0].files[0]
      if (customFileInput != ""){
      if (customFileInput.type == 'application/json'){
      var formData = new FormData();
        formData.append('file', $('#customFileInput')[0].files[0]);
        // alert("fssjbvskb");
        $.ajax({
            url : '/FileUpload',
            type : 'POST',
            headers:{'token':token},
            data : formData,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success : function(data) {
                // console.log(data);
                // alert(data);
                alert("succefully data proessed")
                window.location.reload();
            }
        });
    }
        else{
        alert("invalid format");
        }
    }
    else{
        alert("Upload file");
    }
  })


  $("#logout").click(function(){
       
    $.ajax({
        url:"/User/LogOut",
        method:"GET",
        headers:{"token":token},
        cache:false,
        async:false,
        success(response){  
        }



    })
    window.open("/", "_self")
})