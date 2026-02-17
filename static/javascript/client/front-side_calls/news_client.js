import { displayError } from "../index.js"

let current_page = 1;
const pagePer_art = 10;

//const isLoading = 90
//const QUERY = 'Philippines';

const CATEGORIES = document.getElementById("q"); 
const button = document.getElementById("btn");
const loading = document.getElementById("loading");
const cat_container = document.getElementById("categories");
const container = document.getElementById("news_header");
const btn = document.getElementById("btn-open");
const btn_close = document.getElementById("btn-close");

CATEGORIES.addEventListener("change", () => {
  current_page = 1;
 // loaded = false;
  fetching(current_page, true, false);
});


function toggleUI(isOpen) {
  cat_container.style.visibility = isOpen ? 'visible' : 'hidden';
  btn_close.style.visibility = isOpen ? 'visible' : 'hidden';
  btn.style.visibility = isOpen ? 'hidden' : 'visible';
}

// listeners
btn.onclick = () => toggleUI(true);
btn_close.onclick = () => toggleUI(false);

async function fetching(page = 1, clear = false, loaded = false) {
  //const QUERY = document.getElementById("q").value
 
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
    const fetched = await fetch(`/news?page=${page}&q=${CATEGORIES.value}`);
    const dat = await fetched.json(); 

    if (!fetched.ok) {
      let errorMessage = `Server Error ${fetched.status}`;
    
      if (dat.message) {
        errorMessage += `: ${dat.message}`;
      }
      throw new Error(errorMessage);
    }

    loading.innerHTML = ``;
    button.style.visibility = 'visible';
    btn.style.visibility = 'visible';
    btn_close.style.visibility = 'hidden'

   
   // CATEGORIES.style.visibility = 'visible';
   // cat_container.style.visibility = 'visible';
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
    
     if (data.articles && data.articles.length > 0) {

        data.articles.forEach(article => {

        const link = document.createElement("a");
        link.href = article.url; 
        link.className = "title";
        link.target = "_blank"; 
        link.textContent = article.title || 'Untitled Article';

        const heading = document.createElement("h3");
        heading.className = "heading";
        heading.append(link);

        const clickable = document.createElement('a');
        clickable.href = '/click';
       // clickable.target = "_blank"

        clickable.addEventListener("click", function(event) {
          event.preventDefault();
         
          sessionStorage.setItem('current_article', JSON.stringify({
            title: article.title,
            urlToTitle: article.url,
            urlToImage: article.urlToImage,
            description: article.description,
          }));
          /*
          const articleObj = {
            title: article.title,
            urlToTitle: article.url,
            urlToImage: article.urlToImage,
            description: article.description,
          };
          
          const articleJSON = JSON.stringify(articleObj);
          
          // write to both storages
          sessionStorage.setItem("current_article", articleJSON);
          localStorage.setItem("current_article", articleJSON);
          */

          window.location.href = clickable.href;
        });

        const image = document.createElement('img');
        image.className = "art_img";
        const img_src = article.urlToImage;

         if (img_src === null) {
            const img_err = document.createElement('p');
            img_err.className = 'imgERR';
            img_err.innerHTML = `Image not Available`;
            container.append(img_err);

         } else {
           image.src = img_src; 
           clickable.append(image); 
         }
        
        const details = document.createElement("p");
        details.className = "details";

        const source = document.createElement("small");
        source.className = "source";

        details.textContent = article.description || "No description available.";
        source.textContent =`Source: ${article.source.name || "Unknown"}`;

        const line = document.createElement("hr");
             
        container.append(heading, clickable, details, source, line);
        //container.append(details);
        //container.append(source);
        });
    } else {
     
    }
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
   let end_mssg = document.getElementById("end_message");
   //let totalRes = Math.ceil(data.totalResults / pagePer_art);

   console.log(data.totalResults);
   //console.log(totalRes);

   if (current_page === pagePer_art)  {
      const button = document.getElementById("btn");

      console.log("test");
      button.remove();
      end_mssg.textContent = 'You reached the end, come back later for more news';
   }
 }