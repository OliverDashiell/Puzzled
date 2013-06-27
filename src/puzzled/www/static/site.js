



function Appl(data){
	this._request_id_seed_ = 0;
	this._request_callbacks_ = {};
	this._reconnect_time_default_ = 3000;
	this._reconnect_time_ = this._reconnect_time_default_;
	this._reconnect_timeout_ = null;
	this._ws_ = null;

	if(data && typeof data == "object"){
		for(var name in data){
			this[name]=data[name];
		}
	}
	for(init in this.settings.initializers){
		this.settings.initializers[init].call(this);
	}
}


Appl.prototype.settings = {
	initializers: {}
};


Appl.prototype.wrap = function(name){
	/**
	 * utility function to wrap a function of this object
	 * so that ko can bind it with a closure containing this
	 * as a that variable.
	 */
	var that = this;
	var fn_args = [].splice.call(arguments,1);
	return function(){
		var args = fn_args.concat([].splice.call(arguments,0));
		return that[name].apply(that,args);
	};
};


Appl.prototype.is_connected = function(){
	return this._ws_ !== null;
};


Appl.prototype.connect = function(){
	if(this._reconnect_timeout_ !== null){
		clearTimeout(this._reconnect_timeout_);
		this._reconnect_timeout_ = null;
	}
	var protocol = document.location.protocol == "https:"? "wss://" : "ws://";
	var ws = this._ws_ = new WebSocket(protocol + document.domain + ":" + document.location.port + '/websocket');
	ws.onopen = this.wrap("connected");
	ws.onmessage = this.wrap("handle_message");
	ws.onclose = this.wrap("disconnected");
	ws.onerror = this.wrap("error");
};


Appl.prototype.connected = function(message){
	this._reconnect_time_ = this._reconnect_time_default_;
	this.send({action:"echo", args:{message:"Hello, world!"} },function(response){
		if(response.error){
			this.error(response.error);
		} else {
			this.status(response.result);
		}
	});
};


Appl.prototype.disconnected = function(){
	this._ws_ = null;
	var that = this;
	this.status('reconnecting in ' + (this._reconnect_time_/1000) + ' secs');
	this._reconnect_timeout_ = setTimeout(function(){ 
		that._reconnect_timeout_ = null;
		that.connect();
	}, this._reconnect_time_);
	this._reconnect_time_ = this._reconnect_time_ + this._reconnect_time_;
};


Appl.prototype.handle_message = function(evt){
	var that = this;
	var response = $.parseJSON(evt.data);
	if(response.request_id === -1){
		this.update_user(response);
	} else if(response.request_id && that._request_callbacks_[response.request_id]){
		var callback = that._request_callbacks_[response.request_id]
		if(callback){
			callback.call(that,response);
		}
	} else{
		that.broadcast(response);
	}
};


Appl.prototype.next_request_id = function(callback){
	this._request_id_seed_ = this._request_id_seed_ + 1;
	var request_id = this._request_id_seed_;
	this._request_callbacks_[request_id] = callback;
	return request_id;
};


Appl.prototype.send = function(message, callback){
	this.error(null);
	message['request_id'] = this.next_request_id(callback);
	if(this.is_connected() === true){
		this._ws_.send(ko.toJSON(message));
	}
};


Appl.prototype.login = function(){
	var request = {
		action:"login",
		email: this.user.email(),
		password: this.user.password()
	};
	this.send(request, this.update_user);
};


Appl.prototype.register = function(){
	var request = {
		action:"register",
		email: this.user.email(),
		password: this.user.password()
	};
	this.send(request, this.update_user);
};


Appl.prototype.get_users = function(){
	var request = {
		action:"users",
		args: {}
	};
	this.send(request, function(response){
		if(response.error){
			this.error(response.error);
		} else{
			this.users(response.result);
		}
	});
};


Appl.prototype.update_user = function(response){
	if(response.error){
		this.error(response.error);
	} else{
		if(response.cookie){
			var expires = new Date();
			expires.setMonth( expires.getMonth( ) + 1 );
			document.cookie = response.cookie_name + '= "' + response.cookie + 
					'"; expires=' + expires.toGMTString() + 
					'; path=/';
		}
		this.user.id(response.result.id);
		this.user.email(response.result.email);
		this.user.name(response.result.name);
		this.user.password(null);
	}
};


Appl.prototype.chat = function(){
	var request = {
		action: "chat",
		args: {
			from_user: this.user.name(),
			from_user_id: "" + this.user.id(),
			message: this.chat_entry()
		}
	};
	this.send(request);
	this.chat_entry('');
	this.transcript.push(request.args);
};

$(function(){
	
	var appl = window.appl = new Appl({
		status: ko.observable('connecting...'),
		broadcast: ko.observable(),
		error: ko.observable(),
		user: {
			email: ko.observable('admin@test.com'),
			password: ko.observable('admin'),
			name: ko.observable(),
			id: ko.observable(Appl.prototype.settings.client_id)
		},
		users: ko.observableArray(),
		transcript: ko.observableArray(),
		chat_entry: ko.observable()
	});
	appl.broadcast.subscribe(function(message){
		if(message.signal==='redirect'){
			document.location=message.target;
		} else if(message.signal==='chat'){
			appl.transcript.push(message.message);
		}
	});
	ko.applyBindings(appl);
	appl.connect();
	
});