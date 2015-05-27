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

  function inflection ($filter) {
    return function(value) {
      if (!value) {
        return;
      }
      return value.replace(/\b[a-z](?!\s)/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }
  }

  angular
    .module('lodjersFilters', [])
    .filter('gradYear', gradYear)
    .filter('inflection', inflection)

  angular.module('lodjersApp', ['lodjersFilters', 'ngMaterial', 'ngCookies', 'ngMdIcons', 'ngMessages']);

  function config ($interpolateProvider, $mdThemingProvider) {
    $interpolateProvider
      .startSymbol('{[')
      .endSymbol(']}');

    $mdThemingProvider.theme('default')
      .primaryPalette('green')
      .accentPalette('orange');
  }

  angular
    .module('lodjersApp')
    .config(config);

  function UserService ($http, $rootScope, $filter) {
    var transformDate = function(data) {
      data=angular.fromJson(data);
      if (data.user.start_date) {
        data.user.start_date = new Date(data.user.start_date);
      }

      if (data.user.city) {
        data.user.city = $filter('inflection')(data.user.city);
      }

      if (data.user.joined_at) {
        data.user.joined_at = new Date(data.user.joined_at);
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
    .module('lodjersApp')
    .factory('UserService', UserService);

  function MatchesService ($http, $filter) {
    var transformDates = function(data) {
      data=angular.fromJson(data);
      angular.forEach(data.users, function(user) {
        user.joined_at = new Date(user.joined_at);
        user.start_date = new Date(user.start_date);
        user.city = $filter('inflection')(user.city);
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
    .module('lodjersApp')
    .factory('MatchesService', MatchesService);

  function MatchesController ($scope, $cookies, $timeout, MatchesService) {
    $cookies.emailedUsers = $cookies.emailedUsers || "";
    $scope.emailedUsers = $cookies.emailedUsers;
    $scope.searchersOnly = false;

    $scope.$on("profileUpdated", function() {
      $scope.isLoading = true;
      MatchesService.get().then(function(data) {
        $timeout(function() {
            $scope.isLoading = false;
            $scope.matches = data.users;
        }, 500);
      });
    });
  }

  function UserListItemController ($scope, $cookies) {
    $scope.visited = $scope.emailedUsers.indexOf($scope.user.netid) > -1;

    $scope.emailLink = function() {
      var subject;
      if ($scope.searchersOnly) {
        subject = "Still looking for another roommate?";
      } else {
        subject = "Moving to " + $scope.user.city;
      }

      return "mailto:" + $scope.user.email + "?subject=" + subject + "&body=I saw on lodjers.com that you're also going to " + $scope.user.city + ".";
    }

    $scope.emailed = function() {
      if (!$scope.visited) {
        $cookies.emailedUsers = $cookies.emailedUsers + ", " + $scope.user.netid;
        $scope.visited = true;
      }
      mixpanel.track("Blitzed User");
    }
  }

  angular
    .module('lodjersApp')
    .controller('MatchesController', MatchesController)
    .controller('UserListItemController', UserListItemController);

  function ProfileController ($scope, $mdToast, UserService) {
    var self = this;
    self.cities        = loadAll();
    self.selectedItem  = null;

    $scope.querySearch = function(query) {
      var results = query ? self.cities.filter( createFilterFor(query) ) : [];
      return results;
    };

    UserService.get().then(function(data) {
      $scope.user = data.user;
      _identifyUser(data.user);
    });

    $scope.submit = function() {
      UserService.put($scope.user).then(function(data) {
        $scope.user = data.user;
        $mdToast.show(
          $mdToast.simple()
          .content('Saved!')
          .position("top right")
          .hideDelay(3000)
        );
        _identifyUser(data.user);
      });
    };

    function _identifyUser(user) {
      // Identify User on Mixpanel
      mixpanel.identify(user.netid);
      mixpanel.people.set_once('$created', user.joined_at);
      mixpanel.people.set({
          "$name": user.nickname,
          "$email": user.email,
          "city": user.city,
          "grad_year": user.grad_year,
          "searching": user.searching,
      });
    }

    function loadAll() {
      var allCities = 'Atlanta, Austin, Boston, Chicago, Dallas, Dayton, Hanover, Houston, Los Angeles, Madison, New York City, Philadelphia, San Francisco, Washington D.C., ';
      return allCities.split(/, +/g).map( function (city) {
        return {
          value: city.toLowerCase(),
          display: city
        };
      });
    }
    /**
     * Create filter function for a query string
     */
    function createFilterFor(query) {
      var lowercaseQuery = angular.lowercase(query);
      return function filterFn(city) {
        return (city.value.indexOf(lowercaseQuery) !== -1);
      };
    }
  }

  angular
    .module('lodjersApp')
    .controller('ProfileController', ProfileController);

  function userListItem () {
    return {
      restrict: 'AE',
      scope: true,
      replace: true,
      templateUrl: 'static/partials/user-list-item.html'
    };
  }

  angular
    .module('lodjersApp')
    .directive('userListItem', userListItem);

  function profileForm () {
    return {
      replace: true,
      templateUrl: 'static/partials/profile-form.html'
    };
  }

  angular
    .module('lodjersApp')
    .directive('profileForm', profileForm);
})();
