var groupSocket = io.connect('//' + document.domain + ':' + location.port + '/group');
var nodeSocket = io.connect('//' + document.domain + ':' + location.port + '/node');
var userSocket = io.connect('//' + document.domain + ':' + location.port + '/user');
var iCPESocket = io.connect('//' + document.domain + ':' + location.port + '/icpe');
var generalSocket = io.connect('//' + document.domain + ':' + location.port + '/general');
var adminSocket = io.connect('//' + document.domain + ':' + location.port + '/admin');
var dataSocket = io.connect('//' + document.domain + ':' + location.port + '/data');
var plotlySocket = io.connect('//' + document.domain + ':' + location.port + '/plotly');
var sensorSocket = io.connect('//' + document.domain + ':' + location.port + '/sensor');

generalSocket.on('reload', function() {
	console.log('Reloading..');
	location.reload();
})

generalSocket.on('redirect', function(url) {
	console.log("Forwarding to: ", url);
	window.location.replace(url);
});

generalSocket.on('error', function(msg) {
	toastr.error(msg);
});

generalSocket.on('warning', function(msg) {
	toastr.warning(msg);
});

generalSocket.on('info', function(msg) {
	toastr.success(msg);
});
