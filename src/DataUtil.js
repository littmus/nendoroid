///<reference path="../data/NendoroidData.js"/>
///<reference path="../data/ProductData.js"/>

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

var productList = (function () {
    var arr = [];
    for (var key in productMap) {
        if (productMap.hasOwnProperty(key)) {
            var product = productMap[key];
            arr.push(product);
        }
    }
    return arr;
})();