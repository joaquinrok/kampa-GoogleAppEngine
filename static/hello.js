/*
 * http://stackoverflow.com/questions/18260815/use-gapi-client-javascript-to-execute-my-custom-google-api
 * https://developers.google.com/appengine/docs/java/endpoints/consume_js
 * https://developers.google.com/api-client-library/javascript/reference/referencedocs#gapiclientload
 *
 */

/**
 * After the client library has loaded, this init() function is called.
 * The init() function loads the helloworldendpoints API.
 */

function init() {
	
	// You need to pass the root path when you load your API
	// otherwise calls to execute the API run into a problem
	
	// rootpath will evaulate to either of these, depending on where the app is running:
	// //localhost:8080/_ah/api
	// //your-app-id/_ah/api

	var rootpath = "//" + window.location.host + "/_ah/api";
	
	// Load the helloworldendpoints API
	// If loading completes successfully, call loadCallback function
	gapi.client.load('helloworldendpoints', 'v1', loadCallback, rootpath);
}

/*
 * When helloworldendpoints API has loaded, this callback is called.
 * 
 * We need to wait until the helloworldendpoints API has loaded to
 * enable the actions for the buttons in index.html,
 * because the buttons call functions in the helloworldendpoints API
 */
function loadCallback () {	
	// Enable the button actions
	enableButtons ();
}

function enableButtons () {

	btn = document.getElementById("input_add_btn");
	btn.onclick= function(){addAmount();};

	btn = document.getElementById("input_total_btn");
	btn.onclick= function(){changeTotal();};

	btn = document.getElementById("input_obj_btn");
	btn.onclick= function(){changeObj();};

	btn = document.getElementById("generate_btn");
	btn.onclick= function(){generateImage();};

	getValues();
}

//---------------------------------//

function addAmount(){

    document.getElementById("wait").style.display = "block";

    var input_value = parseFloat(document.getElementById("input_field_add").value);
    var params = {'addValue': input_value}
    var request = gapi.client.helloworldendpoints.addAmount(params);

    request.execute(getValuesCallback);

}

function changeTotal(){

    document.getElementById("wait").style.display = "block";

    var input_value = parseFloat(document.getElementById("input_field_total").value);
    var params = {'newValue': input_value}
    var request = gapi.client.helloworldendpoints.changeTotal(params);

    request.execute(getValuesCallback);

}

function changeObj(){

    document.getElementById("wait").style.display = "block";

    var input_value = parseFloat(document.getElementById("input_field_obj").value);
    var params = {'newValue': input_value}
    var request = gapi.client.helloworldendpoints.changeObj(params);

    request.execute(getValuesCallback);

}

function getValues(){

    document.getElementById("wait").style.display = "block";

    var req = gapi.client.helloworldendpoints.getValues();
    req.execute(getValuesCallback);

}

function getValuesCallback (response) {
    document.getElementById("wait").style.display = "none";

    document.getElementById("recaudado").innerHTML = response.recaudado;
    document.getElementById("objetivo").innerHTML = response.objetivo;

    updateRestante();
	//alert(response.greeting);
}

function updateRestante(){

    var rec = parseFloat(document.getElementById("recaudado").innerHTML);
    var obj = parseFloat(document.getElementById("objetivo").innerHTML);

    document.getElementById("restante").innerHTML = obj-rec;

}

function generateImage(){

    document.getElementById("wait").style.display = "block";

    var request = gapi.client.helloworldendpoints.generateImage();

    request.execute(genImgCallback);

}

function genImgCallback(response){

    document.getElementById("wait").style.display = "none";
    document.getElementById("hazclick").style.display = "block";

    document.getElementById("imgdiv").innerHTML = response.imgHTML;

    var url = document.getElementById("theimage").src.replace(/^data:image\/[^;]/, 'data:application/octet-stream');
    document.getElementById("imgdownload").href = url;
    //window.open(document.getElementById("imgdownload").href)
}



