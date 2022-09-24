###############################################################################
# 
#                           sendtopostman_pop.py
#
#  Highlight one or more items in the History pane and send them to Postman
# 
# by T.Fish
#
# Github:  (https://github.com/tdotfish)
# Twitter: @tdotfish
# Web: https://tdot.fish
#
# Usage: 
# 1. Load this script in ZAP as an extender type script
# 2. Change `postmanPort` and `postmanIP` as needed
# 3. Right-click it and choose "Enable Script(s)"
# 4. Optional - Double-click it and tick the "Load on Start" box
# 5. Highlight item(s) in the history pane
# 6. Right click a highlighted item and choose Send to Postman
# 7. All highlighted items will appear in Postman History
#
# If nothing appears in Postman History check that Postman is in Capture mode 
# and IP and port are set correctly.
#
# A warning will also appear in the ZAP script console if this happens.
#
# Caveat: If you are already pointing ZAP to an upstream proxy, you will need 
# to make sure Postman is configured to use that same upstream proxy.
#
###############################################################################

from org.zaproxy.zap.view.popup import PopupMenuItemHistoryReferenceContainer
from org.parosproxy.paros.network import HttpSender, HttpMessage, HttpRequestHeader
from org.parosproxy.paros.model import Model 
from java.net import ConnectException
from time import sleep
import sys

postmanPort = 5555
postmanIP = "127.0.0.1"

class PostmanPopup(PopupMenuItemHistoryReferenceContainer):
    def performAction(self, historyReference):

        connectionParam = Model.getSingleton().getOptionsParam().getConnectionParam()

        #Save existing ProxyChain settings
        oldProxyName = connectionParam.getProxyChainName()
        oldProxyPort = connectionParam.getProxyChainPort()
        oldProxyAuthEnabled = connectionParam.isUseProxyChainAuth()
        oldProxyEnabled = connectionParam.isUseProxyChain()

        connectionParam.setProxyChainName(postmanIP)
        connectionParam.setProxyChainPort(postmanPort)
        connectionParam.setUseProxyChainAuth(False)
        connectionParam.setUseProxyChain(True)
        
        #https://groups.google.com/g/zaproxy-scripts/c/k0trKMHBxQk/m/eHzIkC7rBgAJ
        sender = HttpSender(connectionParam, True, HttpSender.MANUAL_REQUEST_INITIATOR)

        msg =  HttpMessage(historyReference.getHttpMessage().cloneRequest())

        try:
            sender.sendAndReceive(msg)
        except ConnectException, err: # <- java.net.ConnectException is thrown when Postman isn't listening
            #print(sys.exc_info()[0], sys.exc_info()[1])
            print("Proxy connection was refused. Is Postman in capture mode?")
        finally:
            #Revert to prior ProxyChain settings
            connectionParam.setProxyChainName(oldProxyName)
            connectionParam.setProxyChainPort(oldProxyPort)
            connectionParam.setUseProxyChainAuth(oldProxyAuthEnabled)
            connectionParam.setUseProxyChain(oldProxyEnabled)

postmanmenuitem = PostmanPopup("Send To Postman", True)

def install(helper):
    if helper.getView():
        helper.getView().getPopupMenu().addMenu(postmanmenuitem)
    print("SendToPostman.py Enabled")
    return

def uninstall(helper):
    if helper.getView():
        helper.getView().getPopupMenu().removeMenu(postmanmenuitem)
    print("SendToPostman.py Disabled")
    return
