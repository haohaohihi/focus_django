$(document).ready(function(){
	var o1=$('.footer').offset().top;
	var o2=$(document).height();
	if (o2-o1>77) {
		$('.footer').css('position','absolute');
		$('.footer').css('bottom','0px');
	};
});