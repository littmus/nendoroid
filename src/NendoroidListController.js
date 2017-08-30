///<reference path="DataUtil.js"/>
var NendoroidListController = (function () {
    function NendoroidListController($scope) {
        this.$scope = $scope;
        $scope.fullNendoroidList = fullNendoroidList;
        // set the default sort param
        $scope.sortBy = 'num';
        $scope.sortReverse = false;
        $scope.sortFunc = this.getSortValue.bind(this);
    }
    NendoroidListController.prototype.getSortValue = function (item) {
        var sortBy = this.$scope.sortBy;
        return item[sortBy];
        /*
        if (sortBy === "arcana") {
            return item.arcana + (item.level >= 10 ? item.level : ("0" + item.level));
        }
        else {
            return item[sortBy];
        }
        */
    };
    return NendoroidListController;
}());
