var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

var context ;
var canvasWidth	 = 600
var canvasHeight = 300;
var canvas;
var canvasDiv;

//Color
var curColor	= "#000000";
var clickColor	= new Array();

//Size
var clickSize = new Array();
var curSize = 10;

function initialize(){
	canvasDiv = document.getElementById('canvasDiv');
	canvas = document.createElement('canvas');
	canvas.setAttribute('width', canvasWidth);
	canvas.setAttribute('height', canvasHeight);
	canvas.setAttribute('id', 'canvas');
	canvasDiv.appendChild(canvas);


	if(typeof G_vmlCanvasManager != 'undefined') {
		canvas = G_vmlCanvasManager.initElement(canvas);
	}
	context = canvas.getContext("2d");

	$('#canvas').mousedown(function(e){
		var mouseX = e.pageX - this.offsetLeft;
		var mouseY = e.pageY - this.offsetTop;
		paint = true;
		addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
		redraw();
	});

	$('#canvas').mousemove(function(e){
	  if(paint){
	    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
	    redraw();
	  }
	});

	$('#canvas').mouseup(function(e){
	  paint = false;
	});

	$('#canvas').mouseleave(function(e){
	  paint = false;
	});

	$('#prediccion').mousedown(function(e){

		prediccion();
	});

	$('#clear').mousedown(function(e)
	{

		clearCanvas_simpleSizes();
	});
}

function clearCanvas_simpleSizes()
{

	context.clearRect(0, 0, canvasWidth, canvasHeight);

}

function addClick(x, y, dragging){
	clickX.push(x);
  	clickY.push(y);
  	clickDrag.push(dragging);
  	clickColor.push(curColor);
  	clickSize.push(curSize);
}

function redraw(){
	context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
  	context.lineJoin = "round";
	for(var i=0; i < clickX.length; i++) {		
	    context.beginPath();
	    if(clickDrag[i] && i){
	    	context.moveTo(clickX[i-1], clickY[i-1]);
	    }else{
	     	context.moveTo(clickX[i]-1, clickY[i]);
	    }
	    context.lineTo(clickX[i], clickY[i]);
	    context.closePath();
	    context.strokeStyle = clickColor[i];
	    context.lineWidth = curSize;
	    context.stroke();
	}
}

/**
* Descargamos la canvas en archivo.png
*/

//function prediccion() {
//
//    var canvasElement = document.getElementById('canvas');
//
//    var MIME_TYPE = "image/png";
//
//    var imgURL = canvasElement.toDataURL(MIME_TYPE);
//
//    var dlLink = document.createElement('a');
//    dlLink.download = 'number';
//    dlLink.href = imgURL.replace(/^data:image\/[^;]/, 'data:application/octet-stream');;
//
//    dlLink.dataset.downloadurl = [MIME_TYPE, dlLink.download, dlLink.href].join(':');
//    document.body.appendChild(dlLink);
//    dlLink.click();
//    document.body.removeChild(dlLink);
//}

function prediccion(){
    var img = document.getElementById("canvas");
    var data = img.toDataURL();
    $.ajax({
        url : "/",
        data:'{"image":"'+data+'"}',
        type:"POST",
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
            $("#digit_text").text(data.prediccion) ;
        }
    });
}

