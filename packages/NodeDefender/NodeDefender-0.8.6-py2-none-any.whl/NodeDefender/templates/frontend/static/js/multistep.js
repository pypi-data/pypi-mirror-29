var cb = []
var submitcb;
var initMultistep = function() {
	for (var i = 0; i < (arguments.length - 1); i++)
		cb[i] = arguments[i];
	submitcb = arguments[arguments.length - 1];
}
$(document).ready(function() {
	var current = 1;

	multiform   = $(".multiform-step");
	btnnext     = $(".multiform-next");
	btnback     = $(".multiform-back");
	btnsubmit   = $(".multiform-submit");

	// Init buttons and UI
	multiform.not(':eq(0)').hide();
	hideButtons(current);
	setProgress(current);

	// Next button click action
	btnnext.click(function(){
		
		if (checkStep(current) == false)
			return;

		if(current < multiform.length){
                   multiform.show();
                   multiform.not(':eq('+(current++)+')').hide();
  		   setProgress(current);
	       }
        hideButtons(current);
       })
  
	// Back button click action
  btnback.click(function(){
		if(current > 1){
			current = current - 2;
			btnnext.trigger('click');
		}
		hideButtons(current);
	})
	
	btnsubmit.click(function() {
		submitcb();
	})
});
checkStep = function(current) {
	if (current > 0) {
		return cb[current - 1]();
	}
	else {
		return true;
	}
}

// Change progress bar action
setProgress = function(currstep){
	var percent = parseFloat(100 / multiform.length) * currstep;
	percent = percent.toFixed();
	$(".progress-bar")
        .css("width",percent+"%")
        .html(percent+"%");
}

// Hide buttons according to the current step
hideButtons = function(current){
	var limit = parseInt(multiform.length);

	$(".multibtn").hide();

	if(current < limit) btnnext.show(); 	
	if(current > 1) btnback.show();
	if (current == limit) { btnnext.hide(); btnsubmit.show(); }
}
