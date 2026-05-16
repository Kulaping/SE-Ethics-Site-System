import { displayError } from "../index.js"

let current_page = 1;
const pagePer_art = 10;

const button = document.getElementById("btn");
const loading = document.getElementById("loading");
const cat_container = document.getElementById("categories");
const container = document.getElementById("news_header");
const btn = document.getElementById("btn-open");
const btn_close = document.getElementById("btn-close");

function toggleUI(isOpen) {
  cat_container.style.visibility = isOpen ? 'visible' : 'hidden';
  btn_close.style.visibility = isOpen ? 'visible' : 'hidden';
  btn.style.visibility = isOpen ? 'hidden' : 'visible';
}

// listeners
btn.onclick = () => toggleUI(true);
btn_close.onclick = () => toggleUI(false);

const CATEGORIES = document.getElementById("q"); 

CATEGORIES.addEventListener("change", () => {
  current_page = 1;
 // loaded = false;
  fetching(current_page, true, false);
});

async function fetching(page = 1, clear = false, loaded = false) {
  const QUERY = CATEGORIES.value;
  console.log(`Preffered Category: ${QUERY}`);
  const none = CATEGORIES;
  const token = localStorage.getItem("token");
  console.log(token);

  if (clear) {
     container.innerHTML = "";
  }
  
   loaded = true;
   loading.innerHTML = `Loading news....`;
   button.style.visibility = 'hidden';
   btn.style.visibility = 'hidden';
   btn_close.visibility = 'hidden';
   cat_container.style.visibility = 'hidden';

  try {
    let url = `/news?page=${page}&section=${QUERY}`;
    console.log(none);
    
    const fetched = await fetch(url, 
      {
       method: "GET",
       headers: { "Authorization": `Bearer: ${token}`
      }
    });
    console.log(fetched);

    if (!fetched.ok) {
      let errorMessage = `Server Error ${fetched.status}`;
      console.error(`Error fetching news: ${errorMessage}`);
      /*
      if (dat.message) {
        errorMessage += `: ${dat.message}`;
      }
      throw new Error(errorMessage);
      */
    }

    const dat = await fetched.json(); 

   /*
    if (!dat.status) {
      displayError(`${dat.message}`);
      console.error(`Category Doesn't Exist.`)
    }
  */

    loading.innerHTML = ``;
    button.style.visibility = 'visible';
    btn.style.visibility = 'visible';
    btn_close.style.visibility = 'hidden';
    
    console.log(dat);
    display(dat);
    getNew(dat);

  } catch (error) {
    console.log(error.message);
    displayError("Sorry, we couldn't load the news right now. Please try again later.");
 
  } finally {
    loaded = false;
  }
}
fetching(1);

function display(data) {
     const container = document.getElementById("news_header");
    
    //if (data.articles && data.articles.length > 0) {

        data.response.results.forEach(article => {

        const link = document.createElement("a");
        link.href = article.webUrl; 
        link.className = "title";
        link.target = "_blank"; 
        link.textContent = article.webTitle || 'Untitled Article';

        const heading = document.createElement("h3");
        heading.className = "heading";
        heading.append(link);

        const clickable = document.createElement('a');
        clickable.href = '/click';
       // clickable.target = "_blank"

        clickable.addEventListener("click", function(event) {
          event.preventDefault();
         
          sessionStorage.setItem('current_article', JSON.stringify({
            title: article.webTitle,
            urlToTitle: article.webUrl,
            urlToImage: article.fields.thumbnail,
            description: article.fields.body,
          }));
         
          window.location.href = clickable.href;
        });

        const image = document.createElement('img');
        image.className = "art_img";

        if (article.fields && article.fields.thumbnail) {
            const img_src = article.fields.thumbnail;
            image.src = img_src; 
            clickable.append(image);
    
        } else {
          const img_err = document.createElement('p');
          img_err.className = 'imgERR';
          img_err.innerHTML = `Image not Available`;
          container.append(img_err);
        }
        
        const details = document.createElement("p");
        details.className = "details";

        //const source = document.createElement("small");
        //source.className = "source";

        details.innerHTML = article.fields.trailText || "No description available.";
        //source.textContent =`Source: ${article.source.name || "Unknown"}`;

        const line = document.createElement("hr");
             
        container.append(heading, clickable, details, line);
        //container.append(details);
        //container.append(source);
        });
    }


let isLoading = false;
 
  button.addEventListener("click", () => {
      if (isLoading) return;
          isLoading = true;
    //  document.addEventListener("DOMContentLoaded", () => {
        current_page++;
        fetching(current_page, false);
              
        setTimeout(() => { 
          isLoading = false; 
        }, 1500);
   });

 function getNew(data) {

   if (current_page === pagePer_art)  {
      const button = document.getElementById("btn");

      console.log("test");
      button.remove();
      end_mssg.textContent = 'You reached the end, come back later for more news';
   }
 }