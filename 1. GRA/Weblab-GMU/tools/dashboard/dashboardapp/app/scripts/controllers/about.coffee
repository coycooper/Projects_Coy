'use strict'

###*
 # @ngdoc function
 # @name dashboardappApp.controller:AboutCtrl
 # @description
 # # AboutCtrl
 # Controller of the dashboardappApp
###
angular.module('dashboardappApp')
  .controller 'AboutCtrl', ($scope) ->
    $scope.awesomeThings = [
      'HTML5 Boilerplate'
      'AngularJS'
      'Karma'
    ]
