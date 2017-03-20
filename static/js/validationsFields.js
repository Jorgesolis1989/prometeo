/**
 * Created by martha on 5/03/17.
 */

function showPassword() {
    var x = document.getElementById("demo-form-checkbox").checked;
    if (x)
    {
        document.getElementById("passwordA").type = 'text';
        document.getElementById("passwordN").type = 'text';
        document.getElementById("passwordC").type = 'text';
    }
    else
        {
            document.getElementById("passwordA").type = 'password';
            document.getElementById("passwordN").type = 'password';
            document.getElementById("passwordC").type = 'password';
        }
}
