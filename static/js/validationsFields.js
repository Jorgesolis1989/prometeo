/**
 * Created by martha on 5/03/17.
 */

function showPassword() {
    var x = document.getElementById("demo-form-checkbox").checked;
    alert(x)
    if (document.getElementById("demo-form-checkbox").checked = true)
    {
        document.getElementById("passwordA").type = 'text';
        document.getElementById("passwordN").type = 'text';
        document.getElementById("passwordC").type = 'text';
    }
    else
        if (document.getElementById("demo-form-checkbox").checked = false)
        {
            document.getElementById("demo-form-checkbox").checked = false;
            document.getElementById("passwordA").type = 'password';
            document.getElementById("passwordN").type = 'password';
            document.getElementById("passwordC").type = 'password';
        }

}
