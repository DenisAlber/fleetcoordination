/*!
* Start Bootstrap - Bare v5.0.0 (https://startbootstrap.com/template/bare)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/

var exampleSocket = new WebSocket('ws://192.168.178.108:3000'); // evtl. anpassen..
$(document).ready(function () {

    exampleSocket.onopen = function (event) {};

    exampleSocket.onmessage = function (event) {
        try{
            JSON.parse(event.data);
        }
        catch{
            if(event.data != "connected to server ..."){
                alert(event.data);
            }
            else{
                console.log(event.data);
            }
            return;
        }
        console.log(JSON.parse(event.data));
        var dat = JSON.parse(event.data);

        if(dat.hasOwnProperty('isBlocked')){
            var svg = d3.select("svg");
            var line = svg.select(`#${dat.id}`);
            
            if(dat.isBlocked){
                line.style("stroke", "red");
            }
            else{
                line.style("stroke", "grey");
            }
        }
        else if(dat.hasOwnProperty('isTarget')){
            var svg = d3.select("svg");
            var circle = svg.select(`#${dat.id}`);
            
            if(dat.isTarget){
                circle.style("fill", "rgb(68, 201, 164)");
            }
            else{
                circle.style("fill", "rgb(49, 210, 242)");
            }
        }
       


     };

    $.get("/GetMap", function(data){
        console.log(JSON.parse(data));
        
        buildSVG(JSON.parse(data));
    });

})

function buildSVG(graph){
    // width and height for svg image
    var width = 700;
    var height = 600;

    // instantiante new <g></g>
    var svg = d3.select("#d3Class").append("svg")
            .attr("class", "text-center")
            .attr("width", width)
            .attr("height", height).call(responsivefy);

    // add all lines from graph to g
    graph.nodes.forEach(element => {
        // console.log(element.connections.length);
        var connectedNode;
        svg.selectAll("line"+element.name)
            .data(element.connections)
            .enter()
            .append("line")
            .style("stroke", function(d){
                if(d.blocked){
                    return "red";
                }
                else
                {
                    return "gray";
                }
            })
            .style("stroke-width", 10)
            .attr("x1", element.x)
            .attr("y1", element.y)
            .attr("x2", function (d) {
                return findAttribute(d).x 
            })
            .attr("y2", function (d) {
                return findAttribute(d).y
            })
            .attr("id", function(d){
                connectedNode = d.connected;
                return element.name + d.connected;
            })
            .on("click", function(d, i){
                    // send lock for street and change color
                    console.log("Send accident..");
                    var transaction = { node1: element.name, node2: i.connected};
                    exampleSocket.send(JSON.stringify(transaction));
                }
            );
            
    });

    // move overlapping lines 
    svg.selectAll("line").each(function(){  // iterate through all lines
        var firstLine= d3.select(this); // select d3 object from line

        svg.selectAll("line").each(function(){  // iterate through all lines
            var secondLine = d3.select(this);   // select d3 object from line

            // check for overlapping horizontal lines 
            if(firstLine.attr('x1') == secondLine.attr('x2')
            && firstLine.attr('x2') == secondLine.attr('x1') 
            && firstLine.attr('y1') == secondLine.attr('y2')
            && firstLine.attr('y2') == secondLine.attr('y1')
            && firstLine.attr('x1') != secondLine.attr('x1')
            )
            {
                // move first line up
                firstLine.attr('y1', parseInt(firstLine.attr('y1')) + 20);
                firstLine.attr('y2', parseInt(firstLine.attr('y2')) + 20);

                // move second line down
                secondLine.attr('y1', parseInt(secondLine.attr('y1')) - 20);
                secondLine.attr('y2', parseInt(secondLine.attr('y2')) - 20);
            }

            if(firstLine.attr('x1') == secondLine.attr('x2') 
            && firstLine.attr('x2') == secondLine.attr('x1') 
            && firstLine.attr('y1') == secondLine.attr('y2')
            && firstLine.attr('y2') == secondLine.attr('y1')
            && firstLine.attr('y1') != secondLine.attr('y1')
            )
            {
                firstLine.attr('x1', parseInt(firstLine.attr('x1')) - 20);
                firstLine.attr('x2', parseInt(firstLine.attr('x2')) - 20);

                secondLine.attr('x1', parseInt(secondLine.attr('x1')) + 20);
                secondLine.attr('x2', parseInt(secondLine.attr('x2')) + 20);
            }

        })
    })

    // add circles/nodes/crossings
    var circles = svg.selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
        .style("stroke", "gray")
        .style("fill", "rgb(49, 210, 242)")
        .attr("r", function (d, i) {
            return d.r;
        })
        .attr("cx", function (d, i) {
            return d.x;
        })
        .attr("cy", function (d, i) {
            return d.y;
        })
        .attr("id", function(d, i){
            return d.name;
        })
        .on("click", function(d, i){
            // send command to go to specific node
            console.log("Send go to..");
            var transaction = { node1: i.name, node2: ""};
            exampleSocket.send(JSON.stringify(transaction));
        });

    var nodes = graph.nodes;

    // Add text to circles
    var text = svg.selectAll("text")
        .data(graph.nodes)
        .enter()
        .append('text')
        .attr('x', nodes=>nodes.x)
        .attr('y', nodes=>nodes.y)
        .text(nodes => nodes.name)
        .style("text-anchor", "middle")
        .style('fill', 'black')
        .on("click", function(d, i){
            console.log("Send go to..");
            var transaction = { node1: i.name, node2: ""};
            exampleSocket.send(JSON.stringify(transaction));
        });

    // function to find neighbors
    function findAttribute(name) {
        // console.log(name.connected);
        for (var i = 0, len = graph.nodes.length; i < len; i++) {
            if (graph.nodes[i].name === name.connected)
                return graph.nodes[i]; // Return as soon as the object is found
        }
        return null; // The object was not found
    }

    // for responsive graph
    function responsivefy(svg) {
        // get container + svg aspect ratio
        var container = d3.select(svg.node().parentNode),
            width = parseInt(svg.style("width")),
            height = parseInt(svg.style("height")),
            aspect = width / height;

        // add viewBox and preserveAspectRatio properties,
        // and call resize so that svg resizes on inital page load
        svg.attr("viewBox", "0 0 " + width + " " + height)
            .attr("perserveAspectRatio", "xMinYMid")
            .call(resize);

        // to register multiple listeners for same event type, 
        // you need to add namespace, i.e., 'click.foo'
        // necessary if you call invoke this function for multiple svgs
        // api docs: https://github.com/mbostock/d3/wiki/Selections#on
        d3.select(window).on("resize." + container.attr("id"), resize);

        // get width of container and resize svg to fit it
        function resize() {
            var targetWidth = parseInt(container.style("width"));
            svg.attr("width", targetWidth);
            svg.attr("height", Math.round(targetWidth / aspect));
        }
    }
}