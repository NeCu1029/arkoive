const verifyStr = document.getElementById("verify-str");
const str = Math.random().toString(36).substring(2, 10);

verifyStr.innerText = str;

document.getElementById("verify-btn").addEventListener("click", () => {
  fetch("http://localhost:4000/verify")
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
