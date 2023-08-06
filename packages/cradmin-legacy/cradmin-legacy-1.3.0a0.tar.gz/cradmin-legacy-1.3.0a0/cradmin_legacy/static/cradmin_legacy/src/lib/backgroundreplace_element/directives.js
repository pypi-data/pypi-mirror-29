(function() {
  angular.module('cradminLegacy.backgroundreplace_element.directives', []).directive('cradminLegacyBgReplaceElementOnPageLoad', [
    '$window', 'cradminLegacyBgReplaceElement', function($window, cradminLegacyBgReplaceElement) {
      /*
      This is just an example/debugging directive for cradminLegacyBgReplaceElement.
      */

      return {
        restrict: 'A',
        controller: function($scope, $element) {},
        link: function($scope, $element, attributes) {
          var remoteElementSelector, remoteUrl;
          remoteElementSelector = attributes.cradminLegacyRemoteElementSelector;
          remoteUrl = attributes.cradminLegacyRemoteUrl;
          if (remoteElementSelector == null) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.error === "function") {
                console.error("You must include the 'cradmin-legacy-remote-element-id' attribute.");
              }
            }
          }
          if (remoteUrl == null) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.error === "function") {
                console.error("You must include the 'cradmin-legacy-remote-url' attribute.");
              }
            }
          }
          angular.element(document).ready(function() {
            console.log('load', remoteUrl, remoteElementSelector);
            return cradminLegacyBgReplaceElement.load({
              parameters: {
                method: 'GET',
                url: remoteUrl
              },
              remoteElementSelector: remoteElementSelector,
              targetElement: $element,
              $scope: $scope,
              replace: true,
              onHttpError: function(response) {
                return console.log('ERROR', response);
              },
              onSuccess: function() {
                return console.log('Success!');
              },
              onFinish: function() {
                return console.log('Finish!');
              }
            });
          });
        }
      };
    }
  ]);

}).call(this);
