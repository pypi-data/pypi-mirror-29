var app = angular.module('SquadSubscriptions', [], function(
    $locationProvider,
    $routeProvider,
    $resourceProvider,
    $httpProvider,
    $interpolateProvider){
    //$interpolateProvider.startSymbol('//');
    //$interpolateProvider.endSymbol('//');
});

function SubscriptionController($scope, $http, $location, $timeout) {
    $scope.projects = [];
    $scope.selection = [];

    $http.get("/_/profiledetails/").then(
        function(data) {
            $scope.projects = data
        }
    )
    // Helper method to get selected subscriptions
    //$scope.selectedSubscriptions = function selectedSubscriptions() {
    //    return filterFilter($scope.project, { selected: true });
    //};

    // Watch subscriptions for changes
    //$scope.$watch('projects|filter:{selected:true}', function (nv) {
    //    $scope.selection = nv.map(function (subscription) {
    //        return subscription.id;
    //    });
    //}, true);
}

app.controller(
    'SubscriptionController',
    [
        '$scope',
        '$http',
        '$location',
        '$timeout',
        SubscriptionController
    ]
);

