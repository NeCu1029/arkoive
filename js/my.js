const verifyStr = document.getElementById("verify-str");
const userID = document.querySelector("input");
const str = Math.random().toString(36).substring(2, 10);

verifyStr.innerText = str;

document.getElementById("verify-btn").addEventListener("click", () => {
  fetch("http://localhost:4000/verify")
    .then((response) => response.json())
    .then((data) => {
      let mes = data.message;
      console.log(mes);
      if (mes == str) {
        console.log("verification succeeded!");
      } else {
        console.log("verification failed.");
      }
    })
    .catch(() => {
      console.log("Error occured");
    });
});
