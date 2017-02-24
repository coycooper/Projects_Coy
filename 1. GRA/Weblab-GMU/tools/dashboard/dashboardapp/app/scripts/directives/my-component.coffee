'use strict'

###*
 # @ngdoc directive
 # @name dashboardappApp.directive:myComponent
 # @description
 # # myComponent
###
angular.module 'dashboardappApp'
  .directive 'myComponent', ['$rootScope', ($rootScope) ->
    restrict: 'E',
    scope:
      componentid: '=componentid'
      component: '=component'
    templateUrl: 'views/my-component.html'
    link: (scope, element, attrs) ->

      # Gets an icon class which is appropriate for the specified status.
      scope.getIconForStatus = (status) ->
        if status == 'OK'
          return "fa fa-check icon-green"
        else if status == 'WARNING'
          return "fa fa-warning icon-red"
        else if status == 'ERROR'
          return "fa fa-remove icon-red"
        else if status == 'FAIL'
          return "fa fa-remove icon-red"
        else if status == undefined
          return "fa fa-question icon-red"

      # Converts the given string to a Date object.
      scope.dateStrToDate = (date) ->
        # The date is in UTC so we indicate it so that it's parsed correctly.
        date = date + " Z";
        return new Date(date)

      # Counts the results of the checks.
      scope.countResults = ->
        console.log "Counting results"

        scope.totals = {"TOTAL": 0}

        for own elemid, element of scope.component
          console.log element
          scope.totals["TOTAL"] += 1
          if scope.totals[element.status] == undefined
            scope.totals[element.status] = 0
          scope.totals[element.status] += 1

        console.log "RESULTS: "
        console.log scope.totals

        return

      scope.countResults()
  ]
