$(document).ready(function(){
  // $('.profile-panel').pushpin({ top: $('.profile-panel').offset().top });

  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 2 // Creates a dropdown of 15 years to control year
  });

  $(".button-collapse").sideNav();
});


var dartmates = angular.module('dartmatesApp', []);

dartmates.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

dartmates.controller("MatchesController", function($scope, $http) {
  $http.get('/api/users/matches').
    success(function(data, status, headers, config) {
      $scope.matches = data.users;
    }).
    error(function(data, status, headers, config) {
      // Log Error
    });

});

dartmates.controller("ProfileController", function($scope, $http) {
  transformDate = function(data) {
    data=angular.fromJson(data);
    if (data.user.start_date) {
      data.user.start_date = new Date(data.user.start_date);
    }
    return data;
  };

  $http.get('/api/user', {transformResponse: transformDate}).
  success(function(data, status, headers, config) {
    $scope.user = data.user;
  }).
  error(function(data, status, headers, config) {
    // Log Error
  });

  $scope.submit = function() {
    $http.put('/api/user', $scope.user, {transformResponse: transformDate}).
    success(function(data, status, headers, config) {
      $scope.user = data.user;
      Materialize.toast("Saved changes!", 2000)
    }).
    error(function(data, status, headers, config) {
      // Log Error
    });
  };


});

dartmates.filter('range', function() {
  return function(input, min, max) {
    min = parseInt(min); //Make string input int
    max = parseInt(max);
    for (var i=min; i<max; i++)
      input.push(i);
    return input;
  };
});
