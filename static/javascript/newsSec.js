let username;
let article_data;
let article;
const token = localStorage.getItem("token");

async function loadUser() {
  const accStat = document.getElementById("username");
  const res = await fetch("/accounts", {
    headers: { Authorization: `Bearer ${token}` },
  });
  console.log(res);
  const data = await res.json();
  username = data.username;
  console.log(data);

  if (!data.ok) {
    accStat.innerHTML = `Login or sign up to post a comment.`;
    console.log(data.error);
    console.log("token log");

    const input = document.getElementById("user-input").value.trim();
    const button = document.getElementById("btn");
    console.log("Token not found");
    input.disabled = true;
    button.disabled = true;
    document.getElementById("no-token").innerHTML = `pls log in to comment`;

    //return;
  } else {
    console.log(data.username);
    accStat.innerHTML = `Welcome, ${data.username}`;
  }
}
loadUser();

//document.addEventListener('DOMContentLoaded', function() {

try {
  article_data =
    sessionStorage.getItem("current_article") ||
    localStorage.getItem("current_article");
  console.log(`unparsed: ${article_data}`);
  /*
    article_data.forEach("object", () => {
    console.log(`Fall for:${object.urlToTitle}`);
    });
     
    */
  if (article_data) {
    article = JSON.parse(article_data);
    console.log(`parsed: ${article}`);
    console.table(article);

    document.getElementById("title").innerHTML = article.title;
    document.getElementById("source").href = article.urlToTitle;
    document.getElementById("img").src = article.urlToImage;
    document.getElementById("description").innerHTML = article.description;
  } else {
    document.getElementById("title").textContent =
      "Article Not Found or Data Expired.";
  }
} catch (error) {
  console.log(error);
}
//});

const comment_count = [];

//TESTINGGGGGGG::

//const articleURL = article.urlToTitle;
console.log(`Test: ${article.urlToTitle}`);

function Comments_style(Username, comment, timestamp) {
  // const total_comments = document.getElementById("total-comments");
  const result_container = document.getElementById("results");
  const user = document.createElement("div");

  user.className = "user";

  user.innerHTML = `
    <h1 class="name">${Username}</h1>
    <p class="time">${comment}</p>
    <p class="text">${timestamp}</p>
    `;
  result_container.append(user, document.createElement("br"));
}

let nameClick = "";
let ObjectClick = "";
let timeClick = "";

async function commentValues() {
  try {
    const response = await fetch(
      `/display-comments?article=${encodeURIComponent(article.urlToTitle)}`
    );
    const data = await response.json();

    console.log(data);
    data.forEach((Object) => {
      console.log(Object);

      nameClick = Object.username;
      ObjectClick = Object.comment;
      timeClick = Object.timestamp;

      Comments_style(nameClick, ObjectClick, timeClick);
    });
  } catch (error) {
    console.log(error);
  }
}
commentValues();

const button = document.getElementById("btn");

button.addEventListener("click", async (event) => {
  event.preventDefault();
  const input = document.getElementById("user-input").value.trim();
  if (input === "") return;

  const commentPer_art = {
    comment: input,
    specific_article: article.urlToTitle,
  };

  localStorage.setItem("comment_perArticle", JSON.stringify(commentPer_art));

  const result = JSON.parse(localStorage.getItem("comment_perArticle"));

  console.log(result);
  console.log(result.specific_article);

  const post_data = await fetch("/post-comments", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },

    // body: JSON.stringify({input}),
    body: JSON.stringify(result),
  });

  const personCOM = await post_data.json();
 // console.log(personCOM.username, personCOM.user_comment, personCOM.timestamp);
  Comments_style(personCOM.username, personCOM.user_comment, personCOM.timestamp);
});