console.log "hello world"

setInterval ->
  $.get '/static/version.txt',(d)->
    console.log d
    if localStorage.getItem('lastReload') isnt d
      location.reload()
      localStorage.setItem 'lastReload', d
,1000



# THIS CAN BE USED AFTER WE FIND OUT HOW TO RUN A WEBSOCKET SERVER WITH PYTHON
# ws = new ReconnectingWebSocket('ws://0.0.0.0:9091/', null, {reconnectInterval: 100})
#
#
# ws.onmessage = (event) ->
#   console.log message
#   # try msg = JSON.parse event.data
#   # catch e then msg = {}
#   # if msg.command? then @handleIncomingCommand msg
#
# ws.onclose = ->
#   console.log 'Socket closed'
#
# ws.onopen = ->
#     console.log 'Socket connected'
#     if Date.now() - localStorage.getItem('lastReload') > 2000
#       location.reload();
#       localStorage.setItem 'lastReload', Date.now()
