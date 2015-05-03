$(document).ready(function(){
  // $('.profile-panel').pushpin({ top: $('.profile-panel').offset().top });

  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 2 // Creates a dropdown of 15 years to control year
  });

  $(".button-collapse").sideNav();
});


(function() {

  function gradYear ($filter) {
    return function(value) {
      if (!value) {
        return;
      }

      if (value.length < 2) {
        return "'" + value;
      }

      return "'" + $filter('limitTo')(value, -2);
    }
  }

  angular
    .module('dartmatesFilters', [])
    .filter('gradYear', gradYear)

  angular.module('dartmatesApp', ['dartmatesFilters']);

  function config ($interpolateProvider) {
    $interpolateProvider
    .startSymbol('{[')
    .endSymbol(']}');
  }

  angular
    .module('dartmatesApp')
    .config(config);

  function UserService ($http, $rootScope) {
    var transformDate = function(data) {
      data=angular.fromJson(data);
      if (data.user.start_date) {
        data.user.start_date = new Date(data.user.start_date);
      }
      return data;
    };

    var UserService = {

      get: function() {
        var promise = $http.get('/api/user', {transformResponse: transformDate}).then(function (response) {
          $rootScope.$broadcast('profileUpdated');
          return response.data;
        });
        return promise;
      },

      put: function(user) {
        var promise = $http.put('/api/user', user, {transformResponse: transformDate}).then(function (response) {
          $rootScope.$broadcast('profileUpdated');
          return response.data;
        });
        return promise;
      }
    };

    return UserService;
  }

  angular
    .module('dartmatesApp')
    .factory('UserService', UserService);

  function MatchesService ($http) {
    var transformDates = function(data) {
      data=angular.fromJson(data);
      angular.forEach(data.users, function(user) {
        user.joined_at = new Date(user.joined_at);
        user.start_date = new Date(user.start_date);
      });

      return data;
    };

    var MatchesService = {
      get: function() {
        var promise = $http.get('/api/users/matches', {transformResponse: transformDates}).then(function (response) {
          return response.data;
        });
        return promise;
      }
    }

    return MatchesService;
  }

  angular
    .module('dartmatesApp')
    .factory('MatchesService', MatchesService);

  function MatchesController ($scope, MatchesService) {
    $scope.isLoading = true;

    $scope.$on("profileUpdated", function() {
      MatchesService.get().then(function(data) {
        $scope.isLoading = false;
        $scope.matches = data.users;
      });
    });
  }

  angular
    .module('dartmatesApp')
    .controller('MatchesController', MatchesController);

  function ProfileController ($scope, UserService) {
    UserService.get().then(function(data) {
      $scope.user = data.user;
    });

    $scope.submit = function() {
      UserService.put($scope.user).then(function(data) {
        $scope.user = data.user;
        Materialize.toast("Saved changes!", 2000);
      });
    };
  }

  angular
    .module('dartmatesApp')
    .controller('ProfileController', ProfileController);

  function userListItem () {
    return {
      replace: true,
      templateUrl: 'static/partials/user-list-item.html'
    };
  }

  angular
    .module('dartmatesApp')
    .directive('userListItem', userListItem);

  function profileForm () {
    return {
      replace: true,
      templateUrl: 'static/partials/profile-form.html'
    };
  }

  angular
    .module('dartmatesApp')
    .directive('profileForm', profileForm);
})();
