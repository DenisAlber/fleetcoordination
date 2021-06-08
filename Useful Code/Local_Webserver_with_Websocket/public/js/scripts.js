/*!
* Start Bootstrap - Bare v5.0.0 (https://startbootstrap.com/template/bare)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/

var exampleSocket = new WebSocket('ws://localhost:3000');
$(document).ready(function () {


    var exampleSocket = new WebSocket('ws://localhost:3000');
    
    exampleSocket.onopen = function (event) {
        // exampleSocket.send("Here's some text that the server is urgently awaiting!");
      };

    exampleSocket.onmessage = function (event) {
       console.log(event.data);
       var ok = event.data;
       var dat = JSON.parse(ok);
       console.log(dat);

        var svg = d3.select("svg");
        var line = svg.select(`#${dat.id}`);
        
        if(dat.isBlocked){
            line.style("stroke", "red");
        }
        else{
            line.style("stroke", "grey");
        }

     };

    $.get("/GetMap", function(data){
        console.log(JSON.parse(data));
        
        buildSVG(JSON.parse(data));
    });

    // getTraffic();
})

function getTraffic(){
    $.get('/traffic', function(data){
        console.log(data);

        var svg = d3.select("svg");
        var line = svg.select(`#${data.id}`);
        
        if(data.isBlocked){
            line.style("stroke", "red");
        }
        else{
            line.style("stroke", "grey");
        }

        getTraffic();
    });
}

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
            .style("stroke", "gray") // <<<<< Add a color
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
                    // if(d3.select(this).style("stroke") === "red"){
                    //     d3.select(this).style("stroke", "gray");
                    // }
                    // else{
                    //     d3.select(this).style("stroke", "red");
                    // }
                    // $.post("/traffic", transaction)
                    //     .done(function (data) {
                    //         console.log(data);
                    //     });
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
            var transaction = { node1: i.name, node2: "nothing"};
            // if(d3.select(this).style("fill") === "green"){
            //     d3.select(this).style("fill", "rgb(49, 210, 242)");
            // }
            // else{
            //     d3.select(this).style("fill", "green");
            // // }
            // $.post("/traffic", transaction)
            //     .done(function (data) {
            //         console.log(data);
            //     });
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
            var transaction = { node1: i.name, node2: "nothing"};
            // $.post("/traffic", transaction)
            //     .done(function (data) {
            //         console.log(data);
            //     });
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