(function() {
  angular.module('cradminLegacy.modal', []).directive('cradminLegacyModalWrapper', [
    function() {
      /** Shows a modal window on click.
      
      Example
      =======
      
      ```html
      <div cradmin-legacy-modal-wrapper>
        <button ng-click="showModal($event)" type="button">
          Show modal window
        </button>
        <div cradmin-legacy-modal class="cradmin-legacy-modal"
                ng-class="{'cradmin-legacy-modal-visible': modalVisible}">
            <div class="cradmin-legacy-modal-backdrop" ng-click="hideModal()"></div>
            <div class="cradmin-legacy-modal-content">
                <p>Something here</p>
                <button ng-click="hideModal()" type="button">
                  Hide modal window
                </button>
            </div>
        </div>
      </div>
      ```
      */

      return {
        scope: true,
        controller: function($scope) {
          var bodyElement;
          $scope.modalVisible = false;
          bodyElement = angular.element('body');
          $scope.showModal = function(e) {
            if (e != null) {
              e.preventDefault();
            }
            $scope.modalVisible = true;
            bodyElement.addClass('cradmin-legacy-noscroll');
          };
          $scope.hideModal = function() {
            $scope.modalVisible = false;
            bodyElement.removeClass('cradmin-legacy-noscroll');
          };
        }
      };
    }
  ]).directive('cradminLegacyModal', [
    function() {
      return {
        require: '^^cradminLegacyModalWrapper',
        link: function($scope, element) {
          var body;
          body = angular.element('body');
          return element.appendTo(body);
        }
      };
    }
  ]);

}).call(this);
