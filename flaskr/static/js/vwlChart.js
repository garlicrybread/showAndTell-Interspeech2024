import data from '../data/vwls.json' with { type: 'json'};
import dataSpa from '../data/spa-tardo_vwls.json' with { type: 'json'};
// hard coded-values for frequencies for sake of practice
// const dat = [
//     {vwl:{f1:200,f2:2500}}, // top right
//     // {vwl:[{f1:300,f2:25000},{f1:200,f2:500}]}, // top left
//     {vwl:{f1:850,f2:1750}}, // bottom left
//     // {vwl:{f1:900,f2:2500}}, // bottom left out of range
//     // {vwl:{f1:500,f2:2500}},
//     // {vwl:{f1:300,f2:2500}},
//     // {vwl:{f1:850,f2:500}}, // bottom right
//     // {vwl: [
//     //         {f1:300,f2:2300}, // [i]
//     //         {f1:400,f2:1700},
//     //         {f1:900,f2:2500},
//     //         {f1:550,f2:1800} // [ɛ]
//     //     ]
//     // },
//     {vwl: [ // from cry-tardo
//             {f1:843,f2:1495},
//             {f1:825,f2:1513},
//             {f1:810,f2:1541},
//             {f1:790,f2:1569},
//             {f1:778,f2:1590},
//             {f1:765,f2:1635},
//             {f1:757,f2:1677}
//         ]},
//     {vwl: [
//             {f1:478,f2:1968}
//         ]},
//     {vwl: [ // cry-tia
//             {f1:391,f2:2757},
//             {f1:393,f2:2814},
//             {f1:401,f2:2846},
//             {f1:412,f2:2872},
//             {f1:422,f2:2859},
//             {f1:423,f2:2807},
//             {f1:822,f2:1787}
//         ]}
// ];
// console.log(dat[2]['vwl'][0].f1)
// console.log(data[2]['vwl'][0].f1)

"use strict";
window.addEventListener("load", drawVowelChart);
window.addEventListener("load", drawVowels);
async function drawVowelChart(){
    const svg = d3.select("svg");
    const vwlChrtProperties = await svgGetPadding(svg);
    const paddingVwlChrt = vwlChrtProperties.padding;
    const svgWidth = vwlChrtProperties.width;
    const svgHeight = vwlChrtProperties.height;

   // define x boundaries of vowel chart
    const xPadding = paddingVwlChrt.x;
    const xWidth = svgWidth - 2*xPadding;
    const xfront = xPadding;
    const xnearFront = 0.125*xWidth + xPadding;
    const xmidFrontCent = 0.25*xWidth + xPadding;
    const xleftCent = 0.375*xWidth + xPadding;
    const xcent = 0.5*xWidth + xPadding;
    const xnearBack = 0.6875*xWidth + xPadding;
    const xback = xWidth + xPadding;

    // define y boundaries of vowel chart
    const yPadding = paddingVwlChrt.y;
    const yHeight = svgHeight - 2*yPadding;
    const yclose = yPadding;
    const ycloseMid = 0.3333*yHeight + yPadding;
    const yopenMid = 0.6666*yHeight + yPadding;
    const yopen = 0.9999*yHeight + yPadding;


    // Line properties
    const color = "#a2c8db";
    const strokeOpacity = 0.90;
    const strokeLinecap = "round";
    const strokeWidth = 3;

    // Text properties
    const fontSize = "smaller";
    const fontFamily = "Courier, Helvetica, Verdana"


    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // TEXT FOR VWL CHART
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // y labels
    const yAdjustAxis = 10
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xfront-10)
        .attr("text-anchor","end")
        .attr("y", yclose+yAdjustAxis)
        .text("close");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xnearFront-10)
        .attr("text-anchor","end")
        .attr("y", ycloseMid+10)
        .text("close-mid");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xmidFrontCent-10)
        .attr("text-anchor","end")
        .attr("y", yopenMid)
        .text("open-mid");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xleftCent-10)
        .attr("text-anchor","end")
        .attr("y", yopen)
        .text("open");

    // x labels
   svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xfront+10)
        .attr("text-anchor","end")
        .attr("y", yclose-10)
        .text("front");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xcent)
        .attr("text-anchor","middle")
        .attr("y", yclose - 10)
        .text("central");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xback)
        .attr("text-anchor","middle")
        .attr("y", yclose - 10)
        .text("back");

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // HORIZONTAL LINES FOR VWL CHART
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // create close line
    svg.append("line")
        .attr("x1", xfront)
        .attr("y1", yclose)
        .attr("x2", xback)
        .attr("y2", yclose)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);

    // create close-mid line
    svg.append("line")
        .attr("x1", xnearFront)
        .attr("y1", ycloseMid)
        .attr("x2", xback)
        .attr("y2", ycloseMid)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create open-mid line
    svg.append("line")
        .attr("x1", xmidFrontCent)
        .attr("y1", yopenMid)
        .attr("x2", xback)
        .attr("y2", yopenMid)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create open line
    svg.append("line")
        .attr("x1", xleftCent)
        .attr("y1", yopen)
        .attr("x2", xback)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // VERTICAL LINES FOR VWL CHART
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // create front line
    svg.append("line")
        .attr("x1", xfront)
        .attr("y1", yclose)
        .attr("x2", xleftCent)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create central line
    svg.append("line")
        .attr("x1", xcent)
        .attr("y1", yclose)
        .attr("x2", xnearBack)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create back line
    svg.append("line")
        .attr("x1", xback)
        .attr("y1", yclose)
        .attr("x2", xback)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
}

async function drawVowels() {
    const svg = d3.select("svg")
    const vwlChrtProperties = await svgGetPadding(svg);
    // const svgXOrigin = vwlChrtProperties.xOrigin;
    // const svgYOrigin = vwlChrtProperties.yOrigin;
    const svgWidth = vwlChrtProperties.width;
    const svgHeight = vwlChrtProperties.height;
    const padding = vwlChrtProperties.padding;
    const strokeLinecap = "round";
    const xWidth = svgWidth - 2 * padding.x;
    const yHeight = svgHeight - 2 * padding.y;
    const slope = (0.9999 * yHeight) / (0.375 * xWidth);
    // convert frequencies to svg scale
    // TODO: don't hardcode domains
    const f1ToYCoordinates = d3.scaleLinear()
        .domain([200, 850])
        .range([padding.y, svgHeight - padding.y])
        .clamp(true)
    function f2ToXCoordinates(d) {
        const y = f1ToYCoordinates(d.f1);
        const toXCoor = d3.scaleLinear()
            .domain([2500, 500])
            .range([(y + 2 * padding.x) / slope, svgWidth - padding.x])
        .clamp(true)
        return toXCoor(d.f2)
    }

    const glideMaker = d3.line()
        .y(d => f1ToYCoordinates(d.f1))
        .x(d => f2ToXCoordinates(d))
        .curve(d3.curveCardinal);

    const color = 'green';
    const hoverColor = 'green';
    const strokeWidthDefault = 5;
    const strokeWidthHover = 8;

    // Add arrow marker
    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr('color', color)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 5)
        .attr("markerWidth", 2)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("class", "arrowHead");

    d3.select("defs marker#arrow path")
        .attr("fill", color); // Change "red" to the desired color

    // connect the related ones!
    // Draw curves between related data points
    data.forEach(d => {
        if (Array.isArray(d.vwl)) {
            svg.append("path")
                .datum(d.vwl)
                .attr("fill", "none")
                .attr("stroke", color)
                .attr("stroke-width", strokeWidthDefault)
                .attr("stroke-linecap", strokeLinecap)
                .attr("marker-end", "url(#arrow)")
                .attr("d", glideMaker)
                .on("mouseover", function () {
                    d3.select(this)
                        .attr("stroke-width", strokeWidthHover)  // Increase stroke width on hover
                        .attr("stroke", hoverColor);   // Change stroke color on hover
                    // Change color of the arrowhead
                    d3.select("#arrow")
                        .select("path")
                        .attr("fill", hoverColor);
                })
                .on("mouseout", function () {
                    d3.select(this)
                        .attr("stroke-width", strokeWidthDefault)  // Restore original stroke width
                        .attr('stroke', color);
                    d3.select('#arrow')
                        .select('path')
                        .attr('fill', color)
                });
        } else {
            // Draw individual points if no related data points found
            svg.append("circle")
                .data([d.vwl])
                .join("circle")
                .attr("cx", d => f2ToXCoordinates(d))
                .attr("cy", d => f1ToYCoordinates(d.f1))
                .attr("r", strokeWidthDefault)
                .attr("fill", color)
                .on("mouseover", function () {
                    d3.select(this)
                        .attr("r", strokeWidthHover)  // Increase stroke width on hover
                        .attr("fill", hoverColor);   // Change stroke color on hover
                })
                .on("mouseout", function () {
                    d3.select(this)
                        .attr("r", strokeWidthDefault)  // Restore original stroke width
                        .attr('fill', color);
                });
        }
    });
    const colorSpa = 'steelblue';
    dataSpa.forEach(d => {
        console.log(d)
            if (Array.isArray(d.vwl)) {
                svg.append("path")
                    .datum(d.vwl)
                    .attr("fill", "none")
                    .attr("stroke", colorSpa)
                    .attr("stroke-width", strokeWidthDefault)
                    .attr("stroke-linecap", strokeLinecap)
                    .attr("marker-end", "url(#arrow)")
                    .attr("d", glideMaker)
                    .on("mouseover", function () {
                        d3.select(this)
                            .attr("stroke-width", strokeWidthHover)  // Increase stroke width on hover
                            .attr("stroke", colorSpa);   // Change stroke color on hover
                        // Change color of the arrowhead
                        d3.select("#arrow")
                            .select("path")
                            .attr("fill", colorSpa);
                    })
                    .on("mouseout", function () {
                        d3.select(this)
                            .attr("stroke-width", strokeWidthDefault)  // Restore original stroke width
                            .attr('stroke', colorSpa);
                        d3.select('#arrow')
                            .select('path')
                            .attr('fill', colorSpa)
                    });
            }
        }
    );
};
async function svgGetPadding(svg) {
    // get height and width of svg
    const svgViewBox = svg.attr("viewBox").split(',');
    const svgXOrigin = svgViewBox[0];
    const svgYOrigin = svgViewBox[1];
    const svgWidth = svgViewBox[2];
    const svgHeight = svgViewBox[3];

    // Padding for vowel chart
    const fracOfWidth = 0.125;
    const fracOfHeight = 0.0625;
    const padding = {
        x:fracOfWidth*svgWidth,
        y:fracOfHeight*svgHeight
    };
    return {padding:padding,
        xOrigin:svgXOrigin,
        yOrigin:svgYOrigin,
        width:svgWidth,
        height:svgHeight};
}
