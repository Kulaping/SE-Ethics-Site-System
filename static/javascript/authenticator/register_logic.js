import { submitAuth } from "../helper/auth_helper.js";
import { err_message } from "../error_msg.js";

const username = document.getElementById("get_user");
const password = document.getElementById("get_password");
const userReg = /^[A-Za-z0-9_\-@]{4,17}$/;
const passReg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

const alertContainer2 = document.getElementById("alert-container");

const all = [username, password];
all.forEach(inputs => {
   inputs.addEventListener("input", () => {
      let validName = true;
      let validPass = true;

       if (inputs === username) { 
           validName = userReg.test(username.value);
       
       } else if (inputs === password) {
           validPass = passReg.test(password.value);
       }

       if (inputs === username && validName || inputs === password && validPass) {
           inputs.style.border = "2px solid green";
       } else {
           inputs.style.border = "2px solid red";
       }
     });
 });


async function register_Btn(event) {
     event.preventDefault();
     
     const username = document.getElementById("get_user");
     const password = document.getElementById("get_password");
    
     const dat = await submitAuth("/register_logic", username.value, password.value);
     console.log(dat);
    // console.log(dat.message);

     if (username.value == "" || password.value === "") {
        err_message("Please fill the requirements.", "danger", alertContainer2);
        return;
     }
     
     
     if (!dat.userinputLine) {
         username.style.border = "2px solid red";      
     }
     
     if (!dat.ok) {
         err_message(dat.log, "danger", alertContainer2);
         return;

     } else {
         console.log(dat.ok);
         localStorage.setItem("token", dat.token);
         const newsSession = sessionStorage.getItem("current_article");

         console.log(newsSession);
         window.location.href = "/click";  
     }
}

document.addEventListener("DOMContentLoaded", () => {
   document.getElementById("register_btn").addEventListener("click", register_Btn);
});  