function initializeGraph(networkgraph_url) {

  // The main graph container
  var svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  // Gets the JSON representation of a network graph
  var request = new XMLHttpRequest();
  request.open('GET', networkgraph_url, false);
  request.send(null);
  var snapshot = JSON.parse(request.responseText);

  var nodes_data = snapshot['nodes']
  var links_data = snapshot['links']
  var simulation = d3.forceSimulation().nodes(nodes_data);
  var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; }).strength(0);
  var charge_force = d3.forceManyBody().strength(-5);
  var center_force = d3.forceCenter(width / 2, height / 2);
  simulation
      .force("charge_force", charge_force)
      .force("center_force", center_force)
      .force("links",link_force);

  //Add tick action.
  simulation.on("tick", tickActions );

  // Encompassing group for zoom capabilities.
  var g = svg.append("g")
             .attr("class", "everything");
  var zoom_handler = d3.zoom().on("zoom", zoom_actions);
  zoom_handler(svg);
  function zoom_actions(){
    g.attr("transform", d3.event.transform)
  }

  // Link drawing
  var link = g.append("g")
              .attr("class", "links")
              .selectAll("line")
              .data(links_data)
              .enter().append("line")
              .attr("stroke-width", 6)
              .style("stroke", linkColor);

  // Node drawing
  var node = g.append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(nodes_data)
          .enter()
          .append("svg:image")
          .attr("id", function(d){ return d.id; })
          .attr("name", function(d){ return d.name; })
          .attr("href", function(d) {
            var prefix = d.id.split('-')[0];
            var href = "../static/img/aws.png";
            switch(prefix) {
              case 'vpc':
                href = "../static/img/vpc.png";
                break;
              case 'subnet':
                href = "../static/img/subnet.png";
                break;
              case 'i':
                href = "../static/img/instance.png";
                break;
              case 'igw':
                href = "../static/img/igw.png";
                break;
            }
            return href;
          })
          .attr("x", function(d) {
            var prefix = d.id.split('-')[0];
            var x = d.x - 30;
            switch(prefix) {
              case 'vpc':
                x = d.x - 30;
                break;
              case 'subnet':
                x = d.x - 20;
                break;
              case 'i':
                x = d.x - 12;
                break;
            }
            return x;
          })
          .attr("y", function(d) {
            var prefix = d.id.split('-')[0];
            var y = d.y - 30;
            switch(prefix) {
              case 'vpc':
                y = d.y - 30;
                break;
              case 'subnet':
                y = d.y - 20;
                break;
              case 'i':
                y = d.y - 12;
                break;
            }
            return y;
          })
          .attr("width", function(d) {
            var prefix = d.id.split('-')[0];
            var width = "45px";
            switch(prefix) {
              case 'vpc':
                width = "60px";
                break;
              case 'subnet':
                width = "40px";
                break;
              case 'i':
                width = "24px";
                break;
              case 'igw':
                width = "40px";
                break;
            }
            return width;
          })
          .attr("height", function(d) {
            var prefix = d.id.split('-')[0];
            var height = "45px";
            switch(prefix) {
              case 'vpc':
                height = "60px";
                break;
              case 'subnet':
                height = "40px";
                break;
              case 'i':
                height = "24px";
                break;
              case 'igw':
                height = "50px";
                break;
            }
            return height;
          })

  // Node Label drawing
  var nodelabel = g.append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(nodes_data)
          .enter()
          .append("text")
          .attr("x",function(d){return d.x;})
          .attr("y",function(d){return d.y;})
          .attr("class","tooltip")
          .attr("stroke","black")
          .text(function(d){
            var name = d.name;
            if (name.length > 15){
              name = name.substring(0,15) + "...";
            }
            return name})

  // Add drag and drop functionality to the nodes.
  var drag_handler = d3.drag()
      .on("start", drag_start)
      .on("drag", drag_drag)
      .on("end", drag_end);
  drag_handler(node)

  //drag handler
  //d is the node
  function drag_start(d) {
   if (!d3.event.active) simulation.alphaTarget(0.1).restart();
      d.fx = d.x;
      d.fy = d.y;
    if(d['id'].startsWith('subnet')) {
      for(var i in nodes_data) {
        if(nodes_data[i]['properties']['subnet'] == d['id']) {
          var xdif = nodes_data[i].x - d.x;
          var ydif = nodes_data[i].y - d.y;
          nodes_data[i].fx = nodes_data[i].x;
          nodes_data[i].fy = nodes_data[i].y;
        }
      }
    }
  }

  function drag_drag(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
    if(d['id'].startsWith('subnet')) {
      for(var i in nodes_data) {
        if(nodes_data[i]['properties']['subnet'] == d['id']) {
          var xdif = nodes_data[i].x - d.x;
          var ydif = nodes_data[i].y - d.y;
          nodes_data[i].fx = d3.event.x + xdif;
          nodes_data[i].fy = d3.event.y + ydif;
          // tickActions();
        }
      }
    }
  }

  function drag_end(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
    if(d['id'].startsWith('subnet')) {
      for(var i in nodes_data) {
        if(nodes_data[i]['properties']['subnet'] == d['id']) {
          nodes_data[i].fx = null;
          nodes_data[i].fy = null;
          // tickActions();
        }
      }
    }
  }

  // Add selection functionality to nodes and links
  node.on("click", clickNode)
  link.on("click", clickLink)

  // Keeps a reference of last node selected so that it can be unselected later
  var lastselected;
  var lasthref;
  // Function to highlight a node when its clicked
  function clickNode(d) {
    var overlayInner = d3.select("#info");
    d3.select(lastselected).attr("href", lasthref);
    d3.select(lastselected).attr("style", null);
    hideShowing();
    if(this == lastselected) {
      lastselected = 0;
      overlayInner.html("<p>Nothing Selected</p>");
    }
    else {
      lastselected = this;
      lasthref = d3.select(this).attr("href");
      d3.select(this).attr("href",lasthref.replace("-selected","").replace(".png","-selected.png"));
      d3.select(this).attr("style","filter: drop-shadow(0px 0px 20px blue)");
      var html = "<p class='lead'>" + d.name + "</p>";
      html += "<p><b>ID</b>: "+d.id+"</p>";
      html += "<p><b>AWS Account</b>: "+d.account+"</p>";
      if(d.label) {html += "<p><b>label</b>: " + d.label + "</p>";}
      if(d.properties) {
        var infos = showDetailInfo(d);
        html += infos;
      }
      if(d.linkCount) { html += "<p><b>links</b>: " + d.linkCount + "</p>"; }
      html+="<hr />"
      overlayInner.html(html);
      showSelected();
    }

  }

  // function to show detail info
  function showDetailInfo(d){
    var all_info = "";
    for(var key in d.properties) {
       switch(key){
          case "color":
             break;
          case "type":
             break;
          case "sg":
             var sg = d.properties['sg'];
             var sg_details = sg_info(sg);
             $('#sginfo').html(sg_details);
             all_info += "<p><b>Security Groups: </b><a href='#' data-toggle='modal' data-target='#sgmodal'><i class=\"fa fa-external-link\"></i></a><p>";
             break;
          case "eni":
              var eni = d.properties['eni'];
              var eni_details = eni_info(eni)
              $('#eniinfo').html(eni_details);
              all_info += "<p><b>Elastic Network Interface: </b><a href='#' data-toggle='modal' data-target='#enimodal'> <i class=\"fa fa-external-link\"></i> </a></p>";
              break;
            case "tags":
              var tags = d.properties['tags'];
              tags_info = "<p class='lead'> Tags </p>";
              for (var k in tags){
                if (k!="id"){
                  var tabs = tag_info(k, tags[k]);
                  tags_info += tabs;
                }
              }
              $('#tagsinfo').html(tags_info);
              all_info += "<p><b>Tags: </b><a href='#' data-toggle='modal' data-target='#tagsmodal'><i class=\"fa fa-external-link\"></i></a></p>"
              break;
          default:
            var k = key.replace(/\b\w/g, function(l){ return l.toUpperCase() })
            all_info += "<p><b>"+k+"</b>: " + d.properties[key] + "</p>";
            break;
         }//end_switch
       }//end_for
       return all_info;
    } //endfunction

    // create sg infos
    function sg_info(data){
      var info = "";
      var tab = "<div class='col-sm-offset-2'><table class='table table-striped table-hover' style=\"width:100%\">";
      if (isEmpty(data)){
        tab += "<td><em>No data</em></div></td></table></div>";
        return tab;
      }
      Object.keys(data).forEach(function(sg) {
        info += "<p class='lead'> Security Groups ID: " + sg + "</p>"
        Object.keys(data[sg]).forEach(function(k){
         switch(k) {
            case "id":
             break;
           case "egress":
             var egress = data[sg]['egress'];
             var e_rules = ruleTable(k, egress);
             info += e_rules;
             break;
           case "ingress":
             var ingress = data[sg]['ingress'];
             var i_rules = ruleTable(k, ingress);
             info += i_rules;
             break;
           default:
             info += "<p align=\"left\"><b>"+k.replace(/_/g, " ")+"</b>: " + data[sg][k] + "</p>";
             break;
         } //end rules
         info += "<hr/>"
       });//end_for
     }); //end foreach
       return info;
    }

    function eni_info(data){
      var info = "",
          tag = "";
      Object.keys(data).forEach(function(eni) {
        switch(eni){
          case "id":
              tag += "<p class='lead'>Elastic Network Interface ID: " + data[eni] + "</p><hr/>";
              break;
          default:
              var k = data[eni];
              info += "<p align=\"center\"><b>"+ eni +"</b>: "+k.replace(/_/g, " ")+"</p>";
              info += "<hr/>";
              break;
      }
     }); //end foreach
       return tag+info;
    }

    // create a table of properties
    function ruleTable(rule, data){
      var tab = "<p><b>" + rule + " rules</b></p>";
      tab += "<div class='col-sm-offset-2'><table class='table table-striped table-hover' style=\"width:100%\">";
      if (isEmpty(data)){
        tab += "<td><em>No rules</em></div></td></table></div>";
        return tab;
      }
      var k = "<div class='col-sm-offset-2'><tr>";
      var v = "";
      for(var key in data){
        k += "<th>"+key.replace(/_/g, " ")+"</th>";
        v += "<td>"+data[key]+"</td>";
      }
      k += "</tr>";
      v += "</td>";
      tab += k + "<tr>" + v + "</tr>";
      tab += "</table></div>";
      return tab;
    }

    // get detail info
    function tag_info(rule, data){
      var tab = "";
      tab += "<div class='col-sm-offset-2'><table class='table table-striped table-hover' style=\"width:100%\">";
      if (isEmpty(data)){
        tab += "<td><em>No data</em></div></td></table></div>";
        return tab;
      }
      var k = "<div class='col-sm-offset-2'><tr><th>"+rule+"</th></tr>";
      var v = "<td>"+data+"</td></td>";
      tab += k + "<tr>" + v + "</tr>";
      tab += "</table></div>";
      return tab;
    }

    function isEmpty(ob){
       for(var i in ob){ return false;}
      return true;
    }

  // Function to display link information when a link is clicked
  function clickLink(l) {
    d3.select(lastselected).attr("stroke", null);
    d3.select(lastselected).attr("style", null);
    var overlayInner = d3.select("#info");
    html = "<p class='bigger'><b>source</b>: " + l.source.name + "</p>";
    html += "<p class='bigger'><b>target</b>: " + l.target.name + "</p>";
    if(l.properties) {
        for(var key in l.properties) {
            if(!l.properties.hasOwnProperty(key)) { continue; }
            html += "<p class='bigger'><b>"+ key.replace(/_/g, " ") +"</b>: " + l.properties[key] + "</p>";
        }
    }
    overlayInner.html(html);
  }

  // Start simulation run for 500ms.
  var collapseTime = 1000 + 10*nodes_data.length;
  var expandTime = Math.max(1000 - 10*nodes_data.length, 50);
  var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; }).strength(.3);
  simulation.force('link_force', link_force);
  simulation.alphaTarget(5).restart();
  setTimeout(function() {
    var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; }).strength(0);
    simulation.force('link_force', link_force);
    setTimeout(function() {
      simulation.alphaTarget(0);
    }, expandTime);
  }, collapseTime);


  // Keyboard Events for ESC and F1 functions (expand, collapse)
  d3.select("body")
      .on("keydown", function() {
        if(d3.event.key == "Escape") {
          // charge_force = d3.forceManyBody().strength(-5);
          // simulation.force('charge_force', charge_force);
          var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; }).strength(0);
          simulation.force('link_force', link_force);

          if (!d3.event.active) simulation.alphaTarget(10).restart();
        }
        else if(d3.event.key == "F1") {
          // charge_force = d3.forceManyBody().strength(5);
          // simulation.force('charge_force', charge_force);
          var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; }).strength(0.1);
          simulation.force('link_force', link_force);
          if (!d3.event.active) simulation.alphaTarget(1).restart();
        }
      });
  d3.select("body")
      .on("keyup", function() {
        if(d3.event.key == "Escape") {
          if (!d3.event.active) simulation.alphaTarget(0);
        } else if(d3.event.key == "F1") {
          if (!d3.event.active) simulation.alphaTarget(0);
        }
      });

  //Function to choose node colors
  function circleColor(d){
    switch (d.properties.color){
      case "vpc": return "#3182bd";
      case "subnet": return "#ff8000";
      case "instance": return "#ccccff";
      default: return "#B39EB5";
    }
  }

  // Function to choose node size
  function circleSize(d) {
    switch (d.properties.color){
      case "vpc": return 25;
      case "subnet": return 20;
      case "instance": return 15;
      default: return 20;
    }
  }

  //Function to choose link color
  function linkColor(d){
    switch (d.properties.type){
      case "vpc_link": return "#DEA5A4";
      case "subnet_link": return "#669999";
      case "igw_link": return "#667799";
      case "account_link": return "#FF0000";
      default: return "#FF7F50";
    }
  }

  // This function describes what happens to the graph at each 'tick' of the simulation
  function tickActions() {
    //update node positions
    node
        .attr("x", function(d) {
            var prefix = d.id.split('-')[0];
            var x = d.x - 12;
            switch(prefix) {
              case 'subnet':
                x = d.x - 20;
                break;
              case 'i':
                x = d.x - 12;
                break;
              case 'vpc':
              case 'igw':
              case 'account':
                x = d.x - 30;
                break;
            }
            return x;
          })
        .attr("y", function(d) {
            var prefix = d.id.split('-')[0];
            var y = d.y - 12;
            switch(prefix) {
              case 'subnet':
                y = d.y - 20;
                break;
              case 'i':
                y = d.y - 12;
                break;
              case 'vpc':
              case 'igw':
              case 'account':
                y = d.y - 30;
                break;
            }
            return y;
          });

    //update label positions
    nodelabel
        .attr("x", function(d) { return d.x + 20; })
        .attr("y", function(d) { return d.y - 30; });

    //update link positions
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });


    //update pulse positions
    for(var i in current_pulses) {
      var pulses = $('.' + current_pulses[i]);
      var pulse_el = document.getElementById(current_pulses[i]);
      var xOrigin = parseInt(pulse_el.getAttribute("x")) + parseInt(pulse_el.getAttribute("width"))/2;
      var yOrigin = parseInt(pulse_el.getAttribute("y")) + parseInt(pulse_el.getAttribute("height"))/2;
      pulses.each(function() {
        $(this).attr("cx", xOrigin);
        $(this).attr("cy", yOrigin);
        $(this).css("transform-origin", xOrigin + "px " + yOrigin + "px");
      });
    }
  }
}
