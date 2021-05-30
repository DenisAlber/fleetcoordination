/*!
* Start Bootstrap - Bare v5.0.0 (https://startbootstrap.com/template/bare)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

var graph = {
    "nodes": [
        {name: "A", x: 150, y: 100, r: 50,  "connections" : [
            { connected: "B" },
            { connected: "D" }
        ] 
        },
        {
            name: "B", x: 350, y: 100, r: 50, "connections": [
                { connected: "A" },
                { connected: "C" },
                { connected: "E" }
            ]
        },
        {
            name: "C", x: 550, y: 100, r: 50, "connections" : [
                { connected: "B" },
                { connected: "F" }
            ]
        },
        {
            name: "D", x: 150, y: 300, r: 50, "connections" : [
                { connected: "A" },
                { connected: "G" },
                { connected: "E" }
            ]
        },
        {
            name: "E", x: 350, y: 300, r: 50, "connections" : [
                { connected: "D" },
                { connected: "F" },
                { connected: "B" },
            ]
        },
        {
            name: "F", x: 550, y: 300, r: 50, "connections" : [
                { connected: "C" },
                { connected: "I" },
                { connected: "E" }
            ]
        },
        {
            name: "G", x: 150, y: 500, r: 50, "connections" : [
                { connected: "D" },
                { connected: "H" },
            ]
        },
        {
            name: "H", x: 350, y: 500, r: 50, connections: [
                { connected: "G" },
                { connected: "I" },
            ]
        },
        {
            name: "I", x: 550, y: 500, r: 50, connections : [
                { connected: "H" },
                { connected: "F" },
            ]
        }

    ] 
}


    var width = 700;
    var height = 600;
// // create svg element:
// var svg = d3.select("#d3Class")
//     .selectAll('g')
//     .data(DUMMY_DATA.nodes)
//     .append("svg")
//     .attr("width", 200)
//     .attr("height", 200);
// graph.nodes.forEach(element => {
//     console.log(element.connections);
// });

var svg = d3.select("#d3Class").append("svg")
        .attr("class", "text-center")
        .attr("width", width)
        .attr("height", height)
        .append("g");

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
                console.log("Send accident..");
                var transaction = { node1: element.name, node2: i.connected};
                $.post("/Zumi", transaction)
                    .done(function (data) {
                        console.log(data);
                    });
            }
        );
        
});

svg.selectAll("line").each(function(){
    // console.log(this);
    var firstLine= d3.select(this);

    svg.selectAll("line").each(function(){
        // console.log(this);
        var secondLine = d3.select(this);

        if(firstLine.attr('x1') == secondLine.attr('x2') 
        && firstLine.attr('x2') == secondLine.attr('x1') 
        && firstLine.attr('y1') == secondLine.attr('y2')
        && firstLine.attr('y2') == secondLine.attr('y1')
        && firstLine.attr('x1') != secondLine.attr('x1')
        )
        {
            firstLine.attr('y1', parseInt(firstLine.attr('y1')) + 20);
            firstLine.attr('y2', parseInt(firstLine.attr('y2')) + 20);
            
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
    // console.log(ok.attr('x1'));
})

// graph.nodes.forEach(element => {
//     console.log(element.connections.length);
//     var lineList;
//     svg.selectAll("line"+element.name)
//         .data(element.connections)
//         .enter()
//         .append("line")
//         .style("stroke", "gray") // <<<<< Add a color
//         .style("stroke-width", 10)
//         .attr("x1", element.x)
//         .attr("y1", element.y)
//         .attr("x2", function (d) {
//             return findAttribute(d).x 
//         })
//         .attr("y2", function (d) {
//             return findAttribute(d).y
//         })
// });
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
        console.log("Send go to..");
        var transaction = { node1: i.name, node2: "nothing"};
        $.post("/Zumi", transaction)
            .done(function (data) {
                console.log(data);
            });
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
        $.post("/Zumi", transaction)
            .done(function (data) {
                console.log(data);
            });
    });


function findAttribute(name) {
    // console.log(name.connected);
    for (var i = 0, len = graph.nodes.length; i < len; i++) {
        if (graph.nodes[i].name === name.connected)
            return graph.nodes[i]; // Return as soon as the object is found
    }
    return null; // The object was not found
}

// $("#sendAc").click(function(){
// console.log("Test");
// })


// const DUMMY_DATA = {
//     "nodes": [
//         { kreuzung: 'A', connected: 'B' },
//         { kreuzung: 'B', connected: 'C' },
//         { kreuzung: 'C', connected: 'F' },
//         { kreuzung: 'D', connected: 'A' },
//         { kreuzung: 'E', connected: 'F' },
//         { kreuzung: 'F', connected: 'G' },
//         { kreuzung: 'G', connected: 'D' }]
// };

// // create svg element:
// var svg = d3.select("#d3Class")
//     .selectAll('g')
//     .data(DUMMY_DATA.nodes)
//     .append("svg")
//     .attr("width", 200)
//     .attr("height", 200);

// // Add circles
// var test = svg.append('circle')
//     .attr('cx', 100)
//     .attr('cy', 100)
//     .attr('r', 50)
//     .attr('stroke', 'black')
//     .attr('fill', '#69a3b2');

// // Add text to circles
// var text = svg.append('text')
//     .attr('x', 100)
//     .attr('y', 100)
//     .text(node => node.kreuzung)
//     .style("text-anchor", "middle")
//     .style('fill', 'black');


$(document).ready(function () {
    // $("#sendAc").click(function() {
    // console.log("Send accident..");
    // $.ajax({
    //     crossDomain: true,
    //     dataType: 'jsonp',
    //     type: "POST",
    //     url: "http://localhost:3000/Zumi",
    //     data: {item1: 2, item2: 3}
    //   }).done(function(){
    //       console.log("done")
    //   });
    // })


    $("#sendAc").click(function () {
        console.log("Send accident..");
        var transaction = { node1: 'A', node2: 'C' };
        $.post("/Zumi", transaction)
            .done(function (data) {
                console.log(data);
            });
    })


    $("#releaseAc").click(function () {
        console.log("Send release accident");
    });
})