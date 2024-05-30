$(document).ready(function() {
    $("#toolTemplateInputForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#toolTemplateInputForm").serializeArray();
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