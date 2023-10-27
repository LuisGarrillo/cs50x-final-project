function checkConfirmation(event) {
    let confirm = document.querySelector("#confirmation");
    let password = document.querySelector("#password");
    if (confirm.value != password.value) {
        let listener = document.querySelector("#confirmation-listener");
        listener.innerHTML = `<p>Passwords do not match</p>`;

        let button = document.querySelector("#register");
        button.disabled = true;
    }
    else {
        let listener = document.querySelector("#listener");
        listener.innerHTML = "";

        let button = document.querySelector("#register");
        button.disabled = false;
    }
}


document.addEventListener('DOMContentLoaded', function() {
    let password = document.querySelector("#password");

    confirm.addEventListener('input', checkConfirmation);
});