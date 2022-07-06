function PasswordToggle(PasswordID)
{
    var checkboxId = document.getElementById('show_password');
    var passId = document.getElementById(PasswordID)
    if(checkboxId.checked == true)
    {
        passId.type = "text";
    }

    else
    {
        passId.type = "password";
    
    }
}