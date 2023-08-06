#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Page module."""

import asyncio
import base64
import json
import math
import mimetypes
from types import SimpleNamespace
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

from pyee import EventEmitter

from pyppeteer import helper
from pyppeteer.connection import Session
from pyppeteer.dialog import Dialog
from pyppeteer.element_handle import ElementHandle  # noqa: F401
from pyppeteer.emulation_manager import EmulationManager
from pyppeteer.errors import PageError
from pyppeteer.frame_manager import Frame  # noqa: F401
from pyppeteer.frame_manager import FrameManager
from pyppeteer.input import Keyboard, Mouse, Touchscreen
from pyppeteer.navigator_watcher import NavigatorWatcher
from pyppeteer.network_manager import NetworkManager, Response
from pyppeteer.tracing import Tracing


class Page(EventEmitter):
    """Page class."""

    Events = SimpleNamespace(
        Console='console',
        Dialog='dialog',
        Error='error',
        PageError='pageerror',
        Request='request',
        Response='response',
        RequestFailed='requestfailed',
        RequestFinished='requestfinished',
        FrameAttached='frameattached',
        FrameDetached='framedetached',
        FrameNavigated='framenavigated',
        Load='load',
    )

    PaperFormats: Dict[str, Dict[str, float]] = dict(
        letter={'width': 8.5, 'height': 11},
        legal={'width': 8.5, 'height': 14},
        tabloid={'width': 11, 'height': 17},
        ledger={'width': 17, 'height': 11},
        a0={'width': 33.1, 'height': 46.8},
        a1={'width': 23.4, 'height': 33.1},
        a2={'width': 16.5, 'height': 23.4},
        a3={'width': 11.7, 'height': 16.5},
        a4={'width': 8.27, 'height': 11.7},
        a5={'width': 5.83, 'height': 8.27},
    )

    def __init__(self, client: Session,
                 ignoreHTTPSErrors: bool = True,
                 screenshotTaskQueue: list = None,
                 ) -> None:
        """Make new page object."""
        super().__init__()
        self._client = client
        self._keyboard = Keyboard(client)
        self._mouse = Mouse(client, self._keyboard)
        self._touchscreen = Touchscreen(client, self._keyboard)
        self._frameManager = FrameManager(client, self._mouse, self._touchscreen)  # noqa: E501
        self._networkManager = NetworkManager(client)
        self._emulationManager = EmulationManager(client)
        self._tracing = Tracing(client)
        self._pageBindings: Dict[str, Callable] = dict()
        self._ignoreHTTPSErrors = ignoreHTTPSErrors

        if screenshotTaskQueue is None:
            screenshotTaskQueue = list()
        self._screenshotTaskQueue = screenshotTaskQueue

        _fm = self._frameManager
        _fm.on(FrameManager.Events.FrameAttached,
               lambda event: self.emit(Page.Events.FrameAttached, event))
        _fm.on(FrameManager.Events.FrameDetached,
               lambda event: self.emit(Page.Events.FrameDetached, event))
        _fm.on(FrameManager.Events.FrameNavigated,
               lambda event: self.emit(Page.Events.FrameNavigated, event))

        _nm = self._networkManager
        _nm.on(NetworkManager.Events.Request,
               lambda event: self.emit(Page.Events.Request, event))
        _nm.on(NetworkManager.Events.Response,
               lambda event: self.emit(Page.Events.Response, event))
        _nm.on(NetworkManager.Events.RequestFailed,
               lambda event: self.emit(Page.Events.RequestFailed, event))
        _nm.on(NetworkManager.Events.RequestFinished,
               lambda event: self.emit(Page.Events.RequestFinished, event))

        client.on('Page.loadEventFired',
                  lambda event: self.emit(Page.Events.Load))
        client.on('Runtime.consoleAPICalled',
                  lambda event: self._onConsoleAPI(event))
        client.on('Page.javascriptDialogOpening',
                  lambda event: self._onDialog(event))
        client.on('Runtime.exceptionThrown',
                  lambda exception: self._handleException(
                      exception.get('exceptionDetails')))
        client.on('Security.certificateError',
                  lambda event: self._onCertificateError(event))
        client.on('Inspector.targetCrashed',
                  lambda event: self._onTargetCrashed())

    def _onTargetCrashed(self, *args: Any, **kwargs: Any) -> None:
        self.emit('error', PageError('Page crashed!'))

    @property
    def mainFrame(self) -> Optional['Frame']:
        """Get main frame."""
        return self._frameManager._mainFrame

    @property
    def keyboard(self) -> Keyboard:
        """Get keybord object."""
        return self._keyboard

    @property
    def touchscreen(self) -> Touchscreen:
        """Get touchscreen object."""
        return self._touchscreen

    async def tap(self, selector: str) -> None:
        """Tap the element which matches selector."""
        handle = await self.J(selector)
        if not handle:
            raise PageError('No node found for selector: ' + selector)
        await handle.tap()
        await handle.dispose()

    @property
    def tracing(self) -> 'Tracing':
        """Get tracing object."""
        return self._tracing

    @property
    def frames(self) -> List['Frame']:
        """Get frames."""
        return list(self._frames.values())

    async def setRequestInterceptionEnabled(self, value: bool) -> None:
        """Enable request interception."""
        return await self._networkManager.setRequestInterceptionEnabled(value)

    def _onCertificateError(self, event: Any) -> None:
        if not self._ignoreHTTPSErrors:
            return
        asyncio.ensure_future(
            self._client.send('Security.handleCertificateError', {
                'eventId': event.get('eventId'),
                'action': 'continue'
            })
        )

    async def querySelector(self, selector: str) -> Optional['ElementHandle']:
        """Get Element which matches `selector`."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return await frame.querySelector(selector)

    async def querySelectorEval(self, selector: str, pageFunction: str,
                                *args: Any) -> Optional[Any]:
        """Execute function on element which matches selector."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return await frame.querySelectorEval(selector, pageFunction, *args)

    async def querySelectorAll(self, selector: str
                               ) -> List['ElementHandle']:
        """Get Element which matches `selector`."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return await frame.querySelectorAll(selector)

    #: alias to querySelector
    J = querySelector
    #: alias to querySelectorEval
    Jeval = querySelectorEval
    #: alias to querySelectorAll
    JJ = querySelectorAll

    async def cookies(self, *urls: str) -> dict:
        """Get cookies."""
        if not urls:
            urls = (self.url, )
        resp = await self._client.send('Network.getCookies', {
            'urls': urls,
        })
        return resp.get('cookies', {})

    async def deleteCookie(self, *cookies: dict) -> None:
        """Delete cookie."""
        pageURL = self.url
        for cookie in cookies:
            item = dict(**cookie)
            if not cookie.get('url') and pageURL.startswith('http'):
                item['url'] = pageURL
            await self._client.send('Network.deleteCookies', item)

    async def setCookie(self, *cookies: dict) -> None:
        """Set cookies."""
        items = []
        for cookie in cookies:
            item = dict(**cookie)
            pageURL = self.url
            if 'url' not in item and pageURL.startswith('http'):
                item['url'] = pageURL
            items.append(item)
        await self.deleteCookie(*items)
        if items:
            await self._client.send('Network.setCookies', {
                'cookies': items,
            })

    async def addScriptTag(self, url: str) -> str:
        """Add script tag to this page."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return await frame.addScriptTag(url)

    async def injectFile(self, filePath: str) -> str:
        """Inject file to this page."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return await frame.injectFile(filePath)

    async def exposeFunction(self, name: str, puppeteerFunction: Callable
                             ) -> None:
        """Execute function on this page."""
        if self._pageBindings[name]:
            raise PageError(f'Failed to add page binding with name {name}: '
                            'window["{name}"] already exists!')
        self._pageBindings[name] = puppeteerFunction

        addPageBinding = '''
function addPageBinding(bindingName) {
  window[bindingName] = async(...args) => {
    const me = window[bindingName];
    let callbacks = me['callbacks'];
    if (!callbacks) {
      callbacks = new Map();
      me['callbacks'] = callbacks;
    }
    const seq = (me['lastSeq'] || 0) + 1;
    me['lastSeq'] = seq;
    const promise = new Promise(fulfill => callbacks.set(seq, fulfill));
    // eslint-disable-next-line no-console
    console.debug('driver:page-binding', JSON.stringify({name: bindingName, seq, args}));
    return promise;
  };
}
        '''  # noqa: E501
        expression = helper.evaluationString(addPageBinding, name)
        await self._client.send('Page.addScriptToEvaluateOnNewDocument',
                                {'source': expression})
        await self._client.send('Runtime.evaluate', {
            'expression': expression,
            'returnByValue': True
        })

    async def authenticate(self, credentials: Dict[str, str]) -> Any:
        """Provide credentials for http authentication.

        `credentials` should be `None` or dict which has `username` and
        `password` in its keys.
        """
        return await self._networkManager.authenticate(credentials)

    async def setExtraHTTPHeaders(self, headers: Dict[str, str]) -> None:
        """Set extra http headers."""
        return await self._networkManager.setExtraHTTPHeaders(headers)

    async def setUserAgent(self, userAgent: str) -> None:
        """Set user agent."""
        return await self._networkManager.setUserAgent(userAgent)

    def _handleException(self, exceptionDetails: Dict) -> None:
        message = helper.getExceptionMessage(exceptionDetails)
        self.emit(Page.Events.PageError, PageError(message))

    async def _onConsoleAPI(self, event: dict) -> None:
        _args = event.get('args', [])
        if (event.get('type') == 'debug' and _args and
                _args[0]['value'] == 'driver:page-binding'):
            obj = json.loads(_args[1]['value'])
            name = obj.get('name')
            seq = obj.get('seq')
            args = obj.get('args')
            result = await self._pageBindings[name](*args)

            deliverResult = '''
function deliverResult(name, seq, result) {
  window[name]['callbacks'].get(seq)(result)
  window[name]['callbacks'].delete(seq)
}
            '''
            expression = helper.evaluationString(deliverResult, name, seq,
                                                 result)
            await self._client.send('Runtime.evaluate', {
                'expression': expression
            })
            return

        if not self.listeners(Page.Events.Console):
            for arg in _args:
                await helper.releaseObject(self._client, arg)
            return

        _values = []
        for arg in _args:
            _values.append(asyncio.ensure_future(
                helper.serializeRemoteObject(self._client, arg)))
        values = await asyncio.gather(*_values)
        self.emit(Page.Events.Console, *values)

    def _onDialog(self, event: Any) -> None:
        dialogType = ''
        _type = event.get('type')
        if _type == 'alert':
            dialogType = Dialog.Type.Alert
        elif (_type == 'confirm'):
            dialogType = Dialog.Type.Confirm
        elif (_type == 'prompt'):
            dialogType = Dialog.Type.Prompt
        elif (_type == 'beforeunload'):
            dialogType = Dialog.Type.BeforeUnload
        dialog = Dialog(self._client, dialogType, event.get('message'),
                        event.get('defaultPrompt'))
        self.emit(Page.Events.Dialog, dialog)

    @property
    def url(self) -> str:
        """Get url of this page."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return frame.url

    async def content(self) -> str:
        """Get the whole HTML contents of the page."""
        return await self.evaluate('''
() => {
  let retVal = '';
  if (document.doctype)
    retVal = new XMLSerializer().serializeToString(document.doctype);
  if (document.documentElement)
    retVal += document.documentElement.outerHTML;
  return retVal;
}
        '''.strip())

    async def setContent(self, html: str) -> None:
        """Set content."""
        func = '''
function(html) {
  document.open();
  document.write(html);
  document.close();
}
'''
        await self.evaluate(func, html)

    async def goto(self, url: str, options: dict = None, **kwargs: Any
                   ) -> Optional[Response]:
        """Got to url."""
        if options is None:
            options = dict()
        options.update(kwargs)
        watcher = NavigatorWatcher(self._client, self._ignoreHTTPSErrors,
                                   options)
        responses: Dict[str, Response] = dict()
        listener = helper.addEventListener(
            self._networkManager, NetworkManager.Events.Response,
            lambda response: responses.__setitem__(response.url, response)
        )
        navigationPromise = watcher.waitForNavigation()
        referrer = self._networkManager.extraHTTPHeaders().get('referer', '')

        try:
            await self._client.send('Page.navigate',
                                    dict(url=url, referrer=referrer))
        except Exception:
            watcher.cancel()
            raise
        error = await navigationPromise
        helper.removeEventListeners([listener])
        if error:
            raise error

        if self._frameManager.isMainFrameLoadingFailed():
            raise PageError('Failed to navigate: ' + url)
        return responses.get(self.url)

    async def reload(self, options: dict = None, **kwargs: Any
                     ) -> Optional[Response]:
        """Reload this page."""
        if options is None:
            options = dict()
        options.update(kwargs)
        response = (await asyncio.gather(
            self.waitForNavigation(options),
            self._client.send('Page.reload'),
        ))[0]
        return response

    async def waitForNavigation(self, options: dict = None, **kwargs: Any
                                ) -> Optional[Response]:
        """Wait navigation completes."""
        if options is None:
            options = dict()
        options.update(kwargs)
        watcher = NavigatorWatcher(self._client, self._ignoreHTTPSErrors,
                                   options)
        responses: Dict[str, Response] = dict()
        listener = helper.addEventListener(
            self._networkManager,
            NetworkManager.Events.Response,
            lambda response: responses.__setitem__(response.url, response)
        )
        helper.removeEventListeners([listener])

        error = await watcher.waitForNavigation()
        if error:
            raise error
        return responses.get(self.url, None)

    async def goBack(self, options: dict = None, **kwargs: Any
                     ) -> Optional[Response]:
        """Go back history."""
        if options is None:
            options = dict()
        options.update(kwargs)
        return await self._go(-1, options)

    async def goForward(self, options: dict = None, **kwargs: Any
                        ) -> Optional[Response]:
        """Go forward history."""
        if options is None:
            options = dict()
        options.update(kwargs)
        return await self._go(+1, options)

    async def _go(self, delta: int, options: dict) -> Optional[Response]:
        history = await self._client.send('Page.getNavigationHistory')
        _count = history.get('currentIndex', 0) + delta
        entries = history.get('entries', [])
        if len(entries) < _count:
            return None
        entry = entries[_count]
        response = (await asyncio.gather(
            self.waitForNavigation(options),
            self._client.send('Page.navigateToHistoryEntry', {
                'entryId': entry.get('id')
            })
        ))[0]
        return response

    async def emulate(self, options: dict = None, **kwargs: Any) -> None:
        """Emulate viewport and user agent."""
        if options is None:
            options = dict()
        options.update(kwargs)
        await self.setViewport(options.get('viewport', {}))
        await self.setUserAgent(options.get('userAgent', ''))

    async def setJavaScriptEnabled(self, enabled: bool) -> None:
        """Set JavaScript enabled/disabled."""
        await self._client.send('Emulation.setScriptExecutionDisabled', {
            'value': not enabled,
        })

    async def emulateMedia(self, mediaType: str = None) -> None:
        """Emulate css media type of the page."""
        if mediaType not in ['screen', 'print', None, '']:
            raise ValueError(f'Unsupported media type: {mediaType}')
        await self._client.send('Emulation.setEmulatedMedia', {
            'media': mediaType or '',
        })

    async def setViewport(self, viewport: dict) -> None:
        """Set viewport."""
        needsReload = await self._emulationManager.emulateViewport(
            self._client, viewport,
        )
        self._viewport = viewport
        if needsReload:
            await self.reload()

    @property
    def viewport(self) -> dict:
        """Get viewport."""
        return self._viewport

    async def evaluate(self, pageFunction: str, *args: Any) -> str:
        """Execute js-function on this page and get result."""
        frame = self._frameManager.mainFrame
        if frame is None:
            raise PageError('No main frame.')
        return await frame.evaluate(pageFunction, *args)

    async def evaluateOnNewDocument(self, pageFunction: str, *args: str
                                    ) -> None:
        """Evaluate js-function on new document."""
        source = helper.evaluationString(pageFunction, *args)
        await self._client.send('Page.addScriptToEvaluateOnNewDocument', {
            'source': source,
        })

    async def screenshot(self, options: dict = None, **kwargs: Any) -> bytes:
        """Take screen shot."""
        options = options or dict()
        options.update(kwargs)
        screenshotType = None
        if 'path' in options:
            mimeType, _ = mimetypes.guess_type(options['path'])
            if mimeType == 'image/png':
                screenshotType = 'png'
            elif mimeType == 'image/jpeg':
                screenshotType = 'jpeg'
            else:
                raise PageError('Unsupported screenshot '
                                f'mime type: {mimeType}')
        if 'type' in options:
            screenshotType = options['type']
        if not screenshotType:
            screenshotType = 'png'
        return await self._screenshotTask(screenshotType, options)

    async def _screenshotTask(self, format: str, options: dict) -> bytes:  # noqa: C901,E501
        await self._client.send('Target.activateTarget', {
            'targetId': self._client.targetId,
        })
        clip = options.get('clip')
        if clip:
            clip['scale'] = 1

        if options.get('fullPage'):
            metrics = await self._client.send('Page.getLayoutMetrics')
            width = math.ceil(metrics['contentSize']['width'])
            height = math.ceil(metrics['contentSize']['height'])

            # Overwrite clip for full page at all times.
            clip = dict(x=0, y=0, width=width, height=height, scale=1)
            mobile = self._viewport.get('isMobile', False)
            deviceScaleFactor = self._viewport.get('deviceScaleFactor', 1)
            landscape = self._viewport.get('isLandscape', False)
            if landscape:
                screenOrientation = dict(angle=90, type='landscapePrimary')
            else:
                screenOrientation = dict(angle=0, type='portraitPrimary')
            await self._client.send('Emulation.setDeviceMetricsOverride', {
                'mobile': mobile,
                'width': width,
                'height': height,
                'deviceScaleFactor': deviceScaleFactor,
                'screenOrientation': screenOrientation,
            })

        if options.get('omitBackground'):
            await self._client.send(
                'Emulation.setDefaultBackgroundColorOverride',
                {'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}},
            )
        opt = {'format': format}
        if clip:
            opt['clip'] = clip
        result = await self._client.send('Page.captureScreenshot', opt)

        if options.get('omitBackground'):
            await self._client.send(
                'Emulation.setDefaultBackgroundColorOverride')

        if options.get('fullPage'):
            await self.setViewport(self._viewport)

        buffer = base64.b64decode(result.get('data', b''))
        _path = options.get('path')
        if _path:
            with open(_path, 'wb') as f:
                f.write(buffer)
        return buffer

    async def pdf(self, options: dict = None, **kwargs: Any) -> bytes:
        """Not yet implemented."""
        if options is None:
            options = dict()
        options.update(kwargs)
        scale = options.get('scale', 1)
        displayHeaderFooter = bool(options.get('displayHeaderFooter'))
        printBackground = bool(options.get('printBackground'))
        landscape = bool(options.get('landscape'))
        pageRanges = options.get('pageRanges', '')

        paperWidth = 8.5
        paperHeight = 11.0
        if 'format' in options:
            fmt = Page.PaperFormats.get(options['format'].lower())
            if not fmt:
                raise ValueError('Unknown paper format: ' + options['format'])
            paperWidth = fmt['width']
            paperHeight = fmt['height']
        else:
            paperWidth = convertPrintParameterToInches(options.get('width')) or paperWidth  # noqa: E501
            paperHeight = convertPrintParameterToInches(options.get('height')) or paperHeight  # noqa: E501

        marginOptions = options.get('margin', {})
        marginTop = convertPrintParameterToInches(marginOptions.get('top')) or 0  # noqa: E501
        marginLeft = convertPrintParameterToInches(marginOptions.get('left')) or 0  # noqa: E501
        marginBottom = convertPrintParameterToInches(marginOptions.get('bottom')) or 0  # noqa: E501
        marginRight = convertPrintParameterToInches(marginOptions.get('right')) or 0  # noqa: E501

        result = await self._client.send('Page.printToPDF', dict(
            landscape=landscape,
            displayHeaderFooter=displayHeaderFooter,
            printBackground=printBackground,
            scale=scale,
            paperWidth=paperWidth,
            paperHeight=paperHeight,
            marginTop=marginTop,
            marginBottom=marginBottom,
            marginLeft=marginLeft,
            marginRight=marginRight,
            pageRanges=pageRanges
        ))
        buffer = base64.b64decode(result.get('data', b''))
        if 'path' in options:
            with open(options['path'], 'wb') as f:
                f.write(buffer)
        return buffer

    async def plainText(self) -> str:
        """Get page content as plain text."""
        return await self.evaluate('() => document.body.innerText')

    async def title(self) -> str:
        """Get page title."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return await frame.title()

    async def close(self) -> None:
        """Close connection."""
        await self._client.dispose()

    @property
    def mouse(self) -> Mouse:
        """Get mouse object."""
        return self._mouse

    async def click(self, selector: str, options: dict = None, **kwargs: Any
                    ) -> None:
        """Click element which matches `selector`."""
        if options is None:
            options = dict()
        options.update(kwargs)
        handle = await self.J(selector)
        if not handle:
            raise PageError('No node found for selector: ' + selector)
        await handle.click(options)
        await handle.dispose()

    async def hover(self, selector: str) -> None:
        """Mouse hover the element which matches `selector`."""
        handle = await self.J(selector)
        if not handle:
            raise PageError('No node found for selector: ' + selector)
        await handle.hover()
        await handle.dispose()

    async def focus(self, selector: str) -> None:
        """Focus the element which matches `selector`."""
        handle = await self.J(selector)
        if not handle:
            raise PageError('No node found for selector: ' + selector)
        await self.evaluate('element => element.focus()', handle)
        await handle.dispose()

    async def type(self, text: str, options: dict = None, **kwargs: Any
                   ) -> None:
        """Type text on the page."""
        options = options or dict()
        options.update(kwargs)
        delay = options.get('delay', 0)
        last: asyncio.Future = asyncio.ensure_future(asyncio.sleep(0))
        for char in text:
            last = asyncio.ensure_future(
                self.press(char, {'text': char, 'delay': delay})
            )
            await asyncio.sleep(delay)
        await last

    async def press(self, key: str, options: dict = None, **kwargs: Any
                    ) -> None:
        """Press key."""
        options = options or dict()
        options.update(kwargs)
        delay = options.get('delay', 0)
        await self._keyboard.down(key, options)
        await asyncio.sleep(delay)
        await self._keyboard.up(key)

    def waitFor(self, selectorOrFunctionOrTimeout: Union[str, int, float],
                options: dict = None, *args: Any, **kwargs: Any) -> Awaitable:
        """Wait for function, timeout, or element which matches on page."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return frame.waitFor(
            selectorOrFunctionOrTimeout, options, *args, **kwargs)

    def waitForSelector(self, selector: str, options: dict = None,
                        **kwargs: Any) -> Awaitable:
        """Wait until element which matches selector appears on page."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return frame.waitForSelector(selector, options, **kwargs)

    def waitForFunction(self, pageFunction: str, options: dict = None,
                        *args: str, **kwargs: Any) -> Awaitable:
        """Wait for function."""
        frame = self.mainFrame
        if not frame:
            raise PageError('no main frame.')
        return frame.waitForFunction(pageFunction, options, *args, **kwargs)


unitToPixels = {
    'px': 1,
    'in': 96,
    'cm': 37.8,
    'mm': 3.78
}


def convertPrintParameterToInches(parameter: Union[None, int, float, str]
                                  ) -> Optional[float]:
    """Convert print parameter to inches."""
    if parameter is None:
        return None
    if isinstance(parameter, (int, float)):
        pixels = parameter
    elif isinstance(parameter, str):
        text = parameter
        unit = text[-2:].lower()
        if unit in unitToPixels:
            valueText = text[:-2]
        else:
            unit = 'px'
            valueText = text
        try:
            value = float(valueText)
        except ValueError:
            raise ValueError('Failed to parse parameter value: ' + text)
        pixels = value * unitToPixels[unit]
    else:
        raise TypeError('page.pdf() Cannot handle parameter type: ' +
                        str(type(parameter)))
    return pixels / 96


async def create_page(client: Session, ignoreHTTPSErrors: bool = False,
                      screenshotTaskQueue: list = None) -> Page:
    """Async function which make new page."""
    await client.send('Network.enable', {}),
    await client.send('Page.enable', {}),
    await client.send('Runtime.enable', {}),
    await client.send('Security.enable', {}),
    if ignoreHTTPSErrors:
        await client.send('Security.setOverrideCertificateErrors',
                          {'override': True})
    page = Page(client, ignoreHTTPSErrors, screenshotTaskQueue)
    await page.goto('about:blank')
    await page.setViewport({'width': 800, 'height': 600})
    return page


#: alias to :func:`create_page()`
craete = create_page
