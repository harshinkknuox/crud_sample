$(document).ready(function() {
    $("#InputDetailsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#InputDetailsForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#tooltemplate-submit").attr("disabled", "disabled");
                    $("#tooltemplate-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        FilterCurriculum('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                    } else {
                        alert('ho')
                        if ('message' in response ){
                            $(".carousel__button").click()
                            $(".msg_desc").text(response.message)
                            $("#flash_message_error").attr("style", "display:block;")
                            setTimeout(function() {
                                $("#flash_message_error").attr("style", "display:none;")
                            }, 3500)                                                       
                        } else {     
                            alert('form')                    
                            $('#inputdetails-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#tooltemplate-submit").attr("disabled", false);
                    $("#tooltemplate-submit").val("Save");
                },
            });
        },
    });
});


$(document).on('click', '#create_input_details', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#inputdetails-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#inputdetails-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})
















// document.addEventListener("DOMContentLoaded", function() {
//     const form = document.getElementById('toolTemplateForm');
    
//     form.addEventListener('submit', function(event) {
//         event.preventDefault();
        
//         const formData = new FormData(form);
//         const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
//         fetch(form.action, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': csrfToken,
//                 'X-Requested-With': 'XMLHttpRequest'
//             },
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status) {
//                 alert(data.message);
//                 // Optionally, you can redirect or update the page content here
//             } else {
//                 // Handle validation errors
//                 const formErrors = data.form_errors;
//                 const inpFormErrors = data.inp_form_errors;
                
//                 // Clear existing error messages
//                 const errorElements = document.querySelectorAll('.errorlist');
//                 errorElements.forEach(el => el.remove());
                
//                 // Display new error messages
//                 for (const [field, errors] of Object.entries(formErrors)) {
//                     const fieldElement = document.querySelector(`[name=${field}]`);
//                     if (fieldElement) {
//                         const errorList = document.createElement('ul');
//                         errorList.classList.add('errorlist');
//                         errors.forEach(error => {
//                             const errorItem = document.createElement('li');
//                             errorItem.textContent = error;
//                             errorList.appendChild(errorItem);
//                         });
//                         fieldElement.parentElement.appendChild(errorList);
//                     }
//                 }
                
//                 for (const [field, errors] of Object.entries(inpFormErrors)) {
//                     const fieldElement = document.querySelector(`[name=${field}]`);
//                     if (fieldElement) {
//                         const errorList = document.createElement('ul');
//                         errorList.classList.add('errorlist');
//                         errors.forEach(error => {
//                             const errorItem = document.createElement('li');
//                             errorItem.textContent = error;
//                             errorList.appendChild(errorItem);
//                         });
//                         fieldElement.parentElement.appendChild(errorList);
//                     }
//                 }
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//     });
// });