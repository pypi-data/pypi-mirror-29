
document.crdist = {};
document.crdist.dist_event = new CustomEvent("load_district");
document.crdist.canton_event = new CustomEvent("load_canton");

function loadDoc(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
    	obj = JSON.parse(xhttp.responseText);
     	document.getElementById(obj['id']).innerHTML = obj['content'];
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
} 


function load_canton(obj_sel, initial){
	name=obj_sel.name.replace("province_", '');
	url = document.getElementById('div_canton_' + name).getAttribute("href");
	document.getElementById('div_district_' + name).innerHTML = "";
	url = url + '&province='+obj_sel.value;
	if (initial != undefined){
		url = url + "&initial="+initial;
	}
	loadDoc(url);
	document.canton_crdist = { "dist": 'div_district_' + name,
		"canton": 'div_canton_' + name };
	document.dispatchEvent(document.crdist.canton_event);
}



function KeySimulation(identificator) {
	var e = document.createEvent("KeyboardEvent");
	if (e.initKeyboardEvent) {  // Chrome, IE
		e.initKeyboardEvent("keyup", true, true, document.defaultView, "Enter", 0, "", false, "");
	} else { // FireFox
    e.initKeyEvent("keyup", true, true, document.defaultView, false, false, false, false, 13, 0);
	}
	document.getElementById(identificator).dispatchEvent(e);
}

function district_change(e){
	
	var selid = this.id.split('_')
	var name = selid[selid.length-1];
	var text = "Costa Rica, ";
	var sel = document.getElementById("id_province_" + name);
	text += sel.options[sel.selectedIndex].text;
	var sel = document.getElementById('id_canton_' + name);
	text +=  ", "+sel.options[sel.selectedIndex].text;
	var sel = this.children.id_location;
	text +=  ", "+sel.options[sel.selectedIndex].text;		
	var obj = document.getElementById('id_' + name +"_text");
	if (obj != undefined ){
		obj.value = text;
		KeySimulation('id_' + name +"_text");
	}
	
}

function load_district(obj_sel, initial){
	name=obj_sel.name.replace("canton_", '');
	url = document.getElementById('div_district_' + name).getAttribute("href");
	url = url + '&canton='+obj_sel.value;
	if (initial != undefined){
		url = url + "&initial=" + initial;
	}
	loadDoc(url);	

	var object = document.getElementById('div_district_' + name);
	object.addEventListener("change", district_change);
	
	document.district_crdist = { "dist": 'div_district_' + name };
	document.dispatchEvent(document.crdist.dist_event);
}

window.addEventListener('load',  function() {
	var elems = document.getElementsByClassName("crdist_onerror");
	var name=undefined;
	for (var x=0; x<elems.length; x++){
	  name = elems[x].name.replace("err_", "div_");
	  var val = name.indexOf("div_canton_");
	  if (val>=0){
	    load_canton({'name': name.replace("div_canton_", "province_"),
	      			'value': elems[x].value }, elems[x].getAttribute("initial"));
	  }else{
	  	val = name.indexOf("div_district_");
	  	if (val>=0){
	      load_district({'name': name.replace("div_district_", "canton_"),
	      			'value': elems[x].value }, elems[x].getAttribute("initial"));
	   }
	  }
	}
},  false );
