/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}




function showSpot(btn, spot){
	document.getElementById(btn).addEventListener("mouseover", function(){
		    var loc = document.getElementsByClassName(spot);
			 loc[0].style.display = "block";
		});
}


function hide(spot){
	document.getElementsByClassName(spot)[0].style.display = "none";
}



function hint(){
	var a = 1;
	document.getElementById("hint-btn").addEventListener("click", function(){
		    var btn = document.getElementsByClassName("hint" + a.toString());
			 btn[0].style.display = "block";
			 a +=1 ;
		});
}
