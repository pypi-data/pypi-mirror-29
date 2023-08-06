(function() {
  angular.module('cradminLegacy.loadmorepager.services', []).factory('cradminLegacyLoadmorepagerCoordinator', function() {
    /*
    Coordinates between cradminLegacyLoadMorePager directives.
    */

    var Coordinator;
    Coordinator = (function() {
      function Coordinator() {
        this.targets = {};
      }

      Coordinator.prototype.registerPager = function(targetDomId, pagerScope) {
        if (this.targets[targetDomId] == null) {
          this.targets[targetDomId] = {};
        }
        return this.targets[targetDomId][pagerScope.getNextPageNumber()] = pagerScope;
      };

      Coordinator.prototype.unregisterPager = function(targetDomId, pagerScope) {
        return del(this.targets[targetDomId][pagerScope.getNextPageNumber()]);
      };

      Coordinator.prototype.__getPagerScope = function(targetDomId, nextPageNumber) {
        var pagerScope, target;
        target = this.targets[targetDomId];
        if (target == null) {
          throw Error("No target with ID '" + targetDomId + "' registered with cradminLegacyLoadmorepagerCoordinator.");
        }
        pagerScope = target[nextPageNumber];
        if (pagerScope == null) {
          throw Error(("No pagerScope for targetDomId='" + targetDomId + "' and nextPageNumber=" + nextPageNumber + " ") + "registered with cradminLegacyLoadmorepagerCoordinator.");
        }
        return pagerScope;
      };

      return Coordinator;

    })();
    return new Coordinator();
  });

}).call(this);
