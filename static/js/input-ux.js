$(document).ready(function() {
  var inputs = $('form.guess input')
  var button = $('form.guess button')
  var timer = null
  var beingPressed = false

  inputs[0].focus()
  $(window).keydown(function(event) {
    if (event.metaKey || event.ctrlKey) {
      return
    }
    if (event.target.tagName == 'BUTTON' && event.key == 'Backspace') {
      inputs.last().focus()
    } else if (
      event.target.tagName != 'INPUT' &&
      event.target.tagName != 'BUTTON'
    ) {
      inputs.first().focus()
    }
  })

  inputs.keydown(function(event) {
    if (event.metaKey || event.ctrlKey) {
      return
    }
    if (timer) {
      clearTimeout(timer)
      timer = null
    }

    var input = $(this)
    if (inputSet.indexOf(event.key) > -1) {
      if (input.val().length) {
        input.val('')
      } else {
        event.preventDefault()
      }
      input.val(event.key)
      if (!!input.parent().next().find('input').length) {
        input.parent().next().find('input').focus()
      } else {
        button.focus()
      }
    } else if (event.key.length == 1) {
      event.preventDefault()
      input.val(event.key)
      timer = setTimeout(function() {
        input.val('')
      }, 100)
    } else if (event.key == 'Backspace' && input.val().length == 0) {
      if (!!input.parent().prev().find('input').length) {
        event.preventDefault()
        input.parent().prev().find('input').focus()
      }
    } else if (event.key == 'Backspace' && input.val().length == 0) {
      if (!!input.parent().prev().find('input').length) {
        event.preventDefault()
        input.parent().prev().find('input').focus()
      }
    }
  })

  inputs.keyup(function(event) {
    if (event.metaKey || event.ctrlKey) {
      return
    }
    event.preventDefault()
  })

  button.focus(function() {
    button.removeClass('primary')
    button.addClass('orange')
  })
  button.blur(function() {
    button.removeClass('orange')
    button.addClass('primary')
  })
})
