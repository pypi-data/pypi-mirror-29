(function() {
  angular.module('cradminLegacy.forms.modelchoicefield', []).provider('cradminLegacyModelChoiceFieldCoordinator', function() {
    var ModelChoiceFieldOverlay;
    ModelChoiceFieldOverlay = (function() {
      function ModelChoiceFieldOverlay(cradminLegacyWindowDimensions) {
        this.cradminLegacyWindowDimensions = cradminLegacyWindowDimensions;
        this.modelChoiceFieldIframeWrapper = null;
        this.bodyContentWrapperElement = angular.element('#cradmin_legacy_bodycontentwrapper');
        this.bodyElement = angular.element('body');
      }

      ModelChoiceFieldOverlay.prototype.registerModeChoiceFieldIframeWrapper = function(modelChoiceFieldIframeWrapper) {
        return this.modelChoiceFieldIframeWrapper = modelChoiceFieldIframeWrapper;
      };

      ModelChoiceFieldOverlay.prototype.onChangeValueBegin = function(fieldWrapperScope) {
        return this.modelChoiceFieldIframeWrapper.onChangeValueBegin(fieldWrapperScope);
      };

      ModelChoiceFieldOverlay.prototype.addBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.addClass(cssclass);
      };

      ModelChoiceFieldOverlay.prototype.removeBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.removeClass(cssclass);
      };

      ModelChoiceFieldOverlay.prototype.disableBodyScrolling = function() {
        return this.bodyElement.addClass('cradmin-legacy-noscroll');
      };

      ModelChoiceFieldOverlay.prototype.enableBodyScrolling = function() {
        this.bodyElement.removeClass('cradmin-legacy-noscroll');
        return this.cradminLegacyWindowDimensions.triggerWindowResizeEvent();
      };

      return ModelChoiceFieldOverlay;

    })();
    this.$get = [
      'cradminLegacyWindowDimensions', function(cradminLegacyWindowDimensions) {
        return new ModelChoiceFieldOverlay(cradminLegacyWindowDimensions);
      }
    ];
    return this;
  }).directive('cradminLegacyModelChoiceFieldIframeWrapper', [
    '$window', '$timeout', 'cradminLegacyModelChoiceFieldCoordinator', 'cradminLegacyWindowDimensions', function($window, $timeout, cradminLegacyModelChoiceFieldCoordinator, cradminLegacyWindowDimensions) {
      return {
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.origin = "" + window.location.protocol + "//" + window.location.host;
          $scope.bodyElement = angular.element($window.document.body);
          cradminLegacyModelChoiceFieldCoordinator.registerModeChoiceFieldIframeWrapper(this);
          this.setIframe = function(iframeScope) {
            return $scope.iframeScope = iframeScope;
          };
          this._setField = function(fieldScope) {
            return $scope.fieldScope = fieldScope;
          };
          this._setPreviewElement = function(previewElementScope) {
            return $scope.previewElementScope = previewElementScope;
          };
          this.setLoadSpinner = function(loadSpinnerScope) {
            return $scope.loadSpinnerScope = loadSpinnerScope;
          };
          this.setIframeWrapperInner = function(iframeInnerScope) {
            return $scope.iframeInnerScope = iframeInnerScope;
          };
          this.onChangeValueBegin = function(fieldWrapperScope) {
            this._setField(fieldWrapperScope.fieldScope);
            this._setPreviewElement(fieldWrapperScope.previewElementScope);
            $scope.iframeScope.beforeShowingIframe(fieldWrapperScope.iframeSrc);
            return $scope.show();
          };
          this.onIframeLoadBegin = function() {
            return $scope.loadSpinnerScope.show();
          };
          this.onIframeLoaded = function() {
            $scope.iframeInnerScope.show();
            return $scope.loadSpinnerScope.hide();
          };
          $scope.onChangeValue = function(event) {
            var data;
            if (event.origin !== $scope.origin) {
              console.error("Message origin '" + event.origin + "' does not match current origin '" + $scope.origin + "'.");
              return;
            }
            data = angular.fromJson(event.data);
            if ($scope.fieldScope.fieldid !== data.fieldid) {
              return;
            }
            $scope.fieldScope.setValue(data.value);
            $scope.previewElementScope.setPreviewHtml(data.preview);
            $scope.hide();
            return $scope.iframeScope.afterFieldValueChange();
          };
          $window.addEventListener('message', $scope.onChangeValue, false);
          $scope.onWindowResize = function(newWindowDimensions) {
            return $scope.iframeScope.setIframeSize();
          };
          $scope.show = function() {
            $scope.iframeWrapperElement.addClass('cradmin-legacy-floating-fullsize-iframe-wrapper-show');
            cradminLegacyModelChoiceFieldCoordinator.disableBodyScrolling();
            cradminLegacyModelChoiceFieldCoordinator.addBodyContentWrapperClass('cradmin-legacy-floating-fullsize-iframe-bodycontentwrapper');
            cradminLegacyModelChoiceFieldCoordinator.addBodyContentWrapperClass('cradmin-legacy-floating-fullsize-iframe-bodycontentwrapper-push');
            return cradminLegacyWindowDimensions.register($scope);
          };
          $scope.hide = function() {
            $scope.iframeWrapperElement.removeClass('cradmin-legacy-floating-fullsize-iframe-wrapper-show');
            cradminLegacyModelChoiceFieldCoordinator.removeBodyContentWrapperClass('cradmin-legacy-floating-fullsize-iframe-bodycontentwrapper');
            cradminLegacyModelChoiceFieldCoordinator.removeBodyContentWrapperClass('cradmin-legacy-floating-fullsize-iframe-bodycontentwrapper-push');
            cradminLegacyModelChoiceFieldCoordinator.enableBodyScrolling();
            $scope.iframeScope.onHide();
            return cradminLegacyWindowDimensions.unregister($scope);
          };
          this.closeIframe = function() {
            return $scope.hide();
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.iframeWrapperElement = element;
        }
      };
    }
  ]).directive('cradminLegacyModelChoiceFieldIframeWrapperInner', [
    '$window', function($window) {
      return {
        require: '^^cradminLegacyModelChoiceFieldIframeWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.scrollToTop = function() {
            return $scope.element.scrollTop(0);
          };
          $scope.show = function() {
            return $scope.element.removeClass('ng-hide');
          };
          $scope.hide = function() {
            return $scope.element.addClass('ng-hide');
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.element = element;
          wrapperCtrl.setIframeWrapperInner(scope);
        }
      };
    }
  ]).directive('cradminLegacyModelChoiceFieldIframeClosebutton', function() {
    return {
      require: '^cradminLegacyModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      link: function(scope, element, attrs, iframeWrapperCtrl) {
        element.on('click', function(e) {
          e.preventDefault();
          return iframeWrapperCtrl.closeIframe();
        });
      }
    };
  }).directive('cradminLegacyModelChoiceFieldLoadSpinner', function() {
    return {
      require: '^^cradminLegacyModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      controller: function($scope) {
        $scope.hide = function() {
          return $scope.element.addClass('ng-hide');
        };
        return $scope.show = function() {
          return $scope.element.removeClass('ng-hide');
        };
      },
      link: function(scope, element, attrs, wrapperCtrl) {
        scope.element = element;
        wrapperCtrl.setLoadSpinner(scope);
      }
    };
  }).directive('cradminLegacyModelChoiceFieldIframe', [
    '$interval', function($interval) {
      return {
        require: '^cradminLegacyModelChoiceFieldIframeWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          var currentScrollHeight, getIframeDocument, getIframeScrollHeight, getIframeWindow, resizeIfScrollHeightChanges, scrollHeightInterval, startScrollHeightInterval, stopScrollHeightInterval;
          scrollHeightInterval = null;
          currentScrollHeight = 0;
          getIframeWindow = function() {
            return $scope.element.contents();
          };
          getIframeDocument = function() {
            return getIframeWindow()[0];
          };
          getIframeScrollHeight = function() {
            var iframeDocument;
            iframeDocument = getIframeDocument();
            if ((iframeDocument != null ? iframeDocument.body : void 0) != null) {
              return iframeDocument.body.scrollHeight;
            } else {
              return 0;
            }
          };
          resizeIfScrollHeightChanges = function() {
            var newScrollHeight;
            newScrollHeight = getIframeScrollHeight();
            if (newScrollHeight !== currentScrollHeight) {
              currentScrollHeight = newScrollHeight;
              return $scope.setIframeSize();
            }
          };
          startScrollHeightInterval = function() {
            if (scrollHeightInterval == null) {
              return scrollHeightInterval = $interval(resizeIfScrollHeightChanges, 500);
            }
          };
          stopScrollHeightInterval = function() {
            if (scrollHeightInterval != null) {
              $interval.cancel(scrollHeightInterval);
              return scrollHeightInterval = null;
            }
          };
          $scope.onHide = function() {
            return stopScrollHeightInterval();
          };
          $scope.afterFieldValueChange = function() {
            return stopScrollHeightInterval();
          };
          $scope.beforeShowingIframe = function(iframeSrc) {
            var currentSrc;
            currentSrc = $scope.element.attr('src');
            if ((currentSrc == null) || currentSrc === '' || currentSrc !== iframeSrc) {
              $scope.loadedSrc = currentSrc;
              $scope.wrapperCtrl.onIframeLoadBegin();
              $scope.resetIframeSize();
              $scope.element.attr('src', iframeSrc);
            }
            return startScrollHeightInterval();
          };
          $scope.setIframeSize = function() {};
          $scope.resetIframeSize = function() {};
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.element = element;
          scope.wrapperCtrl = wrapperCtrl;
          wrapperCtrl.setIframe(scope);
          scope.element.on('load', function() {
            wrapperCtrl.onIframeLoaded();
            return scope.setIframeSize();
          });
        }
      };
    }
  ]).directive('cradminLegacyModelChoiceFieldWrapper', [
    'cradminLegacyModelChoiceFieldCoordinator', function(cradminLegacyModelChoiceFieldCoordinator) {
      return {
        restrict: 'A',
        scope: {
          iframeSrc: '@cradminLegacyModelChoiceFieldWrapper'
        },
        controller: function($scope) {
          this.setField = function(fieldScope) {
            return $scope.fieldScope = fieldScope;
          };
          this.setPreviewElement = function(previewElementScope) {
            return $scope.previewElementScope = previewElementScope;
          };
          this.onChangeValueBegin = function() {
            return cradminLegacyModelChoiceFieldCoordinator.onChangeValueBegin($scope);
          };
        }
      };
    }
  ]).directive('cradminLegacyModelChoiceFieldInput', [
    'cradminLegacyModelChoiceFieldCoordinator', function(cradminLegacyModelChoiceFieldCoordinator) {
      return {
        require: '^^cradminLegacyModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.setValue = function(value) {
            return $scope.inputElement.val(value);
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.inputElement = element;
          scope.fieldid = attrs['id'];
          wrapperCtrl.setField(scope);
        }
      };
    }
  ]).directive('cradminLegacyModelChoiceFieldPreview', [
    'cradminLegacyModelChoiceFieldCoordinator', function(cradminLegacyModelChoiceFieldCoordinator) {
      return {
        require: '^^cradminLegacyModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.setPreviewHtml = function(previewHtml) {
            return $scope.previewElement.html(previewHtml);
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.previewElement = element;
          wrapperCtrl.setPreviewElement(scope);
        }
      };
    }
  ]).directive('cradminLegacyModelChoiceFieldChangebeginButton', [
    'cradminLegacyModelChoiceFieldCoordinator', function(cradminLegacyModelChoiceFieldCoordinator) {
      return {
        require: '^^cradminLegacyModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        link: function(scope, element, attrs, wrapperCtrl) {
          element.on('click', function(e) {
            e.preventDefault();
            return wrapperCtrl.onChangeValueBegin();
          });
        }
      };
    }
  ]);

}).call(this);
