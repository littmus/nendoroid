///<reference path="../data/NendoroidData.js"/>

var fullNendoroidList = (function () {
    var arr = [];
    for (var key in nendoroidMap) {
        if (nendoroidMap.hasOwnProperty(key)) {
            var nendo = nendoroidMap[key];
            arr.push(nendo);
        }
    }
    return arr;
})();