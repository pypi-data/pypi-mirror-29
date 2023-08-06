//-----------------------------------------------------------------------------
// j01.dialog javascript
//-----------------------------------------------------------------------------
//
// NOTE. loading a dialog with jsonrpc or ajax requires that the dialog contains
// a root element with the id j01Dialog. You can only use another element id
// if you show a dialog already containd in the DOM. Also note that we use
// fix element id selectors for close controls, iframe, holder and overlay.
// The selectors are:
//
// - #j01DialogOverlay
// - #j01DialogHolder
// - #j01DialogClose
// - #j01Dialog

function getJ01DialogFrameSize(iframe) {
    var win = iframe.contentWindow;
    var doc = iframe.contentWindow.document;
    var xScroll;
    if (win.innerHeight && win.scrollMaxX) {
        xScroll = win.innerWidth + win.scrollMaxX;
    } else if (doc.body.scrollWidth > doc.body.offsetWidth){
        // all but Explorer Mac
        xScroll = doc.body.scrollWidth;
    } else {
        // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
        xScroll = doc.body.offsetWidth;
    }
    var yScroll;
    if (win.innerHeight && win.scrollMaxY) {
        yScroll = win.innerHeight + win.scrollMaxY;
    } else if (doc.body.scrollHeight > doc.body.offsetHeight){
        // all but Explorer Mac
        yScroll = doc.body.scrollHeight;
    } else {
        // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
        yScroll = doc.body.offsetHeight;
    }

    var winWidth, winHeight;
    if (win.innerHeight) {  // all except Explorer
        if(doc.documentElement.clientWidth){
            winWidth = doc.documentElement.clientWidth;
        } else {
            winWidth = win.innerWidth;
        }
        winHeight = win.innerHeight;
    } else if (doc.documentElement && doc.documentElement.clientHeight) {
        // Explorer 6 Strict Mode
        winWidth = doc.documentElement.clientWidth;
        winHeight = doc.documentElement.clientHeight;
    } else if (doc.body) { // other Explorers
        winWidth = doc.body.clientWidth;
        winHeight = doc.body.clientHeight;
    }

    // for small pages with total height less then height of the viewport
    var pageWidth, pageHeight;
    if(yScroll == 0){
        pageHeight = winHeight;
    } else {
        pageHeight = yScroll;
    }

    // for small pages with total width less then width of the viewport
    if(xScroll == 0){
        pageWidth = winWidth;
    } else {
        pageWidth = xScroll;
    }

    return [pageWidth, pageHeight];
};

function setUpJ01DialogOverlay() {
    // set overlay
    var j01DialogOverlay = $('#j01DialogOverlay');
    if (j01DialogOverlay.length == 0){
        j01DialogOverlay = $('<div id="j01DialogOverlay"></div>');
        $(document.body).append(j01DialogOverlay);
        j01DialogOverlay.click(function(e){
            j01DialogClose();
        });
    }
}

function setUpJ01DialogHolder(dlg) {
    var holder = $('#j01DialogHolder');
    if (holder.length == 0){
        holder = $('<div id="j01DialogHolder"></div>');
        $(document.body).append(holder);
    }
    if (typeof(dlg) !== 'undefined') {
        holder.append(dlg);
    }
}

function setUpJ01DialogCloseHandlers(dlg) {
    // apply close handler if new content contains j01DialogClose
    $('#j01DialogClose', dlg).click( function(e){
        j01DialogClose();
    });
    // apply ESC key
    $(document).on('keydown.j01dialog', function(e) {
        if(!e){
            e = window.event;
        }
        keycode = e.keyCode ? e.keyCode : e.which;
        if(keycode == 27){
            j01DialogClose();
        }
    });
}

function setUpJ01DialogCenterOnResize(dlg) {
    var skipCenterOnResize = dlg.data('j01dialog-skip-center-on-resize');
    if (typeof(skipCenterOnResize) === 'undefined' || skipCenterOnResize == '0') {
        $(window).on('resize.j10dialog', function(){
            // bind center to resize event
            j01DialogResize(dlg);
        });
    }
}
function setUpJ01DialogCenterOnScroll(dlg) {
    var skipCenterOnScroll = dlg.data('j01dialog-skip-center-on-scroll');
    if (typeof(skipCenterOnScroll) === 'undefined' || skipCenterOnScroll == '0') {
        $(window).on('scroll.j10dialog', function(){
            // bind center to scroll event
            j01DialogCenter(dlg);
        });
    }
}

function j01DialogClose(url){
    var j01DialogOverlay = $("#j01DialogOverlay");
    var j01DialogHolder = $('#j01DialogHolder');
    var j01DialogIFrame = $('iframe#j01DialogIFrame', j01DialogHolder);
    var j01DialogClose = ('#j01DialogClose', j01DialogHolder);
    var dlg = $('#j01Dialog', j01DialogHolder);
    // unbind event handler
    $(window).off('resize.j10dialog');
    $(window).off('scroll.j10dialog');
    j01DialogClose.off('click');
    j01DialogOverlay.off("click")
    // remove elements
    j01DialogOverlay.remove();
    if (j01DialogIFrame.length) {
        j01DialogIFrame.unbind('load');
    }
    dlg.hide();
    dlg.remove();
    j01DialogHolder.remove();
    // document.onkeydown = "";
    $(document).off('keydown.j01dialog');
    if (typeof url !== 'undefined' && url){
        window.location = url;
        return false;
    }
}

function j01DialogCenter(dlg){
    var skipCenter = dlg.data('j01dialog-skip-center');
    if (typeof(skipCenter) === 'undefined' || skipCenter == '0') {
        if (typeof(dlg) === 'undefined' || !dlg) {
            dlg = $('#j01Dialog');
        }
        var wh = $(window).height();
        var ww = $(window).width();
        var dh = dlg.height();
        var dw = dlg.width();
        if (wh < dh || ww < dw) {
            // don't center if dialog is bigger then the window.
            // this prevents that the dialog get re-positioned during scrolling
            return false;
        }
        // calculate position
        var top = wh/2 - dh/2 + $(window).scrollTop();
        var left = ww/2 - dw/2 + $(window).scrollLeft();
        // never use a negativ top or left value
        top = Math.max(top, 0);
        left = Math.max(left, 0);
        dlg.css({left: left +'px', top: top +'px'});
    }
}

function j01DialogResize(dlg) {
    var skipResize = dlg.data('j01dialog-skip-resize');
    if (typeof(skipResize) === 'undefined' || skipResize == '0') {
        var j01DialogIFrame = $('iframe#j01DialogIFrame', dlg);
        if (j01DialogIFrame.length) {
            // unbind resize handler
            j01DialogIFrame.unbind('load');
            // use j01DialogResize and use dlg as argument,
            // find iframe if available
            try {
                arrayPageSize = getJ01DialogFrameSize(j01DialogIFrame.get(0));
                w = arrayPageSize[0];
                h = arrayPageSize[1];
            } catch(err) {
                w = dlg.width();
                h = dlg.height();
            }
            j01DialogIFrame.css({'width': w +'px', 'height': h +'px'});
        } else {
            // remove old size
            dlg.css({'width': '', 'height': ''});
            // get calculated new width
            width = dlg.width();
            height = dlg.height();
            // make sure the content is not smaller then the title
            closeWidth = Math.max($('#j01DialogClose', dlg).width(), 0);
            controlsWidth = Math.max($('#j01DialogControls', dlg).width(), 0);
            // needs a padding-right in title as workarround for the floating close div
            minWidth = closeWidth + controlsWidth;
            width = Math.max(width, minWidth);
            dlg.css({'width': dlg.width() +'px', 'height': dlg.height() +'px'});
        }
    }
    // show dialog
    dlg.show();
    if (typeof(skipResize) === 'undefined' || skipResize == '0') {
        j01DialogCenter(dlg);
        if (j01DialogIFrame.length) {
            // apply onload function
            j01DialogIFrame.load(function() {
                j01DialogResize(dlg);
            });
        }
    }
};

function j01DialogRenderContentError(response) {
    // handle error response
    /* see: z3c.publisher.interfaces.IJSONRPCErrorView
     * The z3c.publisher returns the following error data for jsonrpc 2.0
     * {'jsonrpc': self._request.jsonVersion,
     *  'error': {'code': result.code,
     *  'message': '<server error message>',
     *  'data': {
     *      'i18nMessage': '<i18n server error message>'
     *      'nextURL': '<optional url for unauthorized page access>'
     *  },
     *  'id': self._request.jsonId
     * }
     */
    var dlg  = $('#j01Dialog');
    var dlgContent = $('#j01DialogContent', dlg);
    var msg = 'Error';
    if (typeof(response.data.nextURL) !== 'undefined') {
        // support unauthorized jsonrpc error view
        window.location.href = response.data.nextURL;
    } else {
        if (response.data.i18nMessage){
            msg = response.data.i18nMessage;
        }else {
            msg = response.message;
        }
        // show error message in dialog content
        dlgContent.empty();
        contentWrapper = $('<div id="j01DialogError"></div>');
        contentWrapper.append(msg);
        dlgContent.html(contentWrapper);
        j01DialogResize(dlg);
        setUpJ01DialogCenterOnScroll(dlg);
    }
};

function j01DialogRenderContentSuccess(response, contentTargetExpression) {
    // callback method which knows how to redirect, render content into a
    // dialog or content area
    if (typeof(contentTargetExpression) === 'undefined') {
        // only used if we close a dialog
        var contentTargetExpression = '#content';
    }
    var dlg  = $('#j01Dialog');
    var dlgContent = $('#j01DialogContent', dlg);
    if (response.nextURL && response.closeDialog) {
        // handle redirect and support close dialog. note a plain redirect
        // with "window.location = response.nextURL;" whould not work if we
        // use urls like ../index.html#6/shortComments.html?j=1&c=r&_suid=..
        // including anchors if we enable history support
        j01DialogClose(response.nextURL);
        return false;
    }else if (response.nextURL) {
        // load nextURL into dialog
        var onTimeout = null,
            isPushState = false;
        proxy = getJSONRPCProxy(response.nextURL);
        proxy.addMethod('j01DialogContent', j01DialogRenderContentSuccess,
            j01DialogRenderContentError, onTimeout, isPushState,
            'j01DialogRenderContent');
        try {
            params = j01URLToArray(response.nextURL);
        } catch(err) {
            // j01URLToArray not available from j01.jsonrpc.js
            params  = false;
        }
        if (params) {
            proxy.j01DialogContent(params);
        }else{
            proxy.j01DialogContent();
        }
        return false;
    }else if (response.content && response.closeDialog) {
        // handle close dialog and content
        if (response.contentTargetExpression) {
            var contentTarget = $(response.contentTargetExpression);
        }else{
            var contentTarget = $(contentTargetExpression);
        }
        j01DialogClose();
        contentTarget.empty();
        contentTarget.html(response.content);
    }else if (response.content) {
        // handle new dialog content
        dlgContent.empty();
        dlgContent.html(response.content);
        setUpJ01DialogCloseHandlers(dlg);
        j01DialogResize(dlg);
    }else if (response.closeDialog) {
        // handle close dialog without content
        j01DialogClose();
        return false;
    }
    setUpJ01DialogCenterOnResize(dlg);
    setUpJ01DialogCenterOnScroll(dlg);
};

// generic success and error response handler
function j01DialogRenderContent(response) {
    if (response.code) {
        // error handling (only works with jsonrpc 2.0)
        j01DialogRenderContentError(response);
    } else {
        // success handling
        j01DialogRenderContentSuccess(response, '#j01DialogContent');
    }
}

// J01Dialog
var J01Dialog = function(settings) {
    this.settings = $.extend({
        url: false,
        skipCenter: false,
        skipResize: false,
        skipCenterOnResize: false,
        skipCenterOnScroll: false,
        j01DialogExpression: false,
        loadDialogWithJSONRPC: true,
        params: false
    }, settings);

    this.dlgHolder = false;
    this.dlg = false;
};

J01Dialog.prototype.loadDialog = function(url) {
    // load content by ajax or JSON-RPC
    // load dialog
    if (this.settings.j01DialogExpression) {
        return $(this.settings.j01DialogExpression);
    }
    // take url from settings
    if (!url || url === 'undefined') {
        var url = this.settings.url;
    }
    // url could still be false
    if (url && this.settings.loadDialogWithJSONRPC) {
        // load content non async
        var onSuccess = null,
            onError = null,
            onTimeout = null,
            isPushState = null;
        proxy = getJSONRPCProxy(url);
        proxy.addMethod('j01Dialog', onSuccess, onError, onTimeout,
            isPushState, 'j01Dialog');
        // force to get full repsonse for better error handling
        if (this.settings.params) {
            var params = this.settings.params;
        }else {
            var params = {};
        }
        try {
            params = j01URLToArray(url, params);
        }catch(err) {
            // j01URLToArray not available
            params = false;
        }
        if (params) {
            var content = proxy.j01Dialog(params);
        }else{
            var content = proxy.j01Dialog();
        }
        if (typeof(content) !== 'undefined' && content) {
            if (content.message) {
                if (content.data && content.data.i18nMessage) {
                    alert(content.data.i18nMessage); // p01.checker.silence
                }else{
                    alert(content.message); // p01.checker.silence
                }
                return false;
            }else{
                return $(content);
            }
        }else{
            return false;
        }
    }else if (url) {
        if (url.indexOf("?") > -1) {
            url += "&random=" + (new Date().getTime());
        }else{
            url += "?random=" + (new Date().getTime());
        }
        var content = $.ajax({url: url, async: false}).responseText;
        return $(content);
    }else {
        alert("No url or expression given for load dialog"); // p01.checker.silence
        return false;
    }
};

J01Dialog.prototype.setUpDialog = function(url) {
    // render dialog
    var self = this;
    this.dlg = this.loadDialog(url);
    if (!this.dlg) {
        return false;
    }
    // hide dialog before resize
    this.dlg.hide();
    // apply dialog settings as data attributes
    var skipCenter = this.settings.skipCenter;
    if (skipCenter) {
        skipCenter = '1'
    } else {
        skipCenter = '0'
    }
    var skipResize = this.settings.skipResize;
    if (skipResize) {
        skipResize = '1'
    } else {
        skipResize = '0'
    }
    var skipCenterOnResize = this.settings.skipCenterOnResize;
    if (skipCenterOnResize) {
        skipCenterOnResize = '1'
    } else {
        skipCenterOnResize = '0'
    }
    var skipCenterOnScroll = this.settings.skipCenterOnScroll;
    if (skipCenterOnScroll) {
        skipCenterOnScroll = '1'
    } else {
        skipCenterOnScroll = '0'
    }
    this.dlg.data('j01dialog-skip-center', skipCenter);
    this.dlg.data('j01dialog-skip-resize', skipResize);
    this.dlg.data('j01dialog-skip-center-on-resize', skipCenterOnResize);
    this.dlg.data('j01dialog-skip-center-on-scroll', skipCenterOnScroll);
    // this.setupOverlay();
    setUpJ01DialogOverlay();
    // setup dialog container
    setUpJ01DialogHolder(this.dlg);
    // setup close handler
    setUpJ01DialogCloseHandlers(this.dlg);
    // resize and shoe dialog
    j01DialogResize(this.dlg);
    // apply resize handler
    setUpJ01DialogCenterOnResize(this.dlg);
    setUpJ01DialogCenterOnScroll(this.dlg);
};

J01Dialog.prototype.doClose = function(e) {
    var sourceobj = window.event? window.event.srcElement : e.target;
    if (/Close/i.test(sourceobj.getAttribute("title"))) {
       // self.hideDialog();
        j01DialogClose();
    }
    return false;
};

/**
 * j01LoadContent without delegation (not recommended)
 * this plugin does not re bind handlers for new loaded content
 */
(function($) {
$.fn.j01Dialog = function(settings) {
    // setup loader with given settings
    return this.each(function(){
        // apply event handler to links
        $(this).click(function(event){
            var dialog = new J01Dialog(settings);
            var url = $(this).attr('href');
            dialog.setUpDialog(url);
            event.preventDefault();
            return false;
        });
    });
};
})(jQuery);

/**
 * j01DialogOn (only recommended for non click events on links)
 * This method does not get the href as url from <a> tag. You must
 * define j01DialogExpression or a url in settings.
 */
(function($) {
$.fn.j01DialogOn = function(events, selector, settings) {
    // apply delegated event handler
    return this.on(events, selector, function(event){
        // XXX: implement j01DialogExpression or url value check
        var dialog = new J01Dialog(settings);
        dialog.setUpDialog(dialog.settings.url);
        event.preventDefault();
        return false;
    });
};
})(jQuery);

/**
 * j01DialogOnClick uses delegation pattern (recommended) and works on new
 * loaded content
 */
(function($) {
$.fn.j01DialogOnClick = function(selector, settings) {
    // apply delegated event handler to click event
    if(typeof selector === "object"){
        // only settings given, use default selector and adjust settings
        var settings = selector;
        var selector = 'a.j01DialogLink';
    }else if(typeof selector === "undefined"){
        // non argument given, use default selector
        var selector = 'a.j01DialogLink';
    }
    return this.on('click', selector, function(event){
        var dialog = new J01Dialog(settings);
        if ($(this).is('a')){
            var url = $(this).attr('href');
        }else{
            var url = dialog.settings.url;
        }
        dialog.setUpDialog(url);
        event.preventDefault();
        return false;
    });
};
})(jQuery);

//j01Dialog without any event handler (non JQuery)
function j01Dialog(settings) {
    // setup and resize
    var self = new J01Dialog(settings);
    self.setUpDialog(self.settings.url);
    // self.centerDialog();
    j01DialogCenter(self.dlg);
};


(function($) {
$.fn.j01DialogContent = function (settings) {
    settings = $.extend({
        targetContainerExpression: '#j01DialogContent',
        callback: j01DialogRenderContent,
        onSuccess: j01DialogRenderContentSuccess,
        onError: j01DialogRenderContentError,
        onTimeout: null,
        isPushState: false,
        requestId: 'j01DialogContent'
    }, settings);

    // load content from server via jsonrpc
    function loadContent(self) {
        var url = $(self).attr('href');
        proxy = getJSONRPCProxy(url);
        proxy.addMethod('j01DialogContent', settings.onSuccess,
            settings.onError, settings.onTimeout, settings.isPushState,
            settings.requestId);
        try {
            params = j01URLToArray(url);
        } catch(err) {
            // j01URLToArray not available
            params  = false;
        }
        if (params) {
            proxy.j01DialogContent(params);
        }else{
            proxy.j01DialogContent();
        }
    }

    // apply event handler to links
    return this.each(function(){
        $(this).click(function(){
            loadContent(this);
            return false;
        });
    });
};
})(jQuery);
