var page = require('webpage').create();
var system = require('system');

var file = system.args[1];
var file_type = system.args[2];
var delay = system.args[3];

var snapshot = "" + 
"    function(){"+
"        var ele = document.querySelector('div[_echarts_instance_]');"+
"        return ele.length;"+
"    }";

page.open(file, function(){
	window.setTimeout(function () {
		var content = page.evaluateJavaScript(snapshot);
		console.log(content);
        phantom.exit();
    }, delay);
});
