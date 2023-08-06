(function() {
  angular.module('cradminLegacy.imagepreview', []).directive('cradminLegacyImagePreview', function() {
    /*
    A directive that shows a preview when an image field changes
    value.
    
    Components:
      - A wrapper (typically a DIV) using this directive (``cradmin-legacy-image-preview``)
      - An IMG element using the ``cradmin-legacy-image-preview-img`` directive. This is
        needed even if we have no initial image.
      - A file input field using the ``cradmin-legacy-image-preview-filefield`` directive.
    
    Example:
    
      <div cradmin-legacy-image-preview>
        <img cradmin-legacy-image-preview-img>
        <input type="file" name="myfile" cradmin-legacy-image-preview-filefield>
      </div>
    */

    var controller;
    controller = function($scope) {
      this.setImg = function(imgscope) {
        return $scope.cradminImagePreviewImage = imgscope;
      };
      this.previewFile = function(file) {
        return $scope.cradminImagePreviewImage.previewFile(file);
      };
    };
    return {
      restrict: 'A',
      controller: controller
    };
  }).directive('cradminLegacyImagePreviewImg', function() {
    var controller, link, onFilePreviewLoaded;
    onFilePreviewLoaded = function($scope, srcData) {
      $scope.element.attr('height', '');
      $scope.element[0].src = srcData;
      return $scope.element.removeClass('ng-hide');
    };
    controller = function($scope) {
      $scope.previewFile = function(file) {
        var reader;
        reader = new FileReader();
        reader.onload = function(evt) {
          return onFilePreviewLoaded($scope, evt.target.result);
        };
        return reader.readAsDataURL(file);
      };
    };
    link = function($scope, element, attrs, previewCtrl) {
      $scope.element = element;
      previewCtrl.setImg($scope);
      if ((element.attr('src') == null) || element.attr('src') === '') {
        element.addClass('ng-hide');
      }
    };
    return {
      require: '^cradminLegacyImagePreview',
      restrict: 'A',
      scope: {},
      controller: controller,
      link: link
    };
  }).directive('cradminLegacyImagePreviewFilefield', function() {
    var link;
    link = function($scope, element, attrs, previewCtrl) {
      $scope.previewCtrl = previewCtrl;
      $scope.element = element;
      $scope.wrapperelement = element.parent();
      element.bind('change', function(evt) {
        var file;
        if (evt.target.files != null) {
          file = evt.target.files[0];
          return $scope.previewCtrl.previewFile(file);
        }
      });
      element.bind('mouseover', function() {
        return $scope.wrapperelement.addClass('cradmin-legacy-filewidget-field-and-overlay-wrapper-hover');
      });
      element.bind('mouseleave', function() {
        return $scope.wrapperelement.removeClass('cradmin-legacy-filewidget-field-and-overlay-wrapper-hover');
      });
    };
    return {
      require: '^cradminLegacyImagePreview',
      restrict: 'A',
      scope: {},
      link: link
    };
  });

}).call(this);
