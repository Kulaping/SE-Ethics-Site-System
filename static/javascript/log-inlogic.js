import { submitAuth } from "./auth.js";
import { err_message } from "./error_msg.js";

const alertContainer = document.getElementById("alert-container");

async function login_Btn() {
     const username = document.getElementById("get_user");
     const password = document.getElementById("get_password");

     const dat = await submitAuth("/log-in_logic", username.value, password.value);

     if (dat.ok) {
         localStorage.setItem("token", dat.token);
         window.location.href = '/click';  

     } else {
        err_message("Invalid Credentials", "danger", alertContainer);

        const inputs = [username, password];
        inputs.forEach(inputs => {
              inputs.style.border = "2px solid red";
        });
      }
}

document.getElementById("login_btn").addEventListener("click", login_Btn);