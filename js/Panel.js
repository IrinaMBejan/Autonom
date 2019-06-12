// JavaScript source code
function myFunction() {
    var input, filter, ul, li, caut, i, j, txtValue, dis;
    input = document.getElementById("myInput");

    filter = input.value.toUpperCase();


    ul = document.getElementsByClassName("list-requests");
    li = ul[0].getElementsByTagName("li");


    for (i = 0; i < li.length; i++) {
        caut = li[i].querySelectorAll(".user, .field, .modification");

        dis = false;

        for (j = 0; j < caut.length; j++) {
            txtValue = caut[j].textContent || caut[j].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                dis = true;
            }
        }

        if (dis) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }

}