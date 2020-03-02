(function($) {
  $.fn.button = function(action) {
    if (action === 'loading' && this.data('loading-text')) {
      this.data('original-text', this.html()).html(this.data('loading-text')).prop('disabled', true);
    }
    if (action === 'reset' && this.data('original-text')) {
      this.html(this.data('original-text')).prop('disabled', false);
    }
  };
}(jQuery));

const state = {
  languages: {
    "Python3": "python",
    "JavaScript": "js"
  },
  currLang: "python",
  isLoading: false
}

$(document).ready(() => {
  axios.get(`${window.location.href}/prompt`)
    .then(res => {
      document.getElementById("prompt").innerHTML = marked(res.data)
    })
    .catch(err => {
      $("#prompt").innerHTML = `<p>Failed to load prompt</p>`
    })
  axios.get(`${window.location.href}/attempt`)
    .then(res => {
      document.getElementById("prism_code").innerHTML = res.data
    })
    .catch(err => {
      $("#prism_code").innerText = `Failed to load template file`
    }).finally(res => {
      $("#prism_code")[0].PrismLive.update()
    })
})


function toggleSpinner(id) {
  state.isLoading = !state.isLoading
  let button = $(`#${id}`)
  if (state.isLoading) {
    button.button("loading")
  } else {
    button.button("reset")
  }
}

function createPayload(code, harnessMethod) {
  const body = JSON.stringify({
    code: code,
    language: state.currLang,
    method: harnessMethod
  })
  return body
}

function handleResponse(res, method) {
  if (res.status > 399) {
    throw new Error("Error sending response")
  }
  let { data, status } = res
  console.log(data)
  let { output, score } = data


  $("#output__container")[0].innerText = output.join('\n')
  if (score && method == 'submit') {
    $("#current__score")[0].innerText = score

    data.data.forEach(element => {
      let id = `testcase-${element.id.replace(/\./g, '-')}`
      let score = element.score
      let maxscore = element.maxscore
      let elem = $($($(document.getElementById(id))[0]).find(".col-2")[0])[0]
      elem.innerText = `${element.score}/${element.maxscore}`

      elem  = $($(document.getElementById(id))[0])
      elem.removeClass('list-group-item-dark')
      elem.removeClass('list-group-item-success')
      if (score == maxscore) {
        elem.addClass('list-group-item-success')
      } else {
        elem.addClass('list-group-item-dark')
      }
    });

  }
}

function handleError(err) {
  $("#output__container")[0].innerText = err
}

function submit(harnessMethod, btn) {
  const code = $("textarea#prism_code")[0].value
  const payload = createPayload(code, harnessMethod)
  const id = btn.id
  toggleSpinner(id)
  axios.post(window.location.pathname, payload,
    {headers: {'Content-Type': 'application/json'}}
  )
    .then(json => handleResponse(json, harnessMethod))
    .catch(err => handleError(err))
    .finally(() => toggleSpinner(id))
}
