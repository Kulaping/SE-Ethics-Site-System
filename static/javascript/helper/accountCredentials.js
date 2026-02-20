export const token = localStorage.getItem("token");

export async function loadUser() {

    const res = await fetch("/accounts", {
         headers: { Authorization: `Bearer ${token}` },
     });

     const data = await res.json();
     console.log(data);
 
     if (!data.ok) {
         return {"bool": false, "username": ""};
     
     } else {
       //console.log(data.username)
       return {"bool": true, "username": data.username};
     }
 
 //   return bool = true;
}

loadUser();