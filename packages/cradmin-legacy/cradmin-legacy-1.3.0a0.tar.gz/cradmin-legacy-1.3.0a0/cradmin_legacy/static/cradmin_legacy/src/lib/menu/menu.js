(function() {
  angular.module('cradminLegacy.menu', []).directive('cradminLegacyMenu', [
    function() {
      /** Menu that collapses automatically on small displays.
      
      Example
      =======
      
      ```html
      <nav cradmin-legacy-menu class="cradmin-legacy-menu">
        <div class="cradmin-legacy-menu-mobileheader">
          <a href="#" role="button"
              class="cradmin-legacy-menu-mobiletoggle"
              ng-click="cradminMenuTogglePressed()"
              ng-class="{'cradmin-legacy-menu-mobile-toggle-button-expanded': cradminMenuDisplay}"
              aria-pressed="{{ getAriaPressed() }}">
            Menu
          </a>
        </div>
        <div class="cradmin-legacy-menu-content"
            ng-class="{'cradmin-legacy-menu-content-display': cradminMenuDisplay}">
          <ul>
            <li><a href="#">Menu item 1</a></li>
            <li><a href="#">Menu item 2</a></li>
          </ul>
        </div>
      </nav>
      ```
      
      Design notes
      ============
      
      The example uses css classes provided by the default cradmin CSS, but
      you specify all classes yourself, so you can easily provide your own
      css classes and still use the directive.
      */

      return {
        scope: true,
        controller: function($scope, cradminLegacyPagePreview) {
          $scope.cradminMenuDisplay = false;
          $scope.cradminMenuTogglePressed = function() {
            return $scope.cradminMenuDisplay = !$scope.cradminMenuDisplay;
          };
          $scope.getAriaPressed = function() {
            if ($scope.cradminMenuDisplay) {
              return 'pressed';
            } else {
              return '';
            }
          };
          this.close = function() {
            $scope.cradminMenuDisplay = false;
            return $scope.$apply();
          };
        }
      };
    }
  ]).directive('cradminLegacyMenuAutodetectOverflowY', [
    'cradminLegacyWindowDimensions', function(cradminLegacyWindowDimensions) {
      /**
      */

      return {
        require: '?cradminLegacyMenu',
        controller: function($scope) {
          var disableInitialWatcher;
          $scope.onWindowResize = function(newWindowDimensions) {
            return $scope.setOrUnsetOverflowYClass();
          };
          $scope.setOrUnsetOverflowYClass = function() {
            var menuDomElement, _ref;
            menuDomElement = (_ref = $scope.menuElement) != null ? _ref[0] : void 0;
            if (menuDomElement != null) {
              if (menuDomElement.clientHeight < menuDomElement.scrollHeight) {
                return $scope.menuElement.addClass($scope.overflowYClass);
              } else {
                return $scope.menuElement.removeClass($scope.overflowYClass);
              }
            }
          };
          disableInitialWatcher = $scope.$watch(function() {
            var _ref;
            if (((_ref = $scope.menuElement) != null ? _ref[0] : void 0) != null) {
              return true;
            } else {
              return false;
            }
          }, function(newValue) {
            if (newValue) {
              $scope.setOrUnsetOverflowYClass();
              return disableInitialWatcher();
            }
          });
        },
        link: function($scope, element, attrs) {
          $scope.overflowYClass = attrs.cradminLegacyMenuAutodetectOverflowY;
          $scope.menuElement = element;
          cradminLegacyWindowDimensions.register($scope);
          $scope.$on('$destroy', function() {
            return cradminLegacyWindowDimensions.unregister($scope);
          });
        }
      };
    }
  ]).directive('cradminLegacyMenuCloseOnClick', [
    function() {
      /** Directive that you can put on menu links to automatically close the
      menu on click.
      */

      return {
        require: '^^cradminLegacyMenu',
        link: function(scope, element, attrs, cradminLegacyMenuCtrl) {
          element.on('click', function() {
            cradminLegacyMenuCtrl.close();
          });
        }
      };
    }
  ]);

}).call(this);
