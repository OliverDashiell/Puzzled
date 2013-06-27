if(!Array.indexOf){
	// fix bug in ie
	Array.prototype.indexOf = function(obj){
		for(var i=0; i<this.length; i++){
			if(this[i]==obj){
				return i;
			}
		}
		return -1;
	};
}


var ENTER_KEY = 13;

// a custom binding to handle the enter key (could go in a separate library)
ko.bindingHandlers.enterKey = {
	init: function( element, valueAccessor, allBindingsAccessor, data ) {
		var wrappedHandler, newValueAccessor;

		// wrap the handler with a check for the enter key
		wrappedHandler = function( data, event ) {
			if ( event.keyCode === ENTER_KEY ) {
				var that = this;
				setTimeout(function(){
					valueAccessor().call( that, data, event );
				},100);
			}
		};

		// create a valueAccessor with the options that we would want to pass to the event binding
		newValueAccessor = function() {
			return {
				keyup: wrappedHandler
			};
		};

		// call the real event binding's init function
		ko.bindingHandlers.event.init( element, newValueAccessor, allBindingsAccessor, data );
	}
};
