$(document).ready(function() {
    $("#PromptForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#PromptForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#prompt-submit").attr("disabled", "disabled");
                    $("#prompt-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        FilterPrompt('')
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
                            $('#prompt-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#prompt-submit").attr("disabled", false);
                    $("#prompt-submit").val("Save");
                },
            });
        },
    });
});

function FilterPrompt(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_prompt').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function() {},
        success: function(response) {
            $('#prompt-tbody').html(response.template)
            $('#prompt-pagination').html(response.pagination)
        },
    });
}

$(document).on('click', '#create_prompt', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#prompt-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#prompt-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})
$(document).on('click', '.prompt-edit', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#prompt-form-div').html('Loading...')
        },
        success: function(response) {
            $('#prompt-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})

$(document).on('click', '#prompt-out-add', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#prompt-out-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#prompt-out-form-div').html(response.template)
            $('#popup_out_head').html(response.title)
        },
    });
})


// Function to delete curriculum
function DeleteCurriculum(id) {
    var url = '/curriculum/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this record?",
        buttons: true,
        dangerMode: true,
    }).then(function(okey) {
        if (okey) {
            $.ajax({
                url: url,
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                method: "POST",
                data: {},
                beforeSend: function() {},
                success: function(response) {
                    if (response.status) {
                        $(".msg_desc").text(response.message);
                        $("#flash_message_success").attr("style", "display:block;");
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;");
                        }, 3500);
                        FilterPrompt('')
                    }
                },
            });
        }
    });
}