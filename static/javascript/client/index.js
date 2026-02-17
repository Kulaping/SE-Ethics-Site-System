var navbar = document.getElementById("show");
var footer = document.getElementById("futah");

footer.style.position = "fixed";
footer.style.bottom = "0";
footer.style.width= "100%";

window.addEventListener("scroll", () => {
 if (window.scrollY > 10) {
     navbar.style.position = "fixed";
     navbar.style.top = "0";
   
 } else {
    navbar.style.position = "static";
    
}
});

 export function displayError(message) {
   const main_container = document.getElementById("news_header");
   const cat_container = document.getElementById("categories");
   const image_url = "/static/imageors/img_errmess.webp";
  
   if (main_container && cat_container) {
       main_container.innerHTML = "";
       cat_container.innerHTML = "";

       const button = document.getElementById("btn");
       if (button) {
           button.style.display = 'none';
       } 
   }
   
       const err_container = document.createElement('div');
       err_container.className = "err_container";

       const err_message = document.createElement('p');
       err_message.className = "err_message";
       err_message.innerHTML = message;
      
       const error_img = document.createElement('img');
       error_img.className = "error_style"; 
       error_img.src = image_url;

       err_container.append(error_img, err_message);

       main_container.append(err_container);
}