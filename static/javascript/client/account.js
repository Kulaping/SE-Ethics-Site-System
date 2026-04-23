import { loadUser, token} from "../helper/accountCredentials.js";

async function userData() {
  let user = {};
  user = await loadUser();
  const username = user.username;

  if (!username) {
    console.log("No User Token");
    document.getElementById("name").innerHTML = "Go log-in";
    document.getElementById("buttons").innerHTML = "";
    return;
  }
  deleteAcc(username);

  const user_data = await fetch("/user_info",
    {
      method: "GET",
      headers: { "Authorization": `Bearer: ${token}`
    }
  });

  const user_info = await user_data.json();
  console.log(user_info.preferred_category);
}
userData();

const logout_btn = document.getElementById("log-out");
console.log(token);

function removeRedirect() {
  localStorage.removeItem("token");
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
