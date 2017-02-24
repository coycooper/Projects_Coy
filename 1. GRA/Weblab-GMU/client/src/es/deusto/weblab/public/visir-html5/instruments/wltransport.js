"use strict";

var visir = visir || {};

visir.WLTransport = function(workingCallback)
{
	this._isWorking = false;
	this._workCall = workingCallback;
	this._error = null;
	this.onerror = function(err){};
	this._session = null;
}

visir.WLTransport.prototype.Connect = function()
{
	trace("Login");

	Weblab.sendCommand("login",
		function(response){this._session = $.parseJSON(response).sessionkey;}.bind(this),
		this.Error.bind(this));
}

visir.WLTransport.prototype.Request = function(request, callback)
{
	trace("Send request");

	this._error = null;
	if (this._isWorking) return;
	this.SetWorking(true);

	request = '<protocol version="1.3"><request sessionkey="'+this._session+'">'+request+'</request></protocol>';

	Weblab.sendCommand(request, function(response) {
			this.SetWorking(false);
			if (typeof callback == "function")
			{
				// this will check for errors in the request
				var ret = this._ReadResponseProtocolHeader(response);
				// and we only want to do the callback if there is no errors
				if ( ! this._error)
				{
					callback(ret);
				}
			}
		}.bind(this), this.Error.bind(this));
}

visir.WLTransport.prototype._ReadResponseProtocolHeader = function(response)
{
	var $xml = $(response);
	if ($xml.find("response").length > 0) {
		return $xml.html(); // this will strip of the outer protocol tags
	}
	var $error = $xml.find("error");
	if ($error.length > 0)
	{
		this.Error($error.text());
		return;
	}
	this.Error("Unable to parse response");
}

/*
	func is a callback function that the transport system can call to make a new request
*/
visir.WLTransport.prototype.SetMeasureFunc = function(func)
{
	trace("SetMeasureFunc");
}

visir.WLTransport.prototype.SetWorking = function(isWorking, shouldContinue)
{
	shouldContinue = (shouldContinue == undefined) ? true : shouldContinue;
	this._isWorking = isWorking;
	if (typeof this._workCall == "function") this._workCall(isWorking, shouldContinue);
	$("body").trigger({ type:"working", isWorking: isWorking, shouldContinue: shouldContinue });
}

visir.WLTransport.prototype.Error = function(errormsg) {
	this.SetWorking(false, false);
	trace(errormsg);
	this.onerror(errormsg);
	this._error = errormsg;
}

visir.WLTransport.prototype.LoadCircuit = function(file, callback) {

	var reader = new FileReader();

	reader.onload = (function(cirFile) {
		return function(circuit) {
			trace("Loaded: " + circuit.target.result);
			Weblab.sendCommand("load " + circuit.target.result, null, this.Error.bind(this));

			callback(circuit.target.result);
		}.bind(this);
	}.bind(this))(file);

	reader.readAsText(file);
}

visir.WLTransport.prototype.SaveCircuit = function(circuit) {

	trace("Saved: " + circuit);
	Weblab.sendCommand("save " + circuit, null, this.Error.bind(this));

	var blob = new Blob([circuit], {type: "application/xml;charset=UTF-8"});
	saveAs(blob, "experiment.cir");
}