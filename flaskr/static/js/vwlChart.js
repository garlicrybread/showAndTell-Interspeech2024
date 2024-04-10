// import dataL1 from '../participantData/silas/cheese/silas-cheese-2024_04_03_153402.json' with { type: 'json'};
import L1 from '../participantData/silas/cup/silas-cup-2024_04_03_153447.json' with { type: 'json'};
import L2 from '../participantData/yoder/cheese/yoder-cheese-2024_04_03_110616.json' with {type: 'json'};
import coordinatesL1 from '../participantData/yoder/vowelCalibration/vwlChartCoordinates.json' with { type: 'json'};

"use strict";
window.addEventListener("load", drawVowelChart);
// window.addEventListener("load", drawVowels(L1,L2));
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

    // Text Labels
    const topText = 'high';
    const midTopText = 'med-high';
    const midBottomText = 'med-low';
    const bottomText = 'low';


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
        .text(topText);
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xnearFront-10)
        .attr("text-anchor","end")
        .attr("y", ycloseMid+10)
        .text(midTopText);
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xmidFrontCent-10)
        .attr("text-anchor","end")
        .attr("y", yopenMid)
        .text(midBottomText);
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xleftCent-10)
        .attr("text-anchor","end")
        .attr("y", yopen)
        .text(bottomText);

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

export async function drawVowels(dataL1Path) {
    // fetch json data
    // const dataL1Path =
    const response1 = await fetch(dataL1Path);
    const dataL1 = await response1.json();

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
    const pad = 20;
    const xrangeL1 = [coordinatesL1[0][1]+pad, coordinatesL1[0][0]-pad];
    const yrangeL1 = [coordinatesL1[1][0]-pad, coordinatesL1[1][1]+pad];
    // convert frequencies to svg scale
    const f1ToYCoordinatesL1 = d3.scaleLinear()
        .domain(yrangeL1)
        .range([padding.y, svgHeight - padding.y])
        .clamp(true)
    function f2ToXCoordinatesL1(d) {
        const y = f1ToYCoordinatesL1(d.f1);
        const toXCoor = d3.scaleLinear()
            .domain(xrangeL1)
            .range([(y + 2 * padding.x) / slope, svgWidth - padding.x])
        .clamp(true)
        return toXCoor(d.f2)
    }
    const glideMakerL1 = d3.line()
        .y(d => f1ToYCoordinatesL1(d.f1))
        .x(d => f2ToXCoordinatesL1(d))
        .curve(d3.curveCardinal);

    const colorSpa = 'green';
    const hoverColor = 'green';
    const strokeWidthDefault = 5;
    const strokeWidthHover = 8;

    // Add arrow marker
    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr('color', colorSpa)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 5)
        .attr("markerWidth", 2)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("class", "arrowHead");

    d3.select("defs marker#arrow path")
        .attr("fill", colorSpa); // Change "red" to the desired color

    // connect the related ones!
    // Draw curves between related data points
    dataL1.forEach(d => {
        if (Array.isArray(d.vwl)) {
            svg.append("path")
                .datum(d.vwl)
                .attr("fill", "none")
                .attr("stroke", colorSpa)
                .attr("stroke-width", strokeWidthDefault)
                .attr("stroke-linecap", strokeLinecap)
                .attr("marker-end", "url(#arrow)")
                .attr("d", glideMakerL1)
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
                        .attr('stroke', colorSpa);
                    d3.select('#arrow')
                        .select('path')
                        .attr('fill', colorSpa)
                });
        } else {
            // Draw individual points if no related data points found
            svg.append("circle")
                .data([d.vwl])
                .join("circle")
                .attr("cx", d => f2ToXCoordinatesL1(d))
                .attr("cy", d => f1ToYCoordinatesL1(d.f1))
                .attr("r", strokeWidthDefault)
                .attr("fill", colorSpa)
                .on("mouseover", function () {
                    d3.select(this)
                        .attr("r", strokeWidthHover)  // Increase stroke width on hover
                        .attr("fill", hoverColor);   // Change stroke color on hover
                })
                .on("mouseout", function () {
                    d3.select(this)
                        .attr("r", strokeWidthDefault)  // Restore original stroke width
                        .attr('fill', colorSpa);
                });
        }
    });
}
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
