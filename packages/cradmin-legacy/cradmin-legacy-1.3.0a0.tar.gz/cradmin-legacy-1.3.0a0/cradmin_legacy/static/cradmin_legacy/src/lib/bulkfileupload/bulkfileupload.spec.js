(function() {
  angular.module('cradminLegacy.detectizrMockDesktop', []).factory('cradminDetectize', function() {
    return {
      device: {
        type: 'desktop'
      }
    };
  });

  angular.module('cradminLegacy.detectizrMockMobile', []).factory('cradminDetectize', function() {
    return {
      device: {
        type: 'mobile'
      }
    };
  });

  describe('cradminLegacyBulkfileuploadAdvanced', function() {
    var $compile, $rootScope;
    $compile = null;
    $rootScope = null;
    beforeEach(module('cradminLegacy.bulkfileupload', 'cradminLegacy.detectizrMockDesktop'));
    beforeEach(inject(function(_$compile_, _$rootScope_) {
      $compile = _$compile_;
      return $rootScope = _$rootScope_;
    }));
    return it('should hide simple widget', function() {
      var element, html, scope;
      scope = {};
      html = "<form cradmin-legacy-bulkfileupload-form>\n  <div cradmin-legacy-bulkfileupload=\"/file_upload_api_mock\">\n    <div cradmin-legacy-bulkfileupload-advanced-widget id=\"advanced\"></div>\n    <div cradmin-legacy-bulkfileupload-simple-widget id=\"simple\"></div>\n  </div>\n</form>";
      element = $compile(html)($rootScope);
      $rootScope.$digest();
      expect(element.find('#simple').css('display')).toBe('none');
      return expect(element.find('#advanced').css('display')).toBe('');
    });
  });

  describe('cradminLegacyBulkfileuploadMobile', function() {
    var $compile, $rootScope;
    $compile = null;
    $rootScope = null;
    beforeEach(module('cradminLegacy.bulkfileupload', 'cradminLegacy.detectizrMockMobile'));
    beforeEach(inject(function(_$compile_, _$rootScope_) {
      $compile = _$compile_;
      return $rootScope = _$rootScope_;
    }));
    return it('should hide advanced widget', function() {
      var element, html, scope;
      scope = {};
      html = "<form cradmin-legacy-bulkfileupload-form>\n  <div cradmin-legacy-bulkfileupload=\"/file_upload_api_mock\">\n    <div cradmin-legacy-bulkfileupload-advanced-widget id=\"advanced\"></div>\n    <div cradmin-legacy-bulkfileupload-simple-widget id=\"simple\"></div>\n  </div>\n</form>";
      element = $compile(html)($rootScope);
      $rootScope.$digest();
      expect(element.find('#simple').css('display')).toBe('');
      return expect(element.find('#advanced').css('display')).toBe('none');
    });
  });

  describe('cradminLegacyBulkfileuploadInProgressOrFinished', function() {
    var $compile, $rootScope, formElement, getProgressFilenames, getProgressPercents, inProgressOrFinishedElement, inProgressOrFinishedScope;
    $compile = null;
    $rootScope = null;
    formElement = null;
    inProgressOrFinishedElement = null;
    inProgressOrFinishedScope = null;
    beforeEach(module('cradminLegacy.bulkfileupload', 'cradminLegacy.templates', 'cradminLegacy.detectizrMockDesktop'));
    beforeEach(inject(function(_$compile_, _$rootScope_) {
      var html;
      $compile = _$compile_;
      $rootScope = _$rootScope_;
      html = "<form cradmin-legacy-bulkfileupload-form>\n  <div cradmin-legacy-bulkfileupload=\"/file_upload_api_mock\">\n    <div cradmin-legacy-bulkfileupload-progress id=\"progress\"></div>\n  </div>\n</form>";
      formElement = $compile(html)($rootScope);
      $rootScope.$digest();
      inProgressOrFinishedElement = formElement.find('#progress');
      return inProgressOrFinishedScope = inProgressOrFinishedElement.isolateScope();
    }));
    getProgressPercents = function() {
      var domelement, elements, percent, progressPercents, _i, _len;
      progressPercents = [];
      elements = inProgressOrFinishedElement.find('.cradmin-legacy-progresspercent-number');
      for (_i = 0, _len = elements.length; _i < _len; _i++) {
        domelement = elements[_i];
        percent = angular.element(domelement).text().trim();
        progressPercents.push(percent);
      }
      return progressPercents;
    };
    getProgressFilenames = function() {
      var domelement, elements, filename, filenames, _i, _len;
      filenames = [];
      elements = inProgressOrFinishedElement.find('.cradmin-legacy-filename');
      for (_i = 0, _len = elements.length; _i < _len; _i++) {
        domelement = elements[_i];
        filename = angular.element(domelement).text().trim();
        filenames.push(filename);
      }
      return filenames;
    };
    it('should re-render when adding FileInfoList', function() {
      expect(inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item').length).toBe(0);
      inProgressOrFinishedScope.fileInfoLists.push({
        percent: 0,
        files: [
          {
            name: 'test.txt'
          }
        ]
      });
      inProgressOrFinishedScope.$apply();
      return expect(inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item').length).toBe(1);
    });
    it('should re-render when changing percent', function() {
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 0,
          files: [
            {
              name: 'test.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      expect(getProgressPercents()[0]).toBe('0');
      inProgressOrFinishedScope.fileInfoLists[0].percent = '20';
      inProgressOrFinishedScope.$apply();
      return expect(getProgressPercents()[0]).toBe('20');
    });
    it('should render files when one file in each item', function() {
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 0,
          files: [
            {
              name: 'test1.txt'
            }
          ]
        }, {
          percent: 0,
          files: [
            {
              name: 'test2.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      expect(getProgressFilenames()[0]).toBe('test1.txt');
      expect(getProgressFilenames()[1]).toBe('test2.txt');
      return expect(inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-fileinfolist').length).toBe(2);
    });
    it('should render files when multiple files in each item', function() {
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 0,
          files: [
            {
              name: 'test1.txt'
            }, {
              name: 'test2.txt'
            }
          ]
        }, {
          percent: 0,
          files: [
            {
              name: 'test3.txt'
            }, {
              name: 'test4.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      expect(getProgressFilenames()[0]).toBe('test1.txt');
      expect(getProgressFilenames()[1]).toBe('test2.txt');
      expect(getProgressFilenames()[2]).toBe('test3.txt');
      expect(getProgressFilenames()[3]).toBe('test4.txt');
      return expect(inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-fileinfolist').length).toBe(2);
    });
    it('should add finished class when finished', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          finished: true,
          files: [
            {
              name: 'test1.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      return expect(firstItem.hasClass('cradmin-legacy-bulkfileupload-progress-item-finished')).toBe(true);
    });
    it('should add error message on error', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          files: [
            {
              name: 'test1.txt'
            }
          ],
          hasErrors: true,
          errors: {
            file: [
              {
                message: 'File is too big'
              }
            ]
          }
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      expect(firstItem.find('.cradmin-legacy-bulkfileupload-error').length).toBe(1);
      return expect(firstItem.find('.cradmin-legacy-bulkfileupload-error').text().trim()).toBe('File is too big');
    });
    it('should add error class on error', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          files: [
            {
              name: 'test1.txt'
            }
          ],
          hasErrors: true,
          errors: {}
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      return expect(firstItem.hasClass('cradmin-legacy-bulkfileupload-progress-item-error')).toBe(true);
    });
    it('should show delete button when finished', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          finished: true,
          files: [
            {
              name: 'test1.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      return expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button').length).toBe(1);
    });
    it('should not show delete button when not finished', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          finished: false,
          files: [
            {
              name: 'test1.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      return expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button').length).toBe(0);
    });
    it('should not show delete button when not successful', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          finished: true,
          files: [
            {
              name: 'test1.txt'
            }
          ],
          hasErrors: true,
          errors: {}
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      return expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button').length).toBe(0);
    });
    it('should show isRemoving message when removing', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          finished: true,
          files: [
            {
              name: 'test1.txt',
              isRemoving: true
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button-isremoving').length).toBe(1);
      return expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button-isnotremoving').length).toBe(0);
    });
    return it('should not show isRemoving message when not removing', function() {
      var firstItem;
      inProgressOrFinishedScope.fileInfoLists = [
        {
          percent: 100,
          finished: true,
          files: [
            {
              name: 'test1.txt'
            }
          ]
        }
      ];
      inProgressOrFinishedScope.$apply();
      firstItem = inProgressOrFinishedElement.find('.cradmin-legacy-bulkfileupload-progress-item');
      expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button-isremoving').length).toBe(0);
      return expect(firstItem.find('.cradmin-legacy-bulkfileupload-remove-file-button-isnotremoving').length).toBe(1);
    });
  });

}).call(this);
