
angular
    .module("lab")
    .directive("wlExperimentIframe", wlExperimentIframe);


function wlExperimentIframe($injector) {
    return {
        restrict: "E",
        scope: {
            experiment: "=",
            iframeurl: "=",
            language: "="
        },
        templateUrl: EXPERIMENT_IFRAME_TEMPLATE_URL,
        controller: "ExperimentIframeController",
        controllerAs: "experimentIframeController",
        link: wlExperimentIframeLink
    };



    function wlExperimentIframeLink(scope, elem, attrs, ctrl) {
        // -------------
        // Dependencies
        // -------------
        var $log = $injector.get('$log');
        var resizer = $injector.get('Resizer');

        var iframe = elem.find("iframe");

        var loadingTimeout;
        var loadedCalled = false;

        // -------------
        // DOM bindings & initialization.
        // -------------
        iframe.load(handleLoadEvent);
        resizer.loadFrameResizer(iframe);
        window.addEventListener('message', _processMessages, false);

        // -------------
        // Scope bindings & data
        // -------------
        scope.$on("experimentFinished", onExperimentFinished);
        scope.$on("experimentLoadedAndDisplayed", onExperimentLoadedAndDisplayed);


        // -------------
        // Implementations
        // -------------

        /**
         * Reloads the iframe when the experimentFinished event is caught.
         */
        function onExperimentFinished() {
            // Reload the frame.
            // This is particularly important at the moment because the WeblabExp compatibility library
            // does not support any kind of reset besides re-instancing. (and it probably shouldn't support it either).
            iframe.attr('src', function (i, val) {
                return val;
            });
        } // !onExperimentFinished

        function onExperimentLoadedAndDisplayed() {
            resizer.resize(iframe);
        }

        function _timeoutFunction() {
            console.log("Timeout happened");
            if (!loadedCalled) {
                scope.$emit("experimentLoadingFailed");
            }
        }

        /**
         * Inject the new experiment library and the compatibility layer which automagically is supposed to replace the old one.
         */
        function handleLoadEvent() {
            $log.debug("Injecting scripts");

            loadingTimeout = setTimeout(_timeoutFunction, 40 * 1000); // 40 seconds

            // TODO: We should maybe consider removing this and just forcing experiment developers to include the library if they want to support proper resizing.
            resizer.injectScriptIntoFrame(iframe, IFRAME_RESIZER_URL); // Automatic iframe resizing.
        }

        function _processMessages(e) {
            if (new String(e.data).indexOf("weblabdeusto::") == 0) {
                if (new String(e.data) == "weblabdeusto::experimentLoaded") {
                    clearTimeout(loadingTimeout);
                    loadedCalled = true;
                    resizer.forceFrameResizer(iframe);
                    setTimeout( function() {
                        scope.$emit("experimentLoaded");
                    }, 2000);
                } else if (new String(e.data).indexOf("weblabdeusto::experimentLoading::") == 0) {
                    var message = new String(e.data);
                    var time = message.substring("weblabdeusto::experimentLoading::".length, message.length);
                    var seconds = parseInt(time);
                    clearTimeout(loadingTimeout);
                    loadingTimeout = setTimeout(_timeoutFunction, seconds * 1000);
                } else if(new String(e.data).indexOf("weblabdeusto::reserve") == 0) {
                    scope.experiment.reserve('frame');
                }
            }
        }

    } // !wlExperimentIframeLink



} //! wlExperimentIframe

