configBox = document.getElementById("configBox");
configForm = document.getElementById("configForm");
configStatusHTML = document.getElementById("configStatus").innerHTML;
configButton = document.getElementById("goConfig");
configEntries = document.getElementById("configEntries");

costBox = document.getElementById("costbox");



function checkConfig(){

	configEntries.style.display = "none";
	if (configStatusHTML == "1"){
		while (configForm.firstChild) {
		    configForm.removeChild(configForm.firstChild);
		}
		while (configBox.firstChild) {
		    configBox.removeChild(configBox.firstChild);
		}
	}

}

checkConfig();

function formAppear(){
	configEntries.style.display = "";
}

configButton.addEventListener("click", formAppear);