

// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById('imageEdit');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
var firstPhoto=document.getElementById('firstPhoto');
var secondPhoto=document.getElementById('secondPhoto');
var thirdPhoto=document.getElementById('thirdPhoto');
firstPhoto.onclick=function(){
  var img=document.getElementsByClassName("imagineEveniment")[0];
  img.style.display="block";
  img=document.getElementsByClassName("imagineEveniment2")[0];
  img.style.display="none";
  img=document.getElementsByClassName("imagineEveniment3")[0];
  img.style.display="none";
  firstPhoto.style.backgroundColor = "blue";
  secondPhoto.style.backgroundColor="gray";
  thirdPhoto.style.backgroundColor="gray";
}


secondPhoto.onclick=function(){
  var img=document.getElementsByClassName("imagineEveniment")[0];
  img.style.display="none";
  img=document.getElementsByClassName("imagineEveniment2")[0];
  img.style.display="block";
  img=document.getElementsByClassName("imagineEveniment3")[0];
  img.style.display="none";
  secondPhoto.style.backgroundColor = "blue";
  firstPhoto.style.backgroundColor = "gray";
  thirdPhoto.style.backgroundColor="gray";

}


thirdPhoto.onclick=function(){
  var img=document.getElementsByClassName("imagineEveniment")[0];
  img.style.display="none";
  img=document.getElementsByClassName("imagineEveniment2")[0];
  img.style.display="none";
  img=document.getElementsByClassName("imagineEveniment3")[0];
  img.style.display="block";
  thirdPhoto.style.backgroundColor="blue";
  firstPhoto.style.backgroundColor="gray";
  secondPhoto.style.backgroundColor="gray";

}


