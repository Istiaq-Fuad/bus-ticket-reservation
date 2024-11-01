document.addEventListener("DOMContentLoaded", () => {
  let ref1Element = document.getElementById("ref1");
  let ref1 = ref1Element ? ref1Element.value : null;

  if (ref1) {
    setTimeout(() => {
      fetch(`/bus/ticket/api/${ref1}`)
        .then((response) => response.json())
        .then((ticket1) => {
          if (ticket1.status === "CONFIRMED") {
            document.querySelector(".section2 .flight1 .ref").innerText =
              ticket1.ref;
            document.querySelector(".section2 .flight1 .from1").innerText =
              ticket1.from;
            document.querySelector(".section2 .flight1 .to1").innerText =
              ticket1.to;
          } else {
            throw Error(ticket1.status);
          }
        })
        .then(() => {
          document.querySelector(".section1").style.display = "none";
          document.querySelector(".section2").style.display = "block";
          document.querySelector(".section3").style.display = "none";
          //document.querySelector(".section2 svg").style.animationPlayState = 'running';
        })
        .catch(() => {
          document.querySelector(".section1").style.display = "none";
          document.querySelector(".section2").style.display = "none";
          document.querySelector(".section3").style.display = "block";
        });
    }, 1000); // Adjust the timeout duration as needed
  } else {
    console.error("Element with ID 'ref1' not found or has no value.");
  }
});
