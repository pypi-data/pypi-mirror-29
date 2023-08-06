
/*--[ scroller key UP/DOWN ]--------------------------------------------------*/

(function($) {
$.fn.j01SimpleScroller = function(o) {
    o = $.extend({
        // scroller
        loadContentURL: null,
        loadContentViewName: 'index.html',
        loadContentMethodName: 'j01LoadContent',
        loadContentTargetExpression: '#right',
        loadContentResultCallback: j01RenderContent,
        clickExpression: 'li',
        objActiveClass: 'active',
        contentURL: null,
        // custom scroller script settings
        settings: {
            alwaysShowScrollbar: 2,
            scrollInertia: 100,
            mouseWheel: {
                enable: true,
                preventDefault: true
            },
            theme: 'dark-3',
            scrollButtons:{
                enable: true
            },
            // advanced: { autoScrollOnFocus: 'a' },/
            callbacks: {
                onTotalScroll: function() {
                    doEndScrolling();
                },
                onTotalScrollOffset: 50
            }
        },
        // order support
        sortName: null,
        sortOrder: null,
        events: true,
        keyboard: false,
        // search
        searchURL: null,
        searchMethodName: 'getJ01SimpleScrollerResult',
        searchResultExpression: '#j01ScrollerResult',
        searchResultCallback: setSearchResult,
        searchWidgetExpression: null,
        minQueryLenght: 2,
        maxReSearch: 0,
        onAfterRender: null
    }, o || {});

    // scroller
    var wrapper = null;
    var scrollable = null;
    // var selected = null;
    // search support
    var currentSearchText = null;
    var reSearchCounter = 0;
    var loading = false;
    var KEY = {
        BACK: 8,
        DEL: 46,
        DOWN: 40,
        ESC: 27,
        PAGEDOWN: 34,
        PAGEUP: 33,
        ENTER: 13,
        TAB: 9,
        UP: 38
    };

    function doLoadContentCallback(response) {
        o.loadContentResultCallback(response);
    }

    // content loader with search support
    function doLoadContent(url) {
        // load only if not a request is pending
        loading = true;
        proxy = getJSONRPCProxy(url);
        proxy.addMethod(o.loadContentMethodName, doLoadContentCallback);
        proxy[o.loadContentMethodName]();
    }

    function getItemURL(item) {
        var viewName = o.loadContentViewName;
        if (item.data('view')) {
            viewName = item.data('view');
        }
        return o.loadContentURL + '/' + item.attr('id') + '/' + viewName;
    }

    function getSelectedItem() {
        return scrollable.find('.' + o.objActiveClass);
    }

    function doSelectItem(obj) {
        var prev = getSelectedItem();
        if (prev) {
            prev.removeClass(o.objActiveClass);
        }
        if (obj) {
            obj.addClass(o.objActiveClass);
        }
    }

    function doKeyUp() {
        var item = getSelectedItem();
        if (item) {
            var obj = item.prev();
            doSelectItem(obj);
        }
    }

    function doKeyDown() {
        var item = getSelectedItem();
        if (item) {
            var obj = item.next();
            doSelectItem(obj);
        }
    }

    function doKeyEnter() {
        var item = getSelectedItem();
        if (item) {
            var url = getItemURL(item);
            doLoadContent(url);
        }
    }

    function doKeyHandling(event) {
        // setup keyboard handling via events
        if (event) {
            switch(event.keyCode) {
                case KEY.UP:
                    event.preventDefault();
                    scrollable.trigger('j01.scroller.up');
                    return false;
                case KEY.DOWN:
                    event.preventDefault();
                    scrollable.trigger('j01.scroller.down');
                    return false;
                case KEY.ENTER:
                    event.preventDefault();
                    scrollable.trigger('j01.scroller.enter');
                    return false;
            }
        }
    }

    function setUpKeyHandling() {
        if (o.keyboard) {
            // setup key handling
            scrollable.on("keyup", function(event) {
                doKeyHandling(event);
                return false;
            });
        }
    }

    function setUpEventHandling() {
        if (o.events || o.keyboard) {
            // setup event handling if enabled or keyboard is used
            scrollable.bind('j01.scroller.up', function(event) {
                event.preventDefault();
                doKeyUp();
            });
            scrollable.bind('j01.scroller.down', function(event) {
                // event.preventDefault();
                doKeyDown();
            });
            scrollable.bind('j01.scroller.enter', function(event) {
                event.preventDefault();
                doKeyEnter();
            });
            // select item
            scrollable.bind('j01.scroller.select', function(event) {
                event.preventDefault();
                var obj = scrollable.find(event.selector);
                doSelectItem(obj);
            });
        }
    }

    // click handling
    function doClickItem(item) {
        doSelectItem(item);
        var url = getItemURL(item);
        doLoadContent(url);
        return false;
    }

    function setUpClickHandling() {
        scrollable.on("click", o.clickExpression, function() {
            doClickItem($(this));
        });
    }

    // search handling
    function setSearchResult(response) {
        var content = response.content;
        var searchText = $(o.searchWidgetExpression).val();
        if (currentSearchText != searchText) {
            // search again
            if (reSearchCounter < o.maxReSearch) {
                reSearchCounter += 1;
                doLiveSearch();
            }
            loading = false;
            return false;
        }
        reSearchCounter = 0;
        scrollable.empty();
        scrollable.html(content);
        if (o.onAfterRender){
            o.onAfterRender(scrollable);
        }
        loading = false;
    }

    function doLiveSearch() {
        var searchText = $(o.searchWidgetExpression).val();
        // do not search if text is given but to short
        if (searchText && searchText.length < o.minQueryLenght) {
            loading = false;
            return false;
        }
        // search only if not text or min length searchText is given and
        // load only if not a request is pending and there is not cache
        if(!loading) {
            // search if we are not loding and text is given with the correct
            // length and also search if no text is given (reset)
            loading = true;
            currentSearchText = searchText;
            // do livesearch call
            var proxy = getJSONRPCProxy(o.searchURL);
            proxy.addMethod(o.searchMethodName, o.searchResultCallback);
            proxy[o.searchMethodName](o.sortName, o.sortOrder, searchText);
        }
    }

    function setUpSearchWidget() {
        if (o.searchWidgetExpression) {
            // unbind previous event handler
            $(o.searchWidgetExpression).unbind('keyup');
            // now setup live search event handler
            $(o.searchWidgetExpression).bind('keyup', function(){
                doLiveSearch();
            });
        }
    }

    // mCustom scroller setup
    function setUpScroller() {
        wrapper.mCustomScrollbar(o.settings);
    }

    return this.each(function() {
        wrapper = $(this);
        scrollable = $(o.searchResultExpression);
        setUpSearchWidget();
        setUpScroller();
        setUpEventHandling();
        setUpKeyHandling();
        setUpClickHandling();
    });
};
})(jQuery);
