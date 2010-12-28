$(document).ready(function(){ 

    login();



// funtions
    //get the username and password
    function get_username_password () {
        // body...
        return{
            id: $("#user_id").val().trim(),
            sn: $("#password").val().trim()
        };
    }

    function login()
    {
        var $dialog = $('#login')
		.dialog({
			autoOpen: true,
			title: '使用饭否帐户登录'
		}); 

        $("#login_button").click(function(){
                
            $.get("/login", get_username_password(), function(data){ 
                var data=eval("("+data+")");
                if (data.screen_name)
                {
                    $dialog.dialog("close");
                }
                else{
                    alert(data.error);
                }

                });//login get end

            });//login_button end
		
    }//login end
});//end document
