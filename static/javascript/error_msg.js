export async function err_message(text, style, container) {
      
       container.innerHTML = "";

       const alert = document.createElement("div");
       alert.className = `alert alert-${style}`
       alert.role = 'alert';
       alert.innerHTML = ` ${text} 
       <button type="button" class="close-btn" 
          style="float: right; background: none; border: none; width: 10px; height: 10px;" "aria-label="Close">
          <img src="/static/imageors/close.png" style="width: 15px; height: 15px;"> 
       </button>`;

       container.appendChild(alert);
   
       const close = alert.querySelector(".close-btn");
             close.addEventListener("click", () => {
             alert.remove();
       });

       setTimeout(() => {
            alert.remove();
            }, 5000);
} 

