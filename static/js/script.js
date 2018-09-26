$(document).ready(function() {
    $('select').material_select();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.modal').modal();



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


    $('a.btn-play-function').click(function() {
        var id_object = $(this).attr('id');
        var id_course = id_object.substring(9, (id_object.length));

        $.ajax({
           type: "get",
           data:{'id_course':id_course},
           url:"play_container/",
           async: false,
           success:function(res){
             alert(res.message);
           },
         });



       });

     $('a.btn-stop-function').click(function() {
        var id_object = $(this).attr('id');
        var id_course = id_object.substring(9, (id_object.length));

        $.ajax({
           type: "get",
           data:{'id_course':id_course},
           url:"stop_container/",
           async: false,
           success:function(res){
             alert(res.message)
           },
         });

       });


    $('a.btn-remove-function').click(function() {
        if (window.confirm("If you delete this container his database will be erased too.")) {
            var id_object = $(this).attr('id');
            var id_course = id_object.substring(11, (id_object.length));

            $.ajax({
               type: "get",
               data:{'id_course':id_course},
               url:"remove_container/",
               async: false,
               success:function(res){
                 alert(res.message);
               },
             });

        }

      });

    $('a.btn-logs-function').click(function() {
        var id_object = $(this).attr('id');
        var id_course = id_object.substring(9, (id_object.length));

        $.ajax({
           type: "get",
           data:{'id_course':id_course},
           url:"logs_container/",
           async: false,
           success:function(res){
             alert(res.message);
           },
         });

    });


    $('.rubric_problem_class').click(function() {
        var result = ($(this).attr('id')).split("_");
        var contest_id = result[3];
        var problem_id = result[5];

        $.ajax({
           type: 'get',
           data: { 'problem_id': problem_id },
           dataType: "json",
           url:"check_rubric/",
           async: false,
           success: function(res){
             if (res.exists=='true'){
             $('#rubricform_terminal_objetive_'+contest_id+'_'+problem_id).val(res.terminal_objetive);
             $('#rubricform_activity_'+contest_id+'_'+problem_id).val(res.activity);
             $('#rubricform_weight_'+contest_id+'_'+problem_id).val(res.weight);
             $('#rubricform_approved_'+contest_id+'_'+problem_id).val(res.approved);
             $('#rubricform_not_approved_'+contest_id+'_'+problem_id).val(res.notapproved);
            }
           }
        });



    });



    $('.btn_rubricform').click(function() {
        var result = ($(this).attr('id')).split("_");
        var id_contest = result[1];
        var id_problem = result[2];
        var terminal_objetive = $('#rubricform_terminal_objetive_'+id_contest+'_'+id_problem).val();
        var activity = $('#rubricform_activity_'+id_contest+'_'+id_problem).val();
        var weight = $('#rubricform_weight_'+id_contest+'_'+id_problem).val();
        var approved = $('#rubricform_approved_'+id_contest+'_'+id_problem).val();
        var notapproved = $('#rubricform_not_approved_'+id_contest+'_'+id_problem).val();


        $.ajax({
           type: 'get',
           data: {
            'id_contest' : id_contest,
            'id_problem' : id_problem,
            'terminal_objetive' : terminal_objetive,
            'activity' : activity,
            'weight' : weight,
            'approved': approved,
            'notapproved': notapproved,
            },
           dataType: "json",
           url:"save_rubric/",
           async: false,
           success: function(res){
             alert(res.message)
           }
        });

    });


});