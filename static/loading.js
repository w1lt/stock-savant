/** @format */

// Get references to DOM elements
const loadButton = document.getElementById("loadButton");
const loadingScreen = document.getElementById("loadingScreen");
const content = document.getElementById("content");

// Add a click event listener to the button
loadButton.addEventListener("click", () => {
  // Show the loading screen
  loadingScreen.style.display = "flex";

  setTimeout(() => {
    // Hide the loading screen and display the content
    loadingScreen.style.display = "none";
    content.style.display = "block";
  }, 10000);
});
