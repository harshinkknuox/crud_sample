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
                       
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                        window.location.href = response.redirect_url;
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


function FilterCurriculum(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_curriculum').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function() {},
        success: function(response) {
            $('#curriculum-tbody').html(response.template)
            $('#curriculum-pagination').html(response.pagination)
        },
    });
}



$(document).on('click', '.create_input_details', function(event) {
    event.preventDefault();

    var url = $(this).data('url');
    var prefix = $(this).data('prefix');
    console.log("prefix ===",prefix);
    var row = $(this).closest('.form_set_row');
    var tool = row.find('.tool-select').val();
    console.log("tool ===", tool);

    var placeHolder = $("#id_place_holder").val() || "";
    console.log("placeHolder ===", placeHolder);

    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {
            'tool': tool
        },
        beforeSend: function() {
            $('#inputdetails-form-div-' + prefix).html('Loading...');
        },
        success: function(response) {
            $('#inputdetails-form-div-' + prefix).html(response.template);
            $('#popup_head-' + prefix).html(response.title);
        },
    });
});


$(document).on('click', '.tooltemplate-input-submit', function(event) {
    event.preventDefault();

    var url = $(this).data('url');
    var prefix = $(this).data('prefix');
    var formData = [];
    $('.form_set_row').each(function() {
        var formRow = $(this);
        var toolInput = formRow.find('.tool-select').val() || "No Inputs";
        var placeHolder = formRow.find('#id_place_holder').val() || "None";
        var description = formRow.find('#id_description').val() || "None";
        var max_length = formRow.find('#id_max_length').val() || "None";
        var max_validation_msg = formRow.find('#id_max_validation_msg').val() || "None";
        var min_length = formRow.find('#id_min_length').val() || "None";
        var min_validation_msg = formRow.find('#id_min_validation_msg').val() || "None";
        var validation_message = formRow.find('.validation-message').val() || "None";
        var sort_order = formRow.find('.sort-order').val() || "None";

        console.log("formRow==",formRow)
        console.log("placeHolderss==",placeHolder)
        console.log("id_description===",description)
        console.log("toolInput==!",toolInput)

        formData.push({
            "toolInput": toolInput,
            "input_details":{
                "placeHolder": placeHolder,
                "description": description,
                "max_length": max_length,
                "max_validation_msg": max_validation_msg,
                "min_length": min_length,
                "min_validation_msg": min_validation_msg,},
            "validation_message": validation_message,
            "sort_order": sort_order,
        });
    });
    
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "POST",
        data: JSON.stringify(formData),
        dataType: "json",
        success: function(response) {
            alert('Saved')

            $('.add-inputdetails').each(function(){
                $(this).modal('hide');
            });
            
            $('#inputdetails-form-div-' + prefix).html(response.template);
            $('#popup_head-' + prefix).html(response.title);
        },
       
    });
});


$(document).ready(function() {
    $('#tool_input').change(function() {
        var tool_input_value = $(this).val();
        $.ajax({
            url: 'swift/viewstool_template', // replace with the actual URL for ToolTemplateView
            type: 'GET',
            data: {
                'tool_input': tool_input_value
            },
            success: function(response) {
                $('#additional_fields_container').html(response.additional_fields_html);
            },
            error: function(xhr, status, error) {
                console.error('An error occurred while fetching additional fields: ', xhr.responseText);
            }

        });
    });
});




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
                    $("#tooltemplate-input-submit").attr("disabled", "disabled");
                    $("#tooltemplate-input-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                       
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
                    $("#tooltemplate-input-submit").attr("disabled", false);
                    $("#tooltemplate-input-submit").val("Save");
                },
            });
        },
    });
});