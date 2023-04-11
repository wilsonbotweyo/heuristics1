angular.module('guitarShopApp', [])
  .controller('GuitarShopController', ['$scope', '$http', function($scope, $http) {
    // Initialize properties
    $scope.inventory = [];
    $scope.formItem = {};
    $scope.hideInsert = true;

    // Load inventory function
    $scope.loadInventory = function() {
      $http.get('/api/guitars').then(function(response) {
        $scope.inventory = response.data;
      }, function(error) {
        console.error('Error loading inventory:', error.status);
      });
    };

    // New button click event handler
    $scope.new = function() {
      $scope.formItem = {};
      $scope.hideInsert = false;
    };

    // Insert button click event handler
    $scope.insert = function() {
      $http.post('/api/guitars', $scope.formItem).then(function(response) {
        $scope.formItem.id = parseInt(response.headers('Location').split('/').pop());
        $scope.loadInventory();
        $scope.hideInsert = true;
      }, function(error) {
        console.error('Error inserting item:', error.status);
      });
    };

    // Edit button click event handler
    $scope.edit = function(id) {
      $http.get('/api.php/' + id).then(function(response) {
        $scope.formItem = response.data;
        $scope.hideInsert = true;
      }, function(error) {
        console.error('Error editing item:', error.status);
      });
    };

    // Update button click event handler
    $scope.update = function() {
      $http.put('/api.php/' + $scope.formItem.id, $scope.formItem).then(function(response) {
        $scope.loadInventory();
      }, function(error) {
        console.error('Error updating item:', error.status);
      });
    };

    // Delete button click event handler
    $scope.delete = function(id) {
      if (window.confirm('Are you sure you want to delete this item?')) {
        $http.delete('/api.php/' + id).then(function(response) {
          $scope.loadInventory();
          if ($scope.formItem.id === id) {
            $scope.new();
          }
        }, function(error) {
          console.error('Error deleting item:', error.status);
        });
      }
    };

    // Load the inventory when the page is first loaded
    $scope.loadInventory();
    $scope.new();
  }]);
