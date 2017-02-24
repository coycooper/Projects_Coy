function wlSourceEditorDirective(){function a(a,b,c){}return{restrict:"E",templateUrl:"views/wlsourceeditor.directive.html",controller:"SourceEditorController",controllerAs:"sourceEditorController",link:a,scope:{}}}function SourceEditorController(a){function b(b){a._editor=b,b.setOptions({fontSize:"12pt"})}function c(a){}function d(a){alert(a)}a.aceOptions={useWrapMode:!0,showGutter:!0,showPrintMargin:!0,highlightActiveLine:!0,theme:"chrome",mode:"vhdl",firstLineNumber:1,onLoad:b,onChange:c},a.msg=d}(function(){"use strict";angular.module("elevatorApp",["ngResource","ngCookies","ngRoute","ngSanitize","ngTouch","angularFileUpload","ui.bootstrap","ui.ace"]).config(["$routeProvider",function(a){return a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl"}).when("/about",{templateUrl:"views/about.html",controller:"AboutCtrl"}).otherwise({redirectTo:"/"})}])}).call(this),function(){"use strict";angular.module("elevatorApp").controller("MainCtrl",["$scope","RefreshState",function(a,b){return a.experiment={},a.experiment.status="not_ready",a.aceEditor={},a.aceEditor.text="",b.start(function(b){return a.experiment.status=b}),a.experiment.getStatusDescription=function(){return"not_ready"===a.experiment.status?"The experiment is not ready to be used. Please, send a program.":"synthesizing"===a.experiment.status?"Now synthesizing the program you provided. Please, wait.":"programming"===a.experiment.status?"Now programming with the logic you provided. Please, wait.":"synthesizing_error"===a.experiment.status?"There was a problem while trying to synthesize your program. You might try with another.":"not_allowed"===a.experiment.status?"The type of program you provided is not allowed.":"awaiting_code"===a.experiment.status?"Waiting for a logic file to program into the board":"failed"===a.experiment.status?"An error occurred. Maybe the logic you provided is not valid. Please, try something else or contact the administrators.":"user_time_exceeded"===a.experiment.status?"Sorry, you exceeded the allocated time.":"ready"===a.experiment.status?"The system is ready. Your logic is running on the equipment.":"The experiment is in an unknown state. It may not work as expected."},a.experiment.getStatusClass=function(){return"not_ready"===a.experiment.status?"alert-info":"synthesizing"===a.experiment.status?"alert-info":"programming"===a.experiment.status?"alert-info":"synthesizing_error"===a.experiment.status?"alert-danger":"not_allowed"===a.experiment.status?"alert-danger":"awaiting_code"===a.experiment.status?"alert-info":"failed"===a.experiment.status?"alert-danger":"user_time_exceeded"===a.experiment.status?"alert-warning":"ready"===a.experiment.status?"alert-success":"alert-danger"},a.shouldShowStatus=function(){return"programming"===a.experiment.status},a.doTest=function(){return 2*Math.random()<1}}])}.call(this),function(){"use strict";angular.module("elevatorApp").controller("AboutCtrl",["$scope",function(a){return a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"]}])}.call(this),function(){"use strict";angular.module("elevatorApp").directive("wlWebcam",["$timeout",function(a){return{templateUrl:"views/wlwebcam.html",restrict:"E",scope:{src:"@src"},link:function(b,c,d){return c.find("img").bind("load error",function(){return b.refreshSoon()}),b.refreshSoon=function(){return a(function(){b.doRefresh()},1e3)},b.doRefresh=function(){var a;return a=URI(b.src),a.query({rnd:1e5*Math.random()}),b.src=a.toString()}}}}])}.call(this),function(){"use strict";angular.module("elevatorApp").directive("wlButton",["$timeout",function(a){return{templateUrl:"views/wlbutton.html",scope:{ident:"@ident",caption:"@caption",overlay:"@overlay"},restrict:"E",link:function(b,c,d){return b.button={},b.isOn=!1,b.isPressed=!1,b.press=function(){return console.debug("Button "+b.ident+" pressed."),b.isPressed=!0,Weblab.dbgSetOfflineSendCommandResponse("ok"),Weblab.sendCommand("SetPulse=off "+b.ident,function(c){return function(){return console.debug("SetPulse off succeeded"),b.isOn=!0,b.isPressed=!1,a(function(){return Weblab.dbgSetOfflineSendCommandResponse("ok"),console.debug("Timeout Triggered"),Weblab.sendCommand("SetPulse=on "+b.ident,function(a){return function(){return console.debug("SetPulse on succeded"),b.isOn=!1,b.isPressed=!1}}(this),function(a){return function(){return console.debug("SetPulse on failed"),b.button.isOn=!1,b.isPressed=!1}}(this))},500)}}(this),function(a){return function(){return console.debug("SetPulse failed")}}(this))}}}}])}.call(this),function(){"use strict";angular.module("elevatorApp").directive("wlUpload",["$upload","$cookies",function(a,b){return{templateUrl:"views/wlupload.html",restrict:"E",link:function(c,d,e){return c.$watch("files",function(){var d,e,f;if(void 0!==c.files){console.log("THE WATCH HAS: "),console.log(c.files),console.log("Cookies service: "),console.log(b),f="",e="";try{f=c.files[0].name.split(".").pop(),e=""}catch(g){d=g,console.log("Could not extract file_info from name")}return c.upload=a.upload({url:"../../../../../web/upload/",data:{file_info:f,session_id:e,is_async:"false"},file:c.files[0],fileFormDataName:"file_sent"}).progress(function(a){return console.log("Progress: "+parseInt(100*a.loaded/a.total)+"% file : "+a.config.file.name)}).success(function(a,b,c,d){return console.log("file "+d.file.name+"is uploaded successfully. Response: "+a)}).error(function(){return console.error("Could not upload the file")})}})}}}])}.call(this),function(){"use strict";angular.module("elevatorApp").directive("wlElevatorControls",function(){return{templateUrl:"views/wlelevatorcontrols.html",restrict:"E",link:function(a,b,c){}}})}.call(this),function(){"use strict";angular.module("elevatorApp").directive("wlCallingControls",function(){return{templateUrl:"views/wlcallingcontrols.html",restrict:"E",link:function(a,b,c){}}})}.call(this),function(){"use strict";var a,b=function(a,b){return function(){return a.apply(b,arguments)}};angular.module("elevatorApp").service("RefreshState",["$timeout","$rootScope",a=function(){function a(a,c){this.$timeout=a,this.$rootScope=c,this._check=b(this._check,this),this.start=b(this.start,this),console.log("ctor"),this.shouldStop=!1,this._timeout=void 0}return a.prototype.start=function(a){return this.shouldStop=!1,this.update=a,console.log("[STARTING REFRESHSTATE]"),console.log(Weblab),this._check()},a.prototype._check=function(){return this.$timeout(function(a){return function(){var b,c;return c=["ready","programming","fail"],b=c[Math.floor(Math.random()*c.length)],Weblab.dbgSetOfflineSendCommandResponse("STATE="+b),Weblab.sendCommand("STATE",function(b){var c;return c=b.substr(6),a.update&&a.$rootScope.$apply(function(){return a.update(c)}),a.shouldStop?void 0:a._timeout=a.$timeout(a._check,2e3)},function(b){return console.error("Error on STATE:"),console.error(b),a.shouldStop?void 0:a._timeout=a.$timeout(a._check,6e3)},2e3)}}(this))},a.prototype.stop=function(){return console.log("Stopping RefreshState"),this.shouldStop=!0,this.$timeout.cancel(this._timeout)},a.prototype.running=function(){return!this.shouldStop},a}()])}.call(this),angular.module("elevatorApp").directive("wlSourceEditor",wlSourceEditorDirective),angular.module("elevatorApp").controller("SourceEditorController",SourceEditorController),SourceEditorController.$inject=["$scope"];