$(document).ready(function() {
    $('select').material_select();
    $('.collapsible').collapsible();

    

    



    $('#password_retype_input').blur(function() {
        var text_password = $('#id_password').val();
        var password_retype = $('#password_retype_input').val();
        
        if(text_password == password_retype ){   

            $('#id_password').addClass("validate")
            $("#password_retype_input").addClass("validate")            
            $("#password_retype_input").next("label").attr('data-success','Passwords match');
             
        }

        if(text_password != password_retype ){            

            $('#id_password').addClass("invalid")
            $("#password_retype_input").addClass("invalid")            
            $("#password_retype_input").next("label").attr('data-error','Passwords do not match');            
        }        
    });

    $('#btn_create_backups_submit').click(function() {
        

        var selecteditems = [];
        var json_var = {}

        $("#create_backups_form").find("input:checked").each(function (i, ob) { 
            selecteditems.push($(ob).val());             
        });       
        
        var string_selecteditems = selecteditems.toString();


        $.ajax({
           type: 'get',
           data: {'selecteditems' : string_selecteditems },
           dataType: "json",          
           url:"create_backups/", 
           async: false,          
           success: function(res){             
             alert(res.message)             
           }                 
        });

        


    });




    

    



});