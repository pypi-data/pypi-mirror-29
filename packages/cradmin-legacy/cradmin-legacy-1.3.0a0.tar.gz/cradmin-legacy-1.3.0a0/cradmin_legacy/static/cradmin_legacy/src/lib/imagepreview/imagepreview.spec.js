(function() {
  describe('cradminLegacyImagePreviewImg', function() {
    var $compile, $rootScope;
    $compile = null;
    $rootScope = null;
    beforeEach(module('cradminLegacy.imagepreview'));
    beforeEach(inject(function(_$compile_, _$rootScope_) {
      $compile = _$compile_;
      return $rootScope = _$rootScope_;
    }));
    it('should hide IMG if no src', function() {
      var element, html, scope;
      scope = {};
      html = "<div cradmin-legacy-image-preview>\n  <img cradmin-legacy-image-preview-img>\n  <input type=\"file\" name=\"myfile\" cradmin-legacy-image-preview-filefield>\n</div>";
      element = $compile(html)($rootScope);
      $rootScope.$digest();
      return expect(element.find('img').hasClass('ng-hide')).toBe(true);
    });
    return it('should show IMG if src', function() {
      var element, html, scope;
      scope = {};
      html = "<div cradmin-legacy-image-preview>\n  <img cradmin-legacy-image-preview-img src=\"https://upload.wikimedia.org/wikipedia/commons/b/ba/Crystal_Clear_app_tux.png?download\">\n  <input type=\"file\" name=\"myfile\" cradmin-legacy-image-preview-filefield>\n</div>";
      element = $compile(html)($rootScope);
      $rootScope.$digest();
      return expect(element.find('img').hasClass('ng-hide')).toBe(false);
    });
  });

}).call(this);
