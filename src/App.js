///<reference path="NendoroidListController.js"/>
var StickyTableDirective = function () { return ({
    restrict: 'A',
    link: function ($scope, $element) {
        $element.stickyTableHeaders();
        $scope.$on('$destroy', function () {
            $element.stickyTableHeaders('destroy');
        });
    }
}); };
var myModule = angular.module('myModule', ['ngRoute']);
myModule.directive('stickyTable', StickyTableDirective);
myModule.controller('NendoroidListController', ['$scope', NendoroidListController]);

myModule.config(function ($routeProvider) {
    $routeProvider.when('/list', { templateUrl: 'view/list.html', controller: NendoroidListController });
    //$routeProvider.when('/skill', { templateUrl: 'view/skill.html', controller: SkillListController });
    //$routeProvider.when('/persona/:persona_name', { templateUrl: 'view/persona.html', controller: PersonaController });
    //$routeProvider.when('/setting', { templateUrl: 'view/setting.html', controller: SettingController });
});

myModule.run(function ($rootScope, $location, $route, $window) {
    $rootScope.$on('$locationChangeStart', function (event) {
        if (!$location.path()) {
            $location.path('/list');
            $route.reload();
        }
        else {
            $window.scrollTo(0, 0);
        }
    });
});
