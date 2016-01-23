var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

var context ;
var canvasWidth	 = 490;
var canvasHeight = 220;
var canvas;
var canvasDiv;

//Colors
var colorPurple = "#cb3594";
var colorGreen	= "#659b41";
var colorYellow = "#ffcf33";
var colorBrown	= "#986928";
var curColor	= colorPurple;
var clickColor	= new Array();

//Size
var clickSize = new Array();
var curSize = "normal";

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
  	/*context.strokeStyle = "#df4b26";*/
  	context.lineJoin = "round";
  	/*context.lineWidth = 5;*/
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
	    //context.lineWidth = radius;
	    context.stroke();
	}
}