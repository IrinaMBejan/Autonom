// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById('addLink');

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
    var divToHide=document.getElementsByClassName("atentie")[0];
divToHide.style.display="none";
var divToHide=document.getElementsByClassName("atentie2")[0];
divToHide.style.display="none";

  }
}

// add links
function addLink(){
  event.preventDefault();
    var linkText=document.getElementById("textLink").value;
    // var tagText=document.getElementById("textTags").value;
    if ((linkText==='' || linkText==null) ) //&& (tagText==='' || tagText===null))
    {
      var divToShow=document.getElementsByClassName("atentie")[0];
      divToShow.style.display="block";
      // var divToShow2=document.getElementsByClassName("atentie2")[0];
      // divToShow2.style.display="block";

    }
    else if(linkText==='' || linkText===null)
    {
      // alert("Nu ai completat!");
      var divToShow=document.getElementsByClassName("atentie")[0];
      divToShow.style.display="block";
  }
  //  else if (tagText==='' || tagText===null)
  //  {
  //   var divToShow=document.getElementsByClassName("atentie2")[0];
  //   divToShow.style.display="block";
  //  }
    else {
      var divToHide=document.getElementsByClassName("atentie")[0];
      divToHide.style.display="none";
      // var divToHide=document.getElementsByClassName("atentie2")[0];
      // divToHide.style.display="none";
      var requestArray=document.getElementsByClassName("request");
      var node = document.createElement("LI");
      node.classList.add("request");
       var span=document.createElement("span");
       span.classList.add("field");
       var text=document.createTextNode("Link");
       span.appendChild(text);
       var input=document.createElement("input");
      input.type = "text";
      input.name="textLink"+requestArray.length+1;
      input.value=document.getElementById("textLink").value;
      input.classList.add("modification");
      var btn=document.createElement("button");
      btn.type="button";
      btn.classList.add("reject");
       var i=document.createElement("i");
       i.classList.add("fas");
       i.classList.add("fa-times");
    document.getElementsByClassName("list-requests")[0].appendChild(node);
    var requestArray=document.getElementsByClassName("request");
    document.getElementsByClassName("request")[requestArray.length-1].appendChild(span);
    document.getElementsByClassName("request")[requestArray.length-1].appendChild(input);
    document.getElementsByClassName("request")[requestArray.length-1].appendChild(btn);
    document.getElementsByClassName("reject")[requestArray.length-1].appendChild(i);
    }
}

function hide(){
var divToHide=document.getElementsByClassName("atentie")[0];
divToHide.style.display="none";
// var divToHide=document.getElementsByClassName("atentie2")[0];
// divToHide.style.display="none";

}