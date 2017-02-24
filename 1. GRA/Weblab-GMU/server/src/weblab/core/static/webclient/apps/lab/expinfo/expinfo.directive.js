angular
    .module("lab")
    .directive("wlExpInfo", wlExpInfo);

function wlExpInfo() {
    return {
        restrict: "E",
        scope: {
            experiment: "=",
            latestuses: "=",
            stats: "=",
            reserve: "&",
            reserveMessage: "="
        },
        templateUrl: EXPINFO_TEMPLATE_URL,
        link: wlExpInfoLink
    };

    function wlExpInfoLink(scope, elem, attrs) {
        scope.Math = Math;
    }
}
