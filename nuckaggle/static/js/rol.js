window.onload=init;
function init() {
	window.setInterval("start2()",1500);
}

var i=2;
function start2() {
	var imgobj=document.getElementById("rol");
	imgobj.src="../images/rol_"+i+".jpg";
    i++;
    if(i>3) i=1;
}