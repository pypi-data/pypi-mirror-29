(function() {
  angular.module('cradminLegacy.directives', []).directive('cradminLegacyBack', function() {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        element.on('click', function() {
          history.back();
          return scope.$apply();
        });
      }
    };
  }).directive('cradminLegacyFormAction', function() {
    return {
      restrict: 'A',
      scope: {
        'value': '=cradminLegacyFormAction'
      },
      controller: function($scope) {
        $scope.$watch('value', function(newValue) {
          return $scope.element.attr('action', newValue);
        });
      },
      link: function(scope, element, attrs) {
        scope.element = element;
      }
    };
  }).directive('cradminLegacySelectTextForCopyOnFocus', function() {
    /*
    Select text of an input field or textarea when the field
    receives focus.
    
    Example:
    ```
    <p>Copy the url below and share it on social media!</p>
    <input type="text" value="example.com" cradmin-legacy-select-text-for-copy-on-focus="http://example.com">
    ```
    */

    return {
      restrict: 'A',
      scope: {
        valueToCopy: '@cradminLegacySelectTextForCopyOnFocus'
      },
      link: function(scope, element, attrs) {
        scope.value = attrs['value'];
        element.on('click', function() {
          element.val(scope.valueToCopy);
          return this.select();
        });
        scope.resetValue = function() {
          return element.val(scope.value);
        };
        element.on('change', function() {
          return scope.resetValue();
        });
        element.on('blur', function() {
          return scope.resetValue();
        });
      }
    };
  }).directive('focusonme', [
    '$timeout', function($timeout) {
      return {
        restrict: 'A',
        link: function($scope, $element) {
          $timeout(function() {
            $element[0].focus();
          });
        }
      };
    }
  ]);

}).call(this);
