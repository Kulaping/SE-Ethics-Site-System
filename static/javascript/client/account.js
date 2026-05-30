//import { loadUser} from "../helper/accountCredentials.js";
async function userData() {
  //let user = {};
  const user = await fetch("/user_info"); 
  console.log(user);
  const response = await user.json();

  if (!user.ok) {
     console.log(response.error);
     document.getElementById("name").innerHTML = "Go log-in";
     document.getElementById("buttons").innerHTML = "";
     return;
  }

  //const response = user.json();
  console.log(response);
  console.log(response.username);
  console.log(response.fav_cat);

  deleteAcc(response.username);

}
userData();

const logout_btn = document.getElementById("log-out");

function removeRedirect() {
 // localStorage.removeItem("token");
  window.location.href = "/log-in";
}

logout_btn.addEventListener("click", (event) => {
  event.preventDefault();
  removeRedirect();
});


function deleteAcc(username) {
  const mssgContainer_test = document.createElement("div");
  const message = document.createElement("p");
  const yesBtn = document.createElement("button");
  const noBtn = document.createElement("button");
  console.log(yesBtn, noBtn);

  const deleteACC = document.getElementById("deleteAcc");
  deleteACC.addEventListener("click", (event) => {
    event.preventDefault();

    console.log("test");
    yesBtn.innerText = `YES`;
    noBtn.innerText = `NO`;
    //this is just for testing:
    console.log(message);
    message.innerText = `Are you sure you want to delete your Account?`;

    mssgContainer_test.append(message, yesBtn, noBtn);

    document.body.appendChild(mssgContainer_test);
  });

  yesBtn.addEventListener("click", async () => {
    console.log(username);
    const userID = username;
    const confirm_delete = true;

    try {
      const response = await fetch("/deleteAcc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirm_delete, userID }),
      });
      //removeRedirect();]
      const data = await response.json();
      console.log(data.res);
    } catch (error) {
      console.log(error);
    } finally {
      removeRedirect();
    }
  });
}