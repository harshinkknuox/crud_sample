$(document).ready(function() {
    $("#TemplateToolForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#TemplateToolForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#template-tool-submit").attr("disabled", "disabled");
                    $("#template-tool-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)

                        // Clear the form fields
                        $("#TemplateToolForm")[0].reset();
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
                            $('#template-tool-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#template-tool-submit").attr("disabled", false);
                    $("#template-tool-submit").val("Save");
                },
            });
        },
    });
});




// 
// $(document).on('click', '.tooltemplate-input-submit', function(event) {
//     event.preventDefault();

//     var url = $(this).data('url');
//     var prefix = $(this).data('prefix');
//     var formData = [];
//     formData[prefix] = {};
//     $('.form_set_row').each(function() {
//         var formRow = $(this);
//         var rowId = formRow.attr('id');
//         if (!rowId) {
//             rowId = 'row_' + Math.random().toString(36).substr(2, 9);
//             formRow.attr('id', rowId); 
//         }

        
//         var toolInput = formRow.find('.tool-select').val() || "No Inputs";
//         var placeHolder = formRow.find('#id_place_holder').val() || "None";
//         var description = formRow.find('#id_description').val() || "None";
//         var max_length = formRow.find('#id_max_length').val() || "None";
//         var max_validation_msg = formRow.find('#id_max_validation_msg').val() || "None";
//         var min_length = formRow.find('#id_min_length').val() || "None";
//         var min_validation_msg = formRow.find('#id_min_validation_msg').val() || "None";
//         var validation_message = formRow.find('.validation-message').val() || "None";
//         var sort_order = formRow.find('.sort-order').val() || "None";

//         console.log("formRow==", formRow);
//         console.log("placeHolderss==", placeHolder);
//         console.log("id_description===", description);
//         console.log("toolInput==!", toolInput);
        
//         formData[prefix][rowId] ={
//             "toolInput": toolInput,
//             "input_details": {
//                 "placeHolder": placeHolder,
//                 "description": description,
//                 "max_length": max_length,
//                 "max_validation_msg": max_validation_msg,
//                 "min_length": min_length,
//                 "min_validation_msg": min_validation_msg,
//             },
//             "validation_message": validation_message,
//             "sort_order": sort_order,
//         };

//     });

//     $.ajax({
//         url: url,
//         headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
//         method: "POST",
//         data: JSON.stringify(formData),
//         contentType: "application/json",
//         dataType: "json",
//         success: function(response) {
//             alert('Saved');

//             $('.add-inputdetails').each(function() {
//                 $(this).modal('hide');
//             });

//             $('#inputdetails-form-div-' + prefix).html(response.template);
//             $('#popup_head-' + prefix).html(response.title);
//         },
//         error: function(xhr, status, error) {
//             console.error('Error:', error);
//             console.log('Response:', xhr.responseText);
//         }
//     });
// });

// 