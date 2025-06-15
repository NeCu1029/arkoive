const verifyDiv = document.querySelector(".verify");
const myDiv = document.querySelector(".my");
const verifyStr = document.getElementById("verify-str");
const copyBtn = document.getElementById("copy");
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
        console.log("Verification failed");
      }
    })
    .catch(() => {
      console.log("Error occured");
    });
});

copyBtn.addEventListener("click", () => {
  navigator.clipboard
    .writeText(str)
    .then(() => {
      copyBtn.setAttribute("class", "copy-success");
      copyBtn.innerText = "복사 성공";
    })
    .catch(() => {
      copyBtn.setAttribute("class", "copy-failure");
      copyBtn.innerText = "복사 실패";
    });
});
