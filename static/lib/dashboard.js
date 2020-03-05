function getRegisteredClasses() {
  $("#registered-classes")[0].innerText = ""
  axios.get("/class/registered")
    .then(res => res.data)
    .then(data => {
      data.forEach(elem => {
        axios.get(`/class/${elem.class}`)
          .then(res => res.data)
          .then(assignments => {
            let runningMaxScore = 0
            let runningCurrScore = 0
            let assnString = ""
            console.log(assignments)
            assignments.forEach(assignment => {
              if (!assignment.currScore) {
                assignment.currScore = 0
              }
              if (!assignment.maxScore) {
                assignment.maxScore = 25
              }
              runningMaxScore += assignment.maxScore
              runningCurrScore += assignment.currScore
              assnString += `
                <a class="dropdown-item" href="/class/${elem.class}/${assignment.assignment}">
                  ${assignment.name} - ${assignment.currScore}/${assignment.maxScore}
                </a>
              `
            })
            let score = ""
            let scorePercent = runningCurrScore / runningMaxScore
            if (scorePercent >= .8) {
              score = "success"
            } else if (scorePercent >= .7) {
              score = "warning"
            } else {
              score = "danger"
            }

            $("#registered-classes").append(
              `<li class="list-group-item">
                <div class="dropdown row">
                  <h3 class="pl-3 pr-3 col-10">${elem.name}</h3>
                  <button class="col-sm-12 col-md-1 btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton-${elem.class}" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  </button>
                  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton-${elem.class}">${assnString}</div>
                  <div class="col-sm-12 col-md-1 btn btn-${score}">${runningCurrScore} / ${runningMaxScore}</div>
                </div>
              </li>`)
              })
          .catch(err => { console.error(err) })
      })
    })
    .catch(err => console.error(err))
}


function getAvailableClasses() {
  $("#available-classes")[0].innerText = ""
  axios.get("/class")
    .then(res => res.data)
    .then(data => {
      if (data.length == 0) {
        $("#available-classes").append(
          `<li class="list-group-item">
          No classes available! Register for some.
          </li>`
        )
        return
      }
      data.forEach(elem => {
        $("#available-classes").append(
          `<li class="list-group-item">
            <form class="align-middle" onsubmit="submitRegisterForm('/class/${elem.class}/register')">
              <span class="align-middle">${elem.name}</span><button class="float-right btn btn-success" action="submit">&plus;</button>
            </form>
          </li>`
        )

      })
    })
  .catch(err => console.error(err))
}

function submitRegisterForm(path) {
  console.log(path)
  axios.post(path)
    .then(res => res.data)
    .then(data => {
      console.log(data)
    })
    .catch(err => {
      console.error(err)
    })
  getAvailableClasses()
  getRegisteredClasses()

  return false;
}

$(document).ready(() => {
  getAvailableClasses()
  getRegisteredClasses()
})
