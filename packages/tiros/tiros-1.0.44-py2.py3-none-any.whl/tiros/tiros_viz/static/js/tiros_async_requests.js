// The set of currently highlighted on the graph.
// Should be the union of all nodes in the last executed set tiros queries.
var current_pulses = [];

$('#inlinequerysubmit').each(function(index) {
  $(this.parentElement).on('submit', function(e) {
    e.preventDefault();
    var data = $(this).serialize();
    $('#inlinequerymodal').modal('hide');
    $("#loadingmodal").modal();
    $.ajax({
      type: 'post',
      url: '/inline_query',
      data: data,
      success: function(d) {
        var response = d;
        var colors = response['colors'];
        var messages = response['messages'];
        loadTirosResults(response['results'], colors, messages);
      },
      error: function (xhr, ajaxOptions, thrownError) {
       loadError(xhr.status, thrownError)
      }
    });
  });
});


$('.runquery').each(function(index) {
  $(this.parentElement).on('submit', function(e) {
    /* Serializes the inputs of the form. Need to do this because the forms
       are dynamic, and the inputs aren't known. */
    var data = $(this).serialize();
    e.preventDefault();

    /* Pops up a temporary "loading" modal, since Tiros queries can often
       take a long time. */
    $("#loadingmodal").modal();

    /* Expected result must have content-type 'application/json' or else you
       must JSON.parse() the response in the success function.*/
    $.ajax({
      type: 'post',
      url: '/policy_query',
      data: data,
      success: function(d) {
        var response = d;
        var colors = response['colors'];
        var messages = response['messages'];
        loadTirosResults(response['results'], colors, messages);
      },
      error: function (xhr, ajaxOptions, thrownError) {
       loadError(xhr.status, thrownError)
      }
    })
  })
});

/*Handle boolean response*/
function boolResponse(resp){
  var out = "";
  switch (resp) {
    case true:
       out += '<p align="center"> <i class="fa fa-check-circle fa-4x" style="color:green" aria-hidden="true"></i></p>';
       break
    case false:
      out += '<p align="center"> <i class="fa fa-times-circle-o fa-4x" style="color:red" aria-hidden="true"></i></p>';
      break
    default:
      out += "<p><b>Result: " + resp + "</b></p>";
      break
    }
  return out;
}

/* Function to load error messages*/
function loadError(code, msg){
  html = '<p class="lead" style="margin-bottom:0px;">Tiros Result</p>';
  html += '<div class="alert alert-danger" role="alert">';
  html += '<strong>Error code: '+code+ '</strong><br />' + msg;
  html += '</div>'
  console.log(msg);
  //Display the results in the modal.
  $('#tirosresult2').html(html);
  //Hide the loading modal.
  $("#loadingmodal").modal('hide');
  //Show the results modal.
  $("#resultsmodal").modal();
  hideShowing();
  showResults();
}

/* This function takes the tiros results and shows them to the user, as
   well as highlighting them on the network graph.
   results = list of result sets from tiros.
   colors = list of CSS colors to display results in.
   messages = list of strings describing each result set. */
function loadTirosResults(results, colors, messages) {
  // Removes all old result highlighting from the network graph.
  resetAffected();
  // list of nodes to be highlighted
  var h_nodes = [];
  // Generate the HTML to display the results to the user.
  var html = '<p class="lead" style="margin-bottom:0px;">Tiros Result</p>';
  for(var i = 0; i < results.length; i++) {
    html +='<p><b>Q' + (parseInt(i)+1) + ':</b><em> ' + messages[i] + '</em></p>';
    html +='<button style="margin-bottom:20px;" class="btn btn-sm btn-warning" data-toggle="modal" data-target="#result' + i + '">Show Results</button><br />';
    html +='<div class="modal" id="result' + i + '"><div class="modal-dialog"><div class="modal-content">';
    html +='<div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">Result Set #' + (parseInt(i)+1) + '</h4></div>'
    html +='<div class="modal-body">';

    if(typeof results[i] === 'string'
      || typeof results[i] === 'boolean'
      || typeof results[i] === 'number') {
        var b_result = boolResponse(results[i]);
        html += b_result;
    } else {
      html += listResources(results[i], colors[i])
    }
    html +='</div></div></div></div>'
  }
  
  //Display the results on the sidebar.
  $('#tirosresult').html(html);
  //Display the results in the modal.
  // $('#tirosresult2').html(html);
  //Hide the loading modal.
  $("#loadingmodal").modal('hide');
  //Show the results modal.
  //$("#resultsmodal").modal();
  hideShowing();
  showResults();
}

// function to list all the resources from query results
function listResources(results, color){
  var html = "";
  var h_nodes = [];
  if(results.length > 0) {
    html += '<table class="table table-striped table-hover"><thead><tr><th>#</th>';
    for(var k in results[0]) {
      if(k != "h_color") {
        html += '<th>' + k + '</th>';
      }
    }
    html += '</tr></thead><tbody>'
    for(var j in results) {
      html += "<tr><td>" + (parseInt(j)+1) + "</td>";
      for(var k in results[j]) {
        switch (k){
          case "h_color":
            h_nodes = h_nodes.concat(results[j][k]);
            break;
          default:
            html += '<td>' + results[j][k] + '</td>';
            break;
        }
      }
      html += "</tr>"
    }
    html += '</tbody></table>'
  }else {
    html += "<p><b>No results</b></p>";
  }
  html += "<p><em>Any nodes listed are marked with a <b>"
  + color + "</b> pulse on the network graph.</em><hr />";
  setAffected(h_nodes, color);
  return html;
}

// Remove all highlights on the network graph
function resetAffected() {
  for (var n in current_pulses) {
    $('.' + current_pulses[n]).remove();
  }
}

// Set highlights on the network graph
function setAffected(tiros_response, color) {
  var solutions = tiros_response;
  var affected_nodes = solutions;
  current_pulses = current_pulses.concat(affected_nodes);
  for (var n in affected_nodes) {
    var anode = $('#' + affected_nodes[n]);
    if(anode.length > 0) {

      var anode = anode[0];
      var xOrigin = parseInt(anode.getAttribute("x")) + parseInt(anode.getAttribute("width"))/2;
      var yOrigin = parseInt(anode.getAttribute("y")) + parseInt(anode.getAttribute("height"))/2;


      var firstCircle = document.createElementNS("http://www.w3.org/2000/svg","circle");
      firstCircle.setAttribute("class", "first-circle " + anode.getAttribute("id"));
      firstCircle.setAttribute("cx", xOrigin);
      firstCircle.setAttribute("cy", yOrigin);
      firstCircle.setAttribute("r", 20);
      firstCircle.setAttribute("fill", color);
      firstCircle.setAttribute("style", "transform-origin:" + xOrigin + "px " + yOrigin + "px;");

      var secondCircle = document.createElementNS("http://www.w3.org/2000/svg","circle");
      secondCircle.setAttribute("class", "second-circle " + anode.getAttribute("id"));
      secondCircle.setAttribute("cx", xOrigin);
      secondCircle.setAttribute("cy", yOrigin);
      secondCircle.setAttribute("r", 20);
      secondCircle.setAttribute("fill", color);
      secondCircle.setAttribute("style", "transform-origin:" + xOrigin + "px " + yOrigin + "px;");

      var thirdCircle = document.createElementNS("http://www.w3.org/2000/svg","circle");
      thirdCircle.setAttribute("class", "third-circle " + anode.getAttribute("id"));
      thirdCircle.setAttribute("cx", xOrigin);
      thirdCircle.setAttribute("cy", yOrigin);
      thirdCircle.setAttribute("r", 20);
      thirdCircle.setAttribute("fill", color);
      thirdCircle.setAttribute("style", "transform-origin:" + xOrigin + "px " + yOrigin + "px;");

      anode.parentElement.insertBefore(firstCircle,anode.parentElement.firstChild);
      anode.parentElement.insertBefore(secondCircle,anode.parentElement.firstChild);
      anode.parentElement.insertBefore(thirdCircle,anode.parentElement.firstChild);
    }
  }
}
