const verifyDiv = document.querySelector(".verify");
const myDiv = document.querySelector(".my");
const verifyStr = document.getElementById("verify-str");
const userID = document.querySelector("input");
const str = Math.random().toString(36).substring(2, 10);

verifyStr.innerText = str;

function verifySucceed() {
  console.log("verification succeeded!");
  verifyDiv.setAttribute("class", "hidden");
  myDiv.removeAttribute("class", "hidden");
}

document.getElementById("verify-btn").addEventListener("click", () => {
  fetch("http://localhost:4000/verify", {
    method: "POST",
    body: JSON.stringify(userID.value),
  })
    .then((response) => response.json())
    .then((data) => {
      let mes = data.message;
      console.log(mes);
      if (mes == str) {
        verifySucceed();
      } else {
        console.log("verification failed.");
      }
    })
    .catch(() => {
      console.log("Error occured");
    });
});
